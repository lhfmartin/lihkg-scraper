import json
import os

from .Dao import Dao


class ThreadDao(Dao):
    def __init__(self, output_folder_path, thread_id, scrape_time_str):
        super().__init__(output_folder_path, thread_id, scrape_time_str)

    def save_topic(self, thread_data):
        with open(os.path.join(self.thread_folder_path, "topic.json"), "w+") as f:
            json.dump(thread_data, f, ensure_ascii=False)
            f.write("\n")

    def load_topic(self):
        with open(os.path.join(self.thread_folder_path, "topic.json"), "r") as f:
            topic = json.load(f)
        return topic

    def save_messages(self, messages, output_file_type="json"):
        if output_file_type == "csv":  # Not supported currently
            import pandas as pd

            pd.DataFrame(messages).set_index("msg_num").to_csv(
                os.path.join(self.thread_folder_path, "messages.csv")
            )
        elif output_file_type == "json":
            with open(
                os.path.join(self.thread_folder_path, "messages.json"), "w+"
            ) as f:
                json.dump(messages, f, ensure_ascii=False)
                f.write("\n")

    def load_messages(self):
        with open(os.path.join(self.thread_folder_path, "messages.json"), "r") as f:
            messages = json.load(f)
        return messages

    def save_image_mappings(self, image_mappings):
        with open(os.path.join(self.thread_folder_path, "images.json"), "w+") as f:
            json.dump(image_mappings, f, ensure_ascii=False)
            f.write("\n")
