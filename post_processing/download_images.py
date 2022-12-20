import json
import os
import pathlib
import re
import requests
import uuid


def download_images(thread_dao, image_dao):
    messages = thread_dao.load_messages()

    urls = re.findall(r"(?:src|href)=\\\"(.*?)\\\"", messages)
    urls = [
        url
        if url.startswith("http")
        else "http://lihkg.com" + ("" if url.startswith("/") else "/") + url
        for url in urls
    ]
    # The urls will also contain links in <a> tag that can link to non-images

    images_downloads = {
        "downloaded": {},
        "failed_to_download": [],
    }

    for i, x in enumerate(urls):
        try:
            response = requests.get(x)
        except Exception:
            images_downloads["failed_to_download"].append(x)
            continue

        if (
            "image/" in response.headers["Content-Type"]
            and x not in images_downloads["downloaded"]
        ):
            file_format = response.headers["Content-Type"][6:]
            image_new_file_name = f"{uuid.uuid4().hex}.{file_format}"
            image_dao.save_image(image_new_file_name, response.content)

            images_downloads["downloaded"][x] = image_new_file_name

    thread_dao.save_image_mappings(images_downloads)
