from browsers import browser
from collections.abc import Iterator
from scrapers.page_scraper import scrape_page


def scrape_pages(
    thread_id,
    start_page_number=1,
    end_page_number=None,
    page_numbers=(),
    tab=None,
):
    open_new_tab = True if tab is None else False
    if open_new_tab:
        tab = browser.new_page()

    if len(page_numbers) > 0:
        page_numbers = iter(sorted(page_numbers))
        start_page_number = next(page_numbers)

    page_number = start_page_number
    while True:
        page_data = scrape_page(thread_id, page_number, tab=tab)
        yield (page_number, page_data)
        if (
            page_number == int(page_data["response"]["total_page"])
            or page_number == end_page_number
        ):
            break

        if isinstance(page_numbers, Iterator):
            try:
                page_number = next(page_numbers)
                if page_number > int(page_data["response"]["total_page"]):
                    raise StopIteration()
            except StopIteration:
                break
        else:
            page_number += 1

    if open_new_tab:
        tab.close()
