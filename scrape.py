if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread", required=True)
    parser.add_argument("-p", "--page", required=False)
    parser.add_argument("-o", "--output-folder", required=False)
    args = parser.parse_args()
    thread_id = args.thread
    page_number = args.page
    output_folder = args.output_folder

    import os
    import logging
    import json
    import time
    import pathlib

    import scrapers

    FORMAT = "%(asctime)s %(filename)s %(levelname)s: %(message)s"
    logger = logging.getLogger("lihkg-scraper")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    if output_folder is None:
        output_folder = "."
    output_folder = os.path.join(
        output_folder, f"thread_{thread_id} {time.strftime('%Y%m%d-%H%M%S')}"
    )

    logger.debug(
        f"Scraping {'page ' + page_number if page_number is not None else 'all pages'} of thread {thread_id}. Output files will be saved to {output_folder}"
    )

    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

    if page_number is None:
        pages = scrapers.scrape_thread(thread_id, open_new_tab=True)
    else:
        pages = scrapers.scrape_pages(
            thread_id,
            start_page_number=page_number,
            end_page_number=page_number,
            open_new_tab=True,
        )

    for page_number, page_data in pages:
        with open(os.path.join(output_folder, f"page_{page_number}.json"), "w+") as f:
            f.write(json.dumps(page_data, ensure_ascii=False) + "\n")

    logger.debug(f"Scraping completed")
