# lihkg-scraper

Download LIHKG threads (aka posts) and pages in json format.

## Using the program

1. Quit Google Chrome if it is opened
2. Open Google Chrome with `--remote-debugging-port=9222` passed into the command line arguments.
    a. The port `9222` may be changed to other available ports. Please also edit `debugger_address` in `config/config.ini` if other ports is used.
3. Run `python3 scrape_thread.py -t <thread-id> -o <output-folder>`, all pages in the thread will be saved inside `<output-folder>/<thread-id>`
