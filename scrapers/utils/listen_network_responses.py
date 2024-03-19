import logging
import time
import re
import json

from drivers import driver


LOADING_TIMEOUT = 60

logger = logging.getLogger("lihkg-scraper")


def _url_matches_patterns(url: str, patterns: list[str]) -> bool:
    return any([bool(re.search(pattern, url)) for pattern in patterns])


def listen_network_responses(
    url_patterns: list[str],
) -> tuple[str, str | int | float | dict | list]:
    performance_logs_filtered = []

    t_0 = time.perf_counter()
    while len(performance_logs_filtered) < 1:
        if time.perf_counter() - t_0 > LOADING_TIMEOUT:
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
            and _url_matches_patterns(pl["params"]["response"]["url"], url_patterns)
        ]

        performance_logs_filtered += performance_logs
        time.sleep(0.1)

    assert len(performance_logs_filtered) == 1

    log = performance_logs_filtered[0]
    req_id = log["params"]["requestId"]
    res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})

    return log["params"]["response"]["url"], json.loads(res["body"])
