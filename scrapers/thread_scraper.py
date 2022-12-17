from drivers import driver
from scrapers.pages_scraper import scrape_pages


def scrape_thread(thread_id, open_new_tab=False):
    return scrape_pages(thread_id, open_new_tab=open_new_tab)
