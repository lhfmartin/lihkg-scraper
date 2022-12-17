from drivers import driver
from scrapers.page_scraper import scrape_page


def scrape_thread(thread, open_new_tab=False):
    if open_new_tab:
        driver.switch_to.new_window("tab")

    page = 1
    while True:
        thread_page = scrape_page(thread, page)
        yield (page, thread_page)
        if page == int(thread_page["response"]["total_page"]):
            break
        page += 1
