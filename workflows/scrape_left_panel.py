import logging

import scraping
from dao import TopicListDao
from postprocessing import remove_logged_in_user_data
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

    post_processing_actions = [
        PostProcessingActions(x) for x in post_processing_actions
    ]
    if PostProcessingActions.ALL in post_processing_actions:
        post_processing_actions = [x for x in PostProcessingActions]

    artifact_metadata = ArtifactMetadata(ArtifactCategory.TOPICS, url)

    logger.info(f"Scraping the left panel of {url}")

    left_panel_content_identifier, topics = scraping.scrape_left_panel(
        url, limit, open_new_tab=True
    )

    artifact_metadata.content_identifier = left_panel_content_identifier

    topic_list_dao = TopicListDao(output_folder_path, artifact_metadata)

    topic_list_dao.save_topic_list(topics)

    # Postprocessing

    # Remove the user data of the logged-in user
    if PostProcessingActions.REMOVE_ME in post_processing_actions:
        remove_logged_in_user_data(topic_list_dao)

    logger.info(
        f"Scraping completed. Data have been saved to {topic_list_dao.artifact_folder_path}"
    )
