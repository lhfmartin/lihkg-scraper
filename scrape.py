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
    output_folder = os.path.join(output_folder, thread_id)

    logger.debug(
        f"Scraping {'page ' + page_number if page_number is not None else 'all pages'} of thread {thread_id}"
    )

    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

    if page_number is None:
        for page_number, page_data in scrapers.scrape_thread(thread_id, True):
            with open(
                os.path.join(output_folder, f"page_{page_number}.json"), "w+"
            ) as f:
                f.write(json.dumps(page_data, ensure_ascii=False) + "\n")
    else:
        page_data = scrapers.scrape_page(thread_id, page_number, True)
        with open(os.path.join(output_folder, f"page_{page_number}.json"), "w+") as f:
            f.write(json.dumps(page_data, ensure_ascii=False) + "\n")
