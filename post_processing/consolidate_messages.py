def consolidate_messages(page_dao):
    page_numbers = page_dao.get_available_page_numbers()

    all_messages = []
    for page_number in sorted(page_numbers):
        page = page_dao.load_page(page_number)
        messages = page["response"]["item_data"]

        # if output_file_type == "csv":
        #     for i, x in enumerate(messages):
        #         user_data = x["user"]
        #         del messages[i]["user"]
        #         if "quote" in x:
        #             del messages[i]["quote"]
        #         messages[i] = {**messages[i], **user_data}
        all_messages += messages

    return all_messages
