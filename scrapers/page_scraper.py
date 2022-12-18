import logging
import json
import time

from drivers import driver


logger = logging.getLogger("lihkg-scraper")


def scrape_page(thread_id, page_number, open_new_tab=False):
    if open_new_tab:
        driver.switch_to.new_window("tab")

    page_url = f"https://lihkg.com/thread/{thread_id}/page/{page_number}"
    logger.debug(f"Scraping {page_url}")
    driver.get(page_url)

    performance_logs_filtered = []
    TIMEOUT = 5
    t_0 = time.time()
    while len(performance_logs_filtered) < 1:
        if time.time() - t_0 > TIMEOUT:
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
        time.sleep(2)

    assert len(performance_logs_filtered) == 1

    log = performance_logs_filtered[0]
    req_id = log["params"]["requestId"]
    res_url = log["params"]["response"]["url"]
    res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})
    return json.loads(res["body"])
