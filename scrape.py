if __name__ == "__main__":
    from enums import PostProcessingActions

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
        "--post-processing-actions",
        required=False,
        default=[],
        choices=[str(x) for x in PostProcessingActions],
        nargs="+",
    )

    args = parser.parse_args()
    thread_id = args.thread
    page_numbers = args.pages
    left_panel_url = args.left_panel
    max_number_of_topics = args.max_number_of_topics
    output_folder_path = args.output_folder
    post_processing_actions = args.post_processing_actions

    from workflows.scrape_thread import scrape_thread
    from workflows.scrape_left_panel import scrape_left_panel

    if thread_id is not None:
        scrape_thread(
            thread_id, page_numbers, output_folder_path, post_processing_actions
        )
    elif left_panel_url is not None:
        scrape_left_panel(
            left_panel_url,
            max_number_of_topics,
            output_folder_path,
            post_processing_actions,
        )
