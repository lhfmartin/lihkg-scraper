import json
import os
import re
import sys


def consolidate_messages(thread_folder_path):
    thread_pages_raw_jsons_folder_path = os.path.join(thread_folder_path, "pages")

    # if output_file_type not in ("csv", "json"):
    #     raise ValueError("Output file type should be either csv or json")

    page_numbers = set()

    for x in os.listdir(thread_pages_raw_jsons_folder_path):
        if x.startswith("page_") and x.endswith(".json"):
            page_numbers.add(re.search("page_(\d+).json", x).group(1))

    all_messages = []
    for page_number in sorted(page_numbers):
        with open(
            os.path.join(
                thread_pages_raw_jsons_folder_path, f"page_{page_number}.json"
            ),
            "r",
        ) as f:
            messages = json.loads(f.read())["response"]["item_data"]

        # if output_file_type == "csv":
        #     for i, x in enumerate(messages):
        #         user_data = x["user"]
        #         del messages[i]["user"]
        #         if "quote" in x:
        #             del messages[i]["quote"]
        #         messages[i] = {**messages[i], **user_data}
        all_messages += messages

    return all_messages
