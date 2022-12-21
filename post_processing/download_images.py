import json
import logging
import re
import requests
import uuid


logger = logging.getLogger("lihkg-scraper")


def download_images(thread_dao, image_dao):
    messages = thread_dao.load_messages()

    urls = re.findall(
        r"(?:src|href)=\\\"(.*?)\\\"", json.dumps(messages, ensure_ascii=False)
    )
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
            logger.debug(f"Failed to download {x}")
            images_downloads["failed_to_download"].append(x)
            continue

        if (
            "image/" in response.headers["Content-Type"]
            and x not in images_downloads["downloaded"]
        ):
            file_format = response.headers["Content-Type"][6:]
            image_new_file_name = f"{uuid.uuid4().hex}.{file_format}"

            images_downloads["downloaded"][x] = image_dao.save_image(
                image_new_file_name, response.content
            )
            logger.debug(f"Downloaded {x} successfully")

    thread_dao.save_image_mappings(images_downloads)

    return images_downloads
