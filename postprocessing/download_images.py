from bs4 import BeautifulSoup
from hashlib import sha1
import logging
import re
import requests
from urllib.parse import urlparse

from dao import ThreadDao, PageDao, ImageDao
from postprocessing import consolidate_messages

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


def download_images(
    thread_dao: ThreadDao, page_dao: PageDao | None, image_dao: ImageDao
) -> dict:
    try:
        messages = thread_dao.load_messages()
    except FileNotFoundError:
        messages = consolidate_messages(page_dao, thread_dao, False)

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

    urls = list(dict.fromkeys(urls))

    for x in urls:
        if url_matches_skip_download_patterns(x):
            logger.info(f"Skipping {x} as it matches the predefined patterns to skip")
            continue

        try:
            response = session.get(
                build_absolute_url_from_url(x),
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {x} ({str(e)})")
            images_downloads[IMAGE_DOWNLOAD_STATUS_FAILED][x] = str(e)
            continue

        response_header_content_type = response.headers.get("Content-Type")
        if response_header_content_type is None:
            logger.warning(f"The Content-Type header of {x} is missing")
        elif "image/" in response_header_content_type:
            file_format = response_header_content_type[6:]
            image_new_file_name = f"{sha1(response.content).hexdigest()}.{file_format}"

            image_dao.save_image(image_new_file_name, response.content)
            images_downloads[IMAGE_DOWNLOAD_STATUS_DOWNLOADED][x] = image_new_file_name
            logger.info(f"Downloaded {x} successfully")
        else:
            logger.info(f"The Content-Type header says {x} is not an image")

    thread_dao.save_image_mappings(images_downloads)

    return images_downloads
