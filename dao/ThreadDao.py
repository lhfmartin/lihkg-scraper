import json
import os

from .Dao import Dao


class ThreadDao(Dao):
    def __init__(self, output_folder_path, thread_id, scrape_time_str):
        super().__init__(output_folder_path, thread_id, scrape_time_str)

    def save_topic(self, thread_data):
        with open(os.path.join(self.thread_folder_path, "topic.json"), "w+") as f:
            f.write(json.dumps(thread_data, ensure_ascii=False) + "\n")

    def save_messages(self, messages):
        with open(os.path.join(self.thread_folder_path, "messages.json"), "w+") as f:
            f.write(json.dumps(messages, ensure_ascii=False) + "\n")

    def load_messages(self):
        with open(os.path.join(self.thread_folder_path, "messages.json"), "r") as f:
            messages = f.read()
        return messages

    def save_image_mappings(self, image_mappings):
        with open(os.path.join(self.thread_folder_path, "images.json"), "w+") as f:
            f.write(json.dumps(image_mappings, ensure_ascii=False) + "\n")
