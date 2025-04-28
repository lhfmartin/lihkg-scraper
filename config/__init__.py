import configparser
import pathlib

config = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))
config.read(
    [
        pathlib.Path(__file__).absolute().parent / "config.default.ini",
        pathlib.Path(__file__).absolute().parent / "config.ini",
    ]
)
