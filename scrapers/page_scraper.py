import logging
import json
import time
from random import randint

from browsers import browser


logger = logging.getLogger("lihkg-scraper")


def scrape_page(thread_id, page_number, tab=None):
    open_new_tab = True if tab is None else False
    if open_new_tab:
        tab = browser.new_page()

    thread_url = f"https://lihkg.com/thread/{thread_id}"
    page_url = f"{thread_url}/page/{page_number}"
    logger.debug(f"Scraping {page_url}")

    with tab.expect_response(
        f"*/api_v2/thread/{thread_id}/page/{page_number}*", timeout=60 * 1000
    ) as res:
        if tab.url.startswith(thread_url) and scrape_page.dom_reuse_count < randint(
            max(6, scrape_page.dom_reuse_count), 10
        ):
            # Navigating to a different page using the drop down list prevents triggering of Cloudflare Turnstile
            # The page is still reloaded when the current DOM is reused 6 - 10 times (i.e. 7 - 11 pages have been rendered) to reduce RAM usage
            page_select = tab.locator("select:not([class])").all()[-1]
            page_select.select_option(str(page_number))
            scrape_page.dom_reuse_count += 1
        else:
            tab.goto(page_url)
            scrape_page.dom_reuse_count = 0

    if open_new_tab:
        tab.close()
    return res.value.json()


scrape_page.dom_reuse_count = 0
