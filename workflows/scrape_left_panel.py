import logging

import scraping
from dao import TopicListDao
import postprocessing.apply
from logger import initialize_logger
from enums import ArtifactCategory, PostProcessingActions
from models import ArtifactMetadata


def scrape_left_panel(
    url: str,
    limit: int | None,
    output_folder_path: str,
    post_processing_actions: list[str],
) -> None:
    initialize_logger()
    logger = logging.getLogger("lihkg-scraper")

    artifact_metadata = ArtifactMetadata(ArtifactCategory.TOPICS, url)

    logger.info(f"Scraping the left panel of {url}")

    left_panel_content_identifier, topics = scraping.scrape_left_panel(
        url, limit, open_new_tab=True
    )

    artifact_metadata.content_identifier = left_panel_content_identifier

    topic_list_dao = TopicListDao(output_folder_path, artifact_metadata)

    topic_list_dao.save_topic_list(topics)

    # Postprocessing

    postprocessing.apply(
        [PostProcessingActions(x) for x in post_processing_actions],
        artifact_metadata,
        topic_list_dao=topic_list_dao,
    )

    logger.info(
        f"Scraping completed. Data have been saved to {topic_list_dao.artifact_folder_path}"
    )
