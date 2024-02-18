import os
import pathlib

from .Dao import Dao


class ImageDao(Dao):
    def __init__(self, output_folder_path: str, thread_id: str, scrape_time_str: str):
        super().__init__(output_folder_path, thread_id, scrape_time_str)
        self.thread_images_folder_path = os.path.join(self.thread_folder_path, "images")
        pathlib.Path(self.thread_images_folder_path).mkdir(parents=True, exist_ok=True)

    def save_image(self, file_name: str, image_binary: bytes) -> None:
        with open(os.path.join(self.thread_images_folder_path, file_name), "wb+") as f:
            f.write(image_binary)
