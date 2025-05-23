import os
import pathlib

from .Dao import Dao
from models import ArtifactMetadata
from config import config


class ImageDao(Dao):
    def __init__(self, output_folder_path: str, artifact_metadata: ArtifactMetadata):
        super().__init__(output_folder_path, artifact_metadata)
        self.thread_images_folder_path = (
            config.get("postprocessing.download_images", "global_images_folder_path")
            if config.getboolean(
                "postprocessing.download_images", "use_global_images_folder"
            )
            else os.path.join(self.artifact_folder_path, "images")
        )
        pathlib.Path(self.thread_images_folder_path).mkdir(parents=True, exist_ok=True)

    def save_image(self, file_name: str, image_binary: bytes) -> None:
        with open(os.path.join(self.thread_images_folder_path, file_name), "wb+") as f:
            f.write(image_binary)
