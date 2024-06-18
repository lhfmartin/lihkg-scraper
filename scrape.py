if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-t", "--thread", required=True)
    parser.add_argument("-p", "--pages", required=False)
    parser.add_argument("-o", "--output-folder", required=False, default="./output")
    parser.add_argument("--remove-me", required=False, action="store_true")
    args = parser.parse_args()
    thread_id = args.thread
    page_numbers = args.pages
    output_folder_path = args.output_folder
    remove_me = args.remove_me

    import scrapers.workflows

    scrapers.workflows.scrape_thread(
        thread_id, page_numbers, output_folder_path, remove_me
    )
