import json
import logging
import re
import requests
import uuid
from urllib.parse import urlparse


IMAGE_DOWNLOAD_STATUS_DOWNLOADED = "downloaded"
IMAGE_DOWNLOAD_STATUS_FAILED = "failed"

logger = logging.getLogger("lihkg-scraper")


def build_absolute_url_from_url(url):
    if bool(urlparse(url).netloc):  # url is absolute url
        return url
    return "http://lihkg.com" + ("" if url.startswith("/") else "/") + url


def download_images(thread_dao, image_dao):
    messages = thread_dao.load_messages()

    urls = re.findall(
        r"(?:src|href)=\\\"(.*?)\\\"", json.dumps(messages, ensure_ascii=False)
    )
    # The urls will also contain links in <a> tag that can link to non-images

    images_downloads = {
        IMAGE_DOWNLOAD_STATUS_DOWNLOADED: {},
        IMAGE_DOWNLOAD_STATUS_FAILED: {},
    }

    for x in urls:
        if x in images_downloads[IMAGE_DOWNLOAD_STATUS_DOWNLOADED]:
            continue

        try:
            response = requests.get(build_absolute_url_from_url(x))
        except requests.exceptions.RequestException as e:
            logger.debug(f"Failed to download {x}")
            images_downloads[IMAGE_DOWNLOAD_STATUS_FAILED][x] = str(e)
            continue

        if "image/" in response.headers["Content-Type"]:
            file_format = response.headers["Content-Type"][6:]
            image_new_file_name = f"{uuid.uuid4().hex}.{file_format}"

            images_downloads[IMAGE_DOWNLOAD_STATUS_DOWNLOADED][
                x
            ] = image_dao.save_image(image_new_file_name, response.content)
            logger.debug(f"Downloaded {x} successfully")
        else:
            logger.debug(f"The Content-Type header says {x} is not an image")

    thread_dao.save_image_mappings(images_downloads)

    return images_downloads
