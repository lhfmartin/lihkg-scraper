import configparser

config = configparser.ConfigParser()
config.read(["config/config.default.ini", "config/config.ini"])
