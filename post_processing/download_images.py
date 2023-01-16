import json
import logging
import re
import requests
import uuid
from urllib.parse import urlparse


IMAGE_DOWNLOAD_STATUS_DOWNLOADED = "downloaded"
IMAGE_DOWNLOAD_STATUS_FAILED = "failed"
URLS_TO_SKIP_DL_REGEX_LIST = [
    "^https:\/\/www\.youtube\.com\/watch\?v=",
    "^https:\/\/i\.lih\.kg\/thumbnail",
]

logger = logging.getLogger("lihkg-scraper")


def url_matches_skip_download_patterns(url):
    return any(
        [
            bool(re.search(pattern, url, re.IGNORECASE))
            for pattern in URLS_TO_SKIP_DL_REGEX_LIST
        ]
    )


def build_absolute_url_from_url(url):
    if bool(urlparse(url).netloc):
        return url  # url is absolute url
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
        if url_matches_skip_download_patterns(x):
            logger.debug(f"Skipping {x} as it matches the predefined patterns to skip")
            continue

        try:
            response = requests.get(build_absolute_url_from_url(x))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.debug(f"Failed to download {x}")
            images_downloads[IMAGE_DOWNLOAD_STATUS_FAILED][x] = str(e)
            continue

        response_content_type = response.headers.get("Content-Type")
        if response_content_type is None:
            logger.debug(f"The Content-Type header of {x} is missing")
        elif "image/" in response_content_type:
            file_format = response_content_type[6:]
            image_new_file_name = f"{uuid.uuid4().hex}.{file_format}"

            image_dao.save_image(image_new_file_name, response.content)
            images_downloads[IMAGE_DOWNLOAD_STATUS_DOWNLOADED][x] = image_new_file_name
            logger.debug(f"Downloaded {x} successfully")
        else:
            logger.debug(f"The Content-Type header says {x} is not an image")

    thread_dao.save_image_mappings(images_downloads)

    return images_downloads
