if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(allow_abbrev=False)

    scrape_from_args_group = parser.add_mutually_exclusive_group(required=True)
    scrape_from_args_group.add_argument("-t", "--thread")
    scrape_from_args_group.add_argument("-l", "--left-panel")

    scrape_thread_args_group = parser.add_argument_group(
        "Extra arguments for scraping thread"
    )
    scrape_thread_args_group.add_argument("-p", "--pages", required=False)

    scrape_left_panel_args_group = parser.add_argument_group(
        "Extra arguments for scraping left panel"
    )
    scrape_left_panel_args_group.add_argument(
        "--max-number-of-topics", required=False, type=int, default=5
    )

    universal_args_group = parser.add_argument_group("Universal arguments")
    universal_args_group.add_argument(
        "-o", "--output-folder", required=False, default="./output"
    )
    universal_args_group.add_argument(
        "--remove-me", required=False, action="store_true"
    )

    args = parser.parse_args()
    thread_id = args.thread
    page_numbers = args.pages
    left_panel_url = args.left_panel
    max_number_of_topics = args.max_number_of_topics
    output_folder_path = args.output_folder
    remove_me = args.remove_me

    import scraping.workflows

    if thread_id is not None:
        scraping.workflows.scrape_thread(
            thread_id, page_numbers, output_folder_path, remove_me
        )
    elif left_panel_url is not None:
        scraping.workflows.scrape_left_panel(
            left_panel_url, max_number_of_topics, output_folder_path, remove_me
        )
