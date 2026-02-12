from enum import Enum


class PostProcessingActions(Enum):
    ALL = "all"
    REMOVE_LOGGED_IN_USER_DATA = "remove_logged_in_user_data"
    CONSOLIDATE_MESSAGES = "consolidate_messages"
    DOWNLOAD_IMAGES = "download_images"

    def __str__(self):
        return self.value
