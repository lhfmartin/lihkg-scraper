def remove_logged_in_user_data_from_thread_data(thread_data):
    thread_data.pop("me", None)
    thread_data.pop("vote_status", None)
    thread_data.pop("is_bookmarked", None)
    thread_data.pop("is_replied", None)
    thread_data.pop("last_read", None)
    thread_data.pop("last_replied", None)
    thread_data.get("pinned_post", {}).pop("vote_status", None)


def remove_logged_in_user_data_from_page_data(page_data):
    page_data["response"].pop("vote_status", None)
    messages = page_data["response"]["item_data"]
    for message in messages:
        while message.pop("vote_status", None) is not None:
            message = message.get("quote", {})


def remove_logged_in_user_data(thread_dao, page_dao):
    topic = thread_dao.load_topic()
    remove_logged_in_user_data_from_thread_data(topic)
    remove_logged_in_user_data_from_thread_data(topic.get("parent_thread", {}))
    for x in topic.get("child_threads", []):
        remove_logged_in_user_data_from_thread_data(x)
    thread_dao.save_topic(topic)

    page_numbers = page_dao.get_available_page_numbers()
    for page_number in page_numbers:
        page_data = page_dao.load_page(page_number)
        remove_logged_in_user_data_from_page_data(page_data)
        page_dao.save_page(page_number, page_data)
