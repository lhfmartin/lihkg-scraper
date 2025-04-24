import configparser

config = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))
config.read(["config/config.default.ini", "config/config.ini"])
