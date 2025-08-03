import __main__, postprocess, scrape

if __main__.__file__ == postprocess.__file__:
    from .postprocess import postprocess
elif __main__.__file__ == scrape.__file__:
    from .scrape_left_panel import scrape_left_panel
    from .scrape_thread import scrape_thread
