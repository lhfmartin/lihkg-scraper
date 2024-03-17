import logging
import sys

LOG_FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"


def initialize_logger() -> None:
    logger = logging.getLogger("lihkg-scraper")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
