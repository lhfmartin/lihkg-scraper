from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import config

opt = Options()
opt.add_experimental_option(
    "debuggerAddress", config["chrome_driver"]["debugger_address"]
)
opt.set_capability("goog:loggingPrefs", {"performance": "ALL"})
chrome_driver = webdriver.Chrome(options=opt)
