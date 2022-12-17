import json
import time

from drivers import driver


def scrape_page(thread, page, open_new_tab=False):
    if open_new_tab:
        driver.switch_to.new_window("tab")

    driver.get(f"https://lihkg.com/thread/{thread}/page/{page}")

    performance_logs_filtered = []
    while True:
        performance_logs = driver.get_log("performance")
        performance_logs = [
            json.loads(pl["message"])["message"] for pl in performance_logs
        ]
        if len(performance_logs) == 0:
            break

        performance_logs = [
            pl
            for pl in performance_logs
            if pl["method"] == "Network.responseReceived"
            and "json" in pl["params"]["response"]["mimeType"]
            and f"{thread}/page/{page}" in pl["params"]["response"]["url"]
        ]

        performance_logs_filtered += performance_logs
        time.sleep(2)

    assert len(performance_logs_filtered) == 1

    log = performance_logs_filtered[0]
    req_id = log["params"]["requestId"]
    res_url = log["params"]["response"]["url"]
    print(f"Parsing {res_url}")
    res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})
    return json.loads(res["body"])