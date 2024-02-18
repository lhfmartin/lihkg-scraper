import os
import pathlib


class Dao:
    def __init__(self, output_folder_path: str, thread_id: str, scrape_time_str: str):
        self.thread_folder_path = os.path.join(
            output_folder_path, f"thread_{thread_id}_{scrape_time_str}"
        )
        pathlib.Path(self.thread_folder_path).mkdir(parents=True, exist_ok=True)
