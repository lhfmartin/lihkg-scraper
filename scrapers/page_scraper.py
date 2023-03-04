import logging
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from drivers import driver


logger = logging.getLogger("lihkg-scraper")


def scrape_page(thread_id, page_number, open_new_tab=False):
    thread_url = f"https://lihkg.com/thread/{thread_id}"
    page_url = f"{thread_url}/page/{page_number}"
    logger.debug(f"Scraping {page_url}")

    if driver.current_url.startswith(thread_url) and page_number % 7 != 0:
        # Navigating to a different page using the drop down list prevents triggering of Cloudflare Turnstile
        # The page is still reloaded when `page_number % 7 != 0` to reduce RAM usage
        page_select = Select(driver.find_elements(By.TAG_NAME, "select")[-2])
        page_select.select_by_value(str(page_number))
    else:
        if open_new_tab:
            driver.switch_to.new_window("tab")

        driver.get(page_url)

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
    return json.loads(res["body"])
