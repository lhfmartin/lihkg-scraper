import logging
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from drivers import driver
from scraping.utils import listen_network_responses


logger = logging.getLogger("lihkg-scraper")


def scrape_page(thread_id: str, page_number: int, open_new_tab: bool = False) -> dict:
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
        page_select = Select(
            driver.find_elements(By.CSS_SELECTOR, "select:not([class])")[-1]
        )
        page_select.select_by_value(str(page_number))
        scrape_page.dom_reuse_count += 1
    else:
        driver.get(page_url)
        scrape_page.dom_reuse_count = 0

    _, page_data = listen_network_responses(
        [f"lihkg\\.com/api_v2/thread/{thread_id}/page/{page_number}\\?"]
    )

    if open_new_tab:
        driver.close()

    return page_data


scrape_page.dom_reuse_count = 0
