from datetime import datetime, timezone
import logging

import scrapers.core
from dao import TopicListDao
from postprocessing import remove_logged_in_user_data
from logger import initialize_logger
from models import ArtifactMetadata


def scrape_left_panel(
    url: str, limit: int | None, output_folder_path: str, remove_me: bool
) -> None:
    initialize_logger()
    logger = logging.getLogger("lihkg-scraper")

    scrape_time_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    logger.info(f"Scraping the left panel of {url}")

    left_panel_content_identifier, topics = scrapers.core.scrape_left_panel(
        url, limit, open_new_tab=True
    )

    artifact_metadata = ArtifactMetadata(
        "topics",
        left_panel_content_identifier,
        scrape_time_str,
    )

    topic_list_dao = TopicListDao(output_folder_path, artifact_metadata)

    topic_list_dao.save_topic_list(topics)

    # Postprocessing

    # Remove the user data of the logged-in user
    if remove_me:
        remove_logged_in_user_data(topic_list_dao)

    logger.info(
        f"Scraping completed. Data have been saved to {topic_list_dao.artifact_folder_path}"
    )
