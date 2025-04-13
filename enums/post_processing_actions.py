from enum import Enum


class PostProcessingActions(Enum):
    ALL = "all"
    REMOVE_ME = "remove_me"
    CONSOLIDATE_MESSAGES = "consolidate_messages"
    DOWNLOAD_IMAGES = "download_images"

    def __str__(self):
        return self.value
