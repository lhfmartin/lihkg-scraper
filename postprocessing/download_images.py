from bs4 import BeautifulSoup
import json
import logging
import re
import requests
import uuid
from urllib.parse import urlparse

from dao import ThreadDao, ImageDao


IMAGE_DOWNLOAD_STATUS_DOWNLOADED = "downloaded"
IMAGE_DOWNLOAD_STATUS_FAILED = "failed"
URLS_TO_SKIP_DL_REGEX_LIST = [
    "^https:\/\/www\.youtube\.com\/watch\?v=",
    "^https:\/\/lihkg\.com\/thread\/",
    "^https:\/\/lih\.kg\/",
]
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}
REQUEST_TIMEOUT = 120

logger = logging.getLogger("lihkg-scraper")


def url_matches_skip_download_patterns(url: str) -> bool:
    return any(
        [
            bool(re.search(pattern, url, re.IGNORECASE))
            for pattern in URLS_TO_SKIP_DL_REGEX_LIST
        ]
    )


def build_absolute_url_from_url(url: str) -> str:
    if bool(urlparse(url).netloc):
        return url  # url is absolute url
    return "https://lihkg.com" + ("" if url.startswith("/") else "/") + url


def download_images(thread_dao: ThreadDao, image_dao: ImageDao) -> dict:
    messages = thread_dao.load_messages()

    soup = BeautifulSoup(
        "\n".join(message["msg"] for message in messages), features="html.parser"
    )

    urls = [
        element.get("src") or element.get("href")
        for element in soup.find_all(["img", "a"])
    ]
    # The urls will also contain links in <a> tag that can link to non-images

    images_downloads = {
        IMAGE_DOWNLOAD_STATUS_DOWNLOADED: {},
        IMAGE_DOWNLOAD_STATUS_FAILED: {},
    }

    session = requests.Session()

    for x in urls:
        if x in images_downloads[IMAGE_DOWNLOAD_STATUS_DOWNLOADED]:
            continue
        if url_matches_skip_download_patterns(x):
            logger.debug(f"Skipping {x} as it matches the predefined patterns to skip")
            continue

        try:
            response = session.get(
                build_absolute_url_from_url(x),
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT,
            )
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
