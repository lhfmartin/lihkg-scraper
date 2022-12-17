from drivers import driver
from scrapers.page_scraper import scrape_page


def scrape_thread(thread_id, open_new_tab=False):
    if open_new_tab:
        driver.switch_to.new_window("tab")

    page_number = 1
    while True:
        page_data = scrape_page(thread_id, page_number)
        yield (page_number, page_data)
        if page_number == int(page_data["response"]["total_page"]):
            break
        page_number += 1
