if __name__ == "__main__":
    from enum import Enum

    class PostProcessingActions(Enum):
        ALL = "all"
        CONSOLIDATE_MESSAGES = "consolidate_messages"
        DOWNLOAD_IMAGES = "download_images"

        def __str__(self):
            return self.value

    import argparse

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("folder")
    parser.add_argument(
        "-a",
        "--actions",
        required=False,
        default=[PostProcessingActions.ALL],
        choices=[str(x) for x in PostProcessingActions],
        nargs="+",
    )
    args = parser.parse_args()
    folder = args.folder
    actions = args.actions

    import logging
    import os
    from pathlib import Path
    import sys

    from dao import ImageDao, PageDao, ThreadDao
    from postprocessing import consolidate_messages, download_images

    LOG_FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"
    logger = logging.getLogger("lihkg-scraper")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    actions = [PostProcessingActions(x) for x in actions]
    if PostProcessingActions.ALL in actions:
        actions = [x for x in PostProcessingActions]

    thread_dao = ThreadDao(
        Path(folder).parent, folder.split("_")[-2], folder.split("_")[-1]
    )
    image_dao = ImageDao(
        Path(folder).parent, folder.split("_")[-2], folder.split("_")[-1]
    )
    page_dao = PageDao(
        Path(folder).parent, folder.split("_")[-2], folder.split("_")[-1]
    )

    if PostProcessingActions.CONSOLIDATE_MESSAGES in actions:
        logger.info(
            f"Performing {PostProcessingActions.CONSOLIDATE_MESSAGES} on {thread_dao.thread_folder_path}"
        )
        consolidate_messages(page_dao, thread_dao)

    if PostProcessingActions.DOWNLOAD_IMAGES in actions:
        logger.info(
            f"Performing {PostProcessingActions.DOWNLOAD_IMAGES} on {thread_dao.thread_folder_path}"
        )
        download_images(thread_dao, image_dao)

    logger.info("Done")