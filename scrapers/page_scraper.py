import logging
import json
import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from drivers import driver


logger = logging.getLogger("lihkg-scraper")


def scrape_page(thread_id, page_number, open_new_tab=False):
    if open_new_tab:
        driver.switch_to.new_window("tab")

    thread_url = f"https://lihkg.com/thread/{thread_id}"
    page_url = f"{thread_url}/page/{page_number}"
    logger.debug(f"Scraping {page_url}")

    if driver.current_url.startswith(
        thread_url
    ) and scrape_page.dom_reuse_count < randint(
        max(6, scrape_page.dom_reuse_count), 10
    ):
        # Navigating to a different page using the drop down list prevents triggering of Cloudflare Turnstile
        # The page is still reloaded when the current DOM is reused 6 - 10 times (i.e. 7 - 11 pages have been rendered) to reduce RAM usage
        page_select = Select(driver.find_elements(By.CSS_SELECTOR, "select:not([class])")[-1])
        page_select.select_by_value(str(page_number))
        scrape_page.dom_reuse_count += 1
    else:
        driver.get(page_url)
        scrape_page.dom_reuse_count = 0

    performance_logs_filtered = []
    TIMEOUT = 5
    t_0 = time.perf_counter()
    while len(performance_logs_filtered) < 1:
        if time.perf_counter() - t_0 > TIMEOUT:
            logger.error(f"Timeout exceeded")
            break
        performance_logs = driver.get_log("performance")
        performance_logs = [
            json.loads(pl["message"])["message"] for pl in performance_logs
        ]

        performance_logs = [
            pl
            for pl in performance_logs
            if pl["method"] == "Network.responseReceived"
            and "json" in pl["params"]["response"]["mimeType"]
            and f"{thread_id}/page/{page_number}" in pl["params"]["response"]["url"]
        ]

        performance_logs_filtered += performance_logs
        time.sleep(0.1)

    assert len(performance_logs_filtered) == 1

    log = performance_logs_filtered[0]
    req_id = log["params"]["requestId"]
    res_url = log["params"]["response"]["url"]
    res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})

    if open_new_tab:
        driver.close()
    return json.loads(res["body"])


scrape_page.dom_reuse_count = 0
