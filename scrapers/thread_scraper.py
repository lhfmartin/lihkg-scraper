from scrapers.pages_scraper import scrape_pages


def scrape_thread(thread_id, tab=None):
    return scrape_pages(thread_id, tab=tab)
