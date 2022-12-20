import json
import os
import pathlib
import re

from .Dao import Dao


class PageDao(Dao):
    def __init__(self, output_folder_path, thread_id, scrape_time_str):
        super().__init__(output_folder_path, thread_id, scrape_time_str)
        self.thread_pages_raw_jsons_folder_path = os.path.join(
            self.thread_folder_path, "pages"
        )
        pathlib.Path(self.thread_pages_raw_jsons_folder_path).mkdir(
            parents=True, exist_ok=True
        )

    def save_page(self, page_number, page_data):
        with open(
            os.path.join(
                self.thread_pages_raw_jsons_folder_path, f"page_{page_number}.json"
            ),
            "w+",
        ) as f:
            json.dump(page_data, f, ensure_ascii=False)
            f.write("\n")

    def load_page(self, page_number):
        with open(
            os.path.join(
                self.thread_pages_raw_jsons_folder_path, f"page_{page_number}.json"
            ),
            "r",
        ) as f:
            page = json.load(f)
        return page

    def get_available_page_numbers(self):
        page_numbers = set()

        for x in os.listdir(self.thread_pages_raw_jsons_folder_path):
            if x.startswith("page_") and x.endswith(".json"):
                page_numbers.add(int(re.search("page_(\d+).json", x).group(1)))

        return sorted(page_numbers)
