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

    import copy
    import logging
    import time

    import scrapers
    from dao import ImageDao, PageDao, ThreadDao
    from post_processing import consolidate_messages, download_images

    LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s: %(message)s"
    logger = logging.getLogger("lihkg-scraper")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    if output_folder_path is None:
        output_folder_path = "."

    scrape_time_str = time.strftime("%Y%m%d_%H%M%S")
    thread_dao = ThreadDao(output_folder_path, thread_id, scrape_time_str)
    image_dao = ImageDao(output_folder_path, thread_id, scrape_time_str)
    page_dao = PageDao(output_folder_path, thread_id, scrape_time_str)

    logger.debug(
        f"Scraping {'page ' + page_number if page_number is not None else 'all pages'} of thread {thread_id}. Output files will be saved in {thread_dao.thread_folder_path}"
    )

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
        page_dao.save_page(page_number, page_data)

    # Process thread data and write to topic.json
    thread_data = copy.deepcopy(page_data["response"])
    del thread_data["page"]
    del thread_data["item_data"]
    if "me" in thread_data:
        del thread_data["me"]

    thread_dao.save_topic(thread_data)

    # Consolidate messages and write to messages.json
    all_messages = consolidate_messages(page_dao)

    output_file_type = "json"

    if output_file_type == "csv":  # Not supported currently
        import pandas as pd

        pd.DataFrame(all_messages).set_index("msg_num").to_csv(
            os.path.join(thread_folder_path, "messages.csv")
        )
    elif output_file_type == "json":
        thread_dao.save_messages(all_messages)

    # Download images
    images_downloads = download_images(thread_dao)

    for image_url in images_downloads["downloaded"]:
        image_new_file_name, image_binary = images_downloads["downloaded"][image_url]
        image_dao.save_image(image_new_file_name, image_binary)

        images_downloads["downloaded"][image_url] = image_new_file_name

    thread_dao.save_image_mappings(images_downloads)

    logger.debug(
        f"Scraping completed. Data have been saved to {thread_dao.thread_folder_path}"
    )
