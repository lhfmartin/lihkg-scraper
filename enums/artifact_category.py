from enum import Enum


class ArtifactCategory(Enum):
    THREAD = "thread"
    TOPICS = "topics"

    def __str__(self):
        return self.value
