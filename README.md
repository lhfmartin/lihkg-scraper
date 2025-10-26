# lihkg-scraper

Download LIHKG threads (aka posts) and pages in json format.

The approach is selenium will connect to the local Chrome browser via [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) and "overheard" the traffic between the browser and the LIHKG server, so that the very same API response which is used to render the LIHKG web app could be seen by selenium.

## Setting up

1. Install required packages using `pip install -r requirements.txt`
2. Install Google Chrome (if not yet installed)
3. *(Optional)* To scrape member-only contents (eg. threads in 成人台 / 留言嘅加密部分), log in to LIHKG in Google Chrome
4. *(Optional)* To override the default config properties defined in `./config/config.default.ini`, create a copy of it and rename the new file to `./config/config.ini`, and edit the values in the new file

## Using the program

1. Quit Google Chrome if it is opened
2. Open Google Chrome with `--remote-debugging-port=9222` passed into the command line arguments.
    - The port `9222` may be changed to other available ports. Please also edit `debugger_address` in the config file if another port is used
3. Run the program
    - To scrape a thread, run `python scrape.py -t <thread-id> [-p <page-numbers>] [-o <output-folder>] [--post-processing-actions <post-processing-actions>]`
        - `-t <thread-id>` is required
        - `-p <page-numbers>` is optional, will scrape all pages in the thread if not provided\
        Examples: `-p 1` / `-p 1-5,8,11-13`
        - `-o <output-folder>` is optional, will save the output to `./output` if not provided
        - `--post-processing-actions <post-processing-actions>` is optional. If provided, will run the specified function(s) in the post-processing stage. When scraping a thread, these post-processing actions are supported: `all`, `remove_me`, `consolidate_messages`, `download_images`
    - To scrape a page's left panel, run `python scrape.py -l <url-to-page-with-left-panel> [--max-number-of-topics <max-number-of-topics>] [-o <output-folder>] [--post-processing-actions <post-processing-actions>]`
        - `-l <url-to-page-with-left-panel>` is required
        - `--max-number-of-topics <max-number-of-topics>` is optional, defaults to 5 if not provided
        - `-o <output-folder>` is optional, will save the output to `./output` if not provided
        - `--post-processing-actions <post-processing-actions>` is optional. If provided, will run the specified function(s) in the post-processing stage. When scraping a page's left panel, these post-processing actions are supported: `all`, `remove_me`

## Viewing the output

To view a scraped thread (scraped with argument `--post-processing-actions all` or `--post-processing-actions consolidate_messages`) in a human-readable manner, use the web app [LIHKG Snapshot Viewer](https://lhfmartin.github.io/lihkg-snapshot-viewer/) (repository: [lihkg-snapshot-viewer](https://github.com/lhfmartin/lihkg-snapshot-viewer))
