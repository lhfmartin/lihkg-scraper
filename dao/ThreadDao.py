import json
import os

from .Dao import Dao
from models import ArtifactMetadata


class ThreadDao(Dao):
    def __init__(self, output_folder_path: str, artifact_metadata: ArtifactMetadata):
        super().__init__(output_folder_path, artifact_metadata)

    def save_topic(self, thread_data: dict) -> None:
        with open(os.path.join(self.folder_path, "topic.json"), "w+") as f:
            json.dump(thread_data, f, ensure_ascii=False)
            f.write("\n")

    def load_topic(self) -> dict:
        with open(os.path.join(self.folder_path, "topic.json"), "r") as f:
            topic = json.load(f)
        return topic

    def save_messages(self, messages: list[dict]) -> None:
        with open(os.path.join(self.folder_path, "messages.json"), "w+") as f:
            json.dump(messages, f, ensure_ascii=False)
            f.write("\n")

    def load_messages(self) -> list[dict]:
        with open(os.path.join(self.folder_path, "messages.json"), "r") as f:
            messages = json.load(f)
        return messages

    def save_image_mappings(self, image_mappings: dict) -> None:
        with open(os.path.join(self.folder_path, "images.json"), "w+") as f:
            json.dump(image_mappings, f, ensure_ascii=False)
            f.write("\n")
