from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import config

opt = Options()
opt.add_experimental_option(
    "debuggerAddress", config["chrome_driver"]["debugger_address"]
)
opt.set_capability("goog:loggingPrefs", {"performance": "ALL"})

service = None
if len(config["chrome_driver"]["executable_path"]) > 0:
    service = Service(executable_path=config["chrome_driver"]["executable_path"])

chrome_driver = webdriver.Chrome(options=opt, service=service)
