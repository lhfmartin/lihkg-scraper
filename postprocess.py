if __name__ == "__main__":
    from enums import PostProcessingActions

    import argparse

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("folder")
    parser.add_argument(
        "-a",
        "--actions",
        required=False,
        default=[PostProcessingActions.ALL],
        choices=[str(x) for x in PostProcessingActions],
        nargs="+",
    )
    args = parser.parse_args()
    folder = args.folder
    actions = args.actions

    from workflows import postprocess

    postprocess(folder, actions)
