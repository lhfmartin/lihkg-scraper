import json
import os

from .Dao import Dao
from models import ArtifactMetadata


class TopicListDao(Dao):
    def __init__(self, output_folder_path: str, artifact_metadata: ArtifactMetadata):
        super().__init__(output_folder_path, artifact_metadata)

    def save_topic_list(self, topic_list: list[dict]) -> None:
        with open(
            os.path.join(self.artifact_folder_path, "topics.json"),
            "w+",
        ) as f:
            json.dump(topic_list, f, ensure_ascii=False)
            f.write("\n")

    def load_topic_list(self) -> list[dict]:
        with open(
            os.path.join(self.artifact_folder_path, "topics.json"),
            "r",
        ) as f:
            topic_list = json.load(f)
        return topic_list
