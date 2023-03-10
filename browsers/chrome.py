import atexit
from playwright.sync_api import sync_playwright

from config import config

playwright = sync_playwright().start()
chrome = playwright.chromium.connect_over_cdp(
    "http://" + config["chrome_driver"]["debugger_address"]
)
chrome = chrome.contexts[0]


@atexit.register
def stop_playwright():
    chrome.close()
    playwright.stop()
