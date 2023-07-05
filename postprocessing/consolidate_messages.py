def consolidate_messages(page_dao, thread_dao):
    page_numbers = page_dao.get_available_page_numbers()

    all_messages = []
    for page_number in page_numbers:
        page = page_dao.load_page(page_number)
        messages = page["response"]["item_data"]
        all_messages += messages

    if all_messages[0]["msg_num"] == "1":
        topic = thread_dao.load_topic()
        like_count, dislike_count = topic["like_count"], topic["dislike_count"]
        all_messages[0]["like_count"] = str(like_count)
        all_messages[0]["dislike_count"] = str(dislike_count)
        all_messages[0]["vote_score"] = str(like_count - dislike_count)

    thread_dao.save_messages(all_messages)

    return all_messages
