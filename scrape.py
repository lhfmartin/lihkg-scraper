if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread", required=True)
    parser.add_argument("-p", "--page", required=False)
    parser.add_argument("-o", "--output-folder", required=False)
    args = parser.parse_args()
    thread = args.thread
    page = args.page
    output_folder = args.output_folder

    import os
    import json
    import pathlib

    import scrapers

    if output_folder is None:
        output_folder = "."
    output_folder = os.path.join(output_folder, thread)

    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

    if page is None:
        for page_number, thread_page in scrapers.scrape_thread(thread, True):
            with open(os.path.join(output_folder, f"page_{page_number}.json"), "w+") as f:
                f.write(json.dumps(thread_page, ensure_ascii=False) + "\n")
    else:
        thread_page = scrapers.scrape_page(thread, page, True)
        with open(os.path.join(output_folder, f"page_{page}.json"), "w+") as f:
            f.write(json.dumps(thread_page, ensure_ascii=False) + "\n")
       