if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--thread", "-t", required=True)
    parser.add_argument("--output-folder", "-o", required=False)
    args = parser.parse_args()
    thread = args.thread
    output_folder = args.output_folder
    if output_folder is None:
        output_folder = "."
    output_folder = os.path.join(output_folder, thread)

    import json
    import pathlib

    import scrapers

    pages = scrapers.scrape_thread(thread, True)

    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

    for i, x in enumerate(pages):
        with open(os.path.join(output_folder, f"page_{i + 1}.json"), "w+") as f:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
