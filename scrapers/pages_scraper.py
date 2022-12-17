from drivers import driver
from scrapers.page_scraper import scrape_page


def scrape_pages(
    thread_id, start_page_number=1, end_page_number=None, open_new_tab=False
):
    if open_new_tab:
        driver.switch_to.new_window("tab")

    page_number = start_page_number
    while True:
        page_data = scrape_page(thread_id, page_number)
        yield (page_number, page_data)
        if (
            page_number == int(page_data["response"]["total_page"])
            or page_number == end_page_number
        ):
            break
        page_number += 1
