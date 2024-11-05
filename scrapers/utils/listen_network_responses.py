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
    req_id = None
    res_url = None
    is_res_completely_loaded = False

    t_0 = time.perf_counter()
    while not is_res_completely_loaded:
        if time.perf_counter() - t_0 > LOADING_TIMEOUT:
            raise RuntimeError(
                "Did not receive the anticipated response within the timeout period"
            )
        performance_logs = driver.get_log("performance")
        performance_logs = [
            json.loads(pl["message"])["message"] for pl in performance_logs
        ]

        for pl in performance_logs:
            if (
                pl["method"] == "Network.responseReceived"
                and "json" in pl["params"]["response"]["mimeType"]
                and _url_matches_patterns(pl["params"]["response"]["url"], url_patterns)
            ):
                req_id = pl["params"]["requestId"]
                res_url = pl["params"]["response"]["url"]
            elif (
                pl["method"] == "Network.loadingFinished"
                and pl["params"]["requestId"] == req_id
            ):
                is_res_completely_loaded = True

        time.sleep(0.1)

    res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})

    return res_url, json.loads(res["body"])
