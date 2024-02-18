from collections.abc import Iterator
from scrapers.pages_scraper import scrape_pages


def scrape_thread(
    thread_id: str, open_new_tab: bool = False
) -> Iterator[tuple[int, dict]]:
    return scrape_pages(thread_id, open_new_tab=open_new_tab)
