import copy
import logging

import scraping.core
from dao import ImageDao, PageDao, ThreadDao
from postprocessing import (
    remove_logged_in_user_data,
    consolidate_messages,
    download_images,
)
from logger import initialize_logger
from models import ArtifactMetadata


def scrape_thread(
    thread_id: str, page_numbers: str, output_folder_path: str, remove_me: bool
) -> None:
    initialize_logger()
    logger = logging.getLogger("lihkg-scraper")

    page_numbers_actual = set()
    if page_numbers is not None:
        for page_range in page_numbers.split(","):
            for page in range(
                int(page_range.split("-")[0]),
                int(page_range.split("-")[-1]) + 1,
            ):
                page_numbers_actual.add(page)

    artifact_metadata = ArtifactMetadata("thread", thread_id)

    thread_dao = ThreadDao(output_folder_path, artifact_metadata)
    image_dao = ImageDao(output_folder_path, artifact_metadata)
    page_dao = PageDao(output_folder_path, artifact_metadata)

    logger.info(
        f"Scraping {'page ' + ','.join(map(str, page_numbers_actual)) if len(page_numbers_actual) > 0 else 'all pages'} of thread {thread_id}. Output files will be saved in {thread_dao.artifact_folder_path}"
    )

    if len(page_numbers_actual) == 0:
        pages = scraping.core.scrape_thread(thread_id, open_new_tab=True)
    else:
        pages = scraping.core.scrape_pages(
            thread_id,
            page_numbers=page_numbers_actual,
            open_new_tab=True,
        )

    for page_number, page_data in pages:
        page_dao.save_page(page_number, page_data)

    # Process thread data and write to topic.json
    thread_data = copy.deepcopy(page_data["response"])
    del thread_data["page"]
    del thread_data["item_data"]
    thread_dao.save_topic(thread_data)

    # Postprocessing

    # Remove the user data of the logged-in user, shall be done before consolidate_messages
    if remove_me:
        remove_logged_in_user_data(thread_dao, page_dao)

    # Consolidate messages and write to messages.json
    consolidate_messages(page_dao, thread_dao)

    # Download images and save images and image mappings to images/ and images.json respectively
    download_images(thread_dao, image_dao)

    logger.info(
        f"Scraping completed. Data have been saved to {thread_dao.artifact_folder_path}"
    )
