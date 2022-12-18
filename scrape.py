if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread", required=True)
    parser.add_argument("-p", "--page", required=False)
    parser.add_argument("-o", "--output-folder", required=False)
    args = parser.parse_args()
    thread_id = args.thread
    page_number = args.page
    output_folder_path = args.output_folder

    import os
    import copy
    import logging
    import json
    import time
    import pathlib

    import scrapers
    from post_processing import consolidate_messages

    LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s: %(message)s"
    logger = logging.getLogger("lihkg-scraper")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    if output_folder_path is None:
        output_folder_path = "."
    thread_folder_path = os.path.join(
        output_folder_path, f"thread_{thread_id} {time.strftime('%Y%m%d_%H%M%S')}"
    )
    thread_pages_raw_jsons_folder_path = os.path.join(thread_folder_path, "pages")

    logger.debug(
        f"Scraping {'page ' + page_number if page_number is not None else 'all pages'} of thread {thread_id}. Output files will be saved in {thread_folder_path}"
    )

    pathlib.Path(thread_folder_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(thread_pages_raw_jsons_folder_path).mkdir(parents=True, exist_ok=True)

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
        with open(
            os.path.join(
                thread_pages_raw_jsons_folder_path, f"page_{page_number}.json"
            ),
            "w+",
        ) as f:
            f.write(json.dumps(page_data, ensure_ascii=False) + "\n")

    thread_data = copy.deepcopy(page_data["response"])
    del thread_data["page"]
    del thread_data["item_data"]
    if "me" in thread_data:
        del thread_data["me"]

    with open(os.path.join(thread_folder_path, "thread.json"), "w+") as f:
        f.write(json.dumps(thread_data, ensure_ascii=False) + "\n")

    consolidate_messages(thread_folder_path)

    logger.debug(f"Scraping completed")
