import logging
from pathlib import Path

from analytics import initialize_posthog, posthog
from dao import ImageDao, PageDao, ThreadDao, TopicListDao
import postprocessing.apply
from logger import initialize_logger
from enums import ArtifactCategory, PostProcessingActions
from models import ArtifactMetadata


def postprocess(folder: str, actions: list[str]) -> None:
    with initialize_posthog():
        initialize_logger()
        logger = logging.getLogger("lihkg-scraper")

        posthog.capture(
            "postprocess_workflow_started",
            properties={"folder": folder, "post_processing_actions": actions},
        )

        path = Path(folder)

        if not (path.exists() and path.is_dir()):
            raise FileNotFoundError(f"'{folder}' does not exist or is not a directory")

        artifact_metadata = ArtifactMetadata.from_folder_name(path.name)

        thread_dao = image_dao = page_dao = topic_list_dao = None

        if artifact_metadata.category == ArtifactCategory.THREAD:
            thread_dao = ThreadDao(path.parent, artifact_metadata)
            image_dao = ImageDao(path.parent, artifact_metadata)
            page_dao = PageDao(path.parent, artifact_metadata)
        elif artifact_metadata.category == ArtifactCategory.TOPICS:
            topic_list_dao = TopicListDao(path.parent, artifact_metadata)

        postprocessing.apply(
            [PostProcessingActions(x) for x in actions],
            artifact_metadata,
            thread_dao,
            page_dao,
            image_dao,
            topic_list_dao,
        )

        posthog.capture("postprocess_workflow_completed")

        logger.info("Done")
