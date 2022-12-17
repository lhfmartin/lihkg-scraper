from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import config

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

opt = Options()
opt.add_experimental_option(
    "debuggerAddress", config["chrome_driver"]["debugger_address"]
)
chrome_driver = webdriver.Chrome(desired_capabilities=capabilities, options=opt)
