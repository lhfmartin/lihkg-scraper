# lihkg-scraper

Download LIHKG threads (aka posts) and pages in json format.

The approach is selenium will connect to the local Chrome browser via [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) and "overheard" the traffic between the browser and the LIHKG server, so that the very same API response which is used to render the LIHKG web app could be seen by selenium. Image urls will be parsed at the end of the script and downloaded separately.

## Setting up

1. Install required packages using `pip3 install -r requirements.txt`
2. Install Google Chrome (if not yet installed)
3. To scrape member-only contents (eg. threads in 成人台 / 留言嘅加密部分), log in to LIHKG in Google Chrome

## Using the program

1. Quit Google Chrome if it is opened
2. Open Google Chrome with `--remote-debugging-port=9222` passed into the command line arguments.
    - The port `9222` may be changed to other available ports. Please also edit `debugger_address` in `config/config.ini` if other ports is used.
3. Run `python3 scrape.py -t <thread-id> -p <page-number> -o <output-folder>`
    - `-t <thread-id>` is required
    - `-p <page-number>` is optional, will scrape all pages in the thread if not provided
    - `-o <output-folder>` is optional, will save the output to the current directory if not provided
