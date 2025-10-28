from dao import ImageDao, PageDao, ThreadDao, TopicListDao
from enums import ArtifactCategory, PostProcessingActions
import logging
from models import ArtifactMetadata
from postprocessing import (
    remove_logged_in_user_data,
    consolidate_messages,
    download_images,
)

logger = logging.getLogger("lihkg-scraper")


def apply(
    post_processing_actions: (
        list[PostProcessingActions]
        | set[PostProcessingActions]
        | tuple[PostProcessingActions, ...]
    ),
    artifact_metadata: ArtifactMetadata,
    thread_dao: ThreadDao | None = None,
    page_dao: PageDao | None = None,
    image_dao: ImageDao | None = None,
    topic_list_dao: TopicListDao | None = None,
) -> None:
    if PostProcessingActions.ALL in post_processing_actions:
        post_processing_actions = [x for x in PostProcessingActions]

    if artifact_metadata.category == ArtifactCategory.THREAD:
        assert None not in (thread_dao, page_dao, image_dao)

        # Remove the user data of the logged-in user, shall be done before consolidate_messages
        if PostProcessingActions.REMOVE_ME in post_processing_actions:
            logger.info(
                f"Performing {PostProcessingActions.REMOVE_ME} on {thread_dao.artifact_folder_path}"
            )
            remove_logged_in_user_data(thread_dao, page_dao)
            logger.info(
                f"Completed {PostProcessingActions.REMOVE_ME} on {thread_dao.artifact_folder_path}"
            )

        # Consolidate messages and write to messages.json
        if PostProcessingActions.CONSOLIDATE_MESSAGES in post_processing_actions:
            logger.info(
                f"Performing {PostProcessingActions.CONSOLIDATE_MESSAGES} on {thread_dao.artifact_folder_path}"
            )
            consolidate_messages(page_dao, thread_dao)
            logger.info(
                f"Completed {PostProcessingActions.CONSOLIDATE_MESSAGES} on {thread_dao.artifact_folder_path}"
            )

        # Download images and save images and image mappings to images/ and images.json respectively
        if PostProcessingActions.DOWNLOAD_IMAGES in post_processing_actions:
            logger.info(
                f"Performing {PostProcessingActions.DOWNLOAD_IMAGES} on {thread_dao.artifact_folder_path}"
            )
            download_images(thread_dao, image_dao)
            logger.info(
                f"Completed {PostProcessingActions.DOWNLOAD_IMAGES} on {thread_dao.artifact_folder_path}"
            )

    elif artifact_metadata.category == ArtifactCategory.TOPICS:
        assert None not in (topic_list_dao,)

        # Remove the user data of the logged-in user
        if PostProcessingActions.REMOVE_ME in post_processing_actions:
            logger.info(
                f"Performing {PostProcessingActions.REMOVE_ME} on {topic_list_dao.artifact_folder_path}"
            )
            remove_logged_in_user_data(topic_list_dao)
            logger.info(
                f"Completed {PostProcessingActions.REMOVE_ME} on {topic_list_dao.artifact_folder_path}"
            )
