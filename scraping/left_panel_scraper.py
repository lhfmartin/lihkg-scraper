import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from drivers import driver
from scraping.utils import (
    listen_network_responses,
    determine_left_panel_content_identifier,
)


logger = logging.getLogger("lihkg-scraper")


def scrape_left_panel(
    url: str, limit: int | None = None, open_new_tab: bool = False
) -> tuple[str, list[dict]]:
    if open_new_tab:
        driver.switch_to.new_window("tab")

    driver.get(url)

    topics = []
    res_body_relevant = None

    while limit is None or len(topics) < limit:
        res_url, res_body = listen_network_responses(
            [
                r"lihkg\.com/api_v2/thread/category\?",
                r"lihkg\.com/api_v2/user/(\d+)/thread\?",
                r"lihkg\.com/api_v2/thread/bookmark\?",
                r"lihkg\.com/api_v2/thread/hot\?",
                r"lihkg\.com/api_v2/thread/latest\?",
                r"lihkg\.com/api_v2/thread/custom\?",
                r"lihkg\.com/api_v2/thread/news\?",
            ],
        )

        if "response" in res_body:
            res_body_relevant = res_body

        if (
            "error_code"
            in res_body  # Useful when the total number of topics is a multiple of the number of topics in one page
            or len(
                driver.find_elements(
                    By.CSS_SELECTOR, ".qoAmEqNpZRLf2KVKZ8DsC > ._33r1FGqGJZF-fM1VZm7mhN"
                )
            )
            > 0
        ):
            break

        topics += res_body["response"]["items"]

        ActionChains(driver).move_to_element(
            driver.find_elements(By.CSS_SELECTOR, ".qoAmEqNpZRLf2KVKZ8DsC > span")[0]
        ).perform()

    if limit is not None:
        topics = topics[:limit]

    left_panel_content_identifier = determine_left_panel_content_identifier(
        res_url, res_body_relevant
    )

    if open_new_tab:
        driver.close()

    return left_panel_content_identifier, topics
