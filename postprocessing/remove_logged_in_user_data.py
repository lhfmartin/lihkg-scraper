from functools import singledispatch


from dao import ThreadDao, PageDao, TopicListDao


def _remove_logged_in_user_data_from_poster_data(poster_data: dict) -> None:
    poster_data.pop("is_following", None)
    poster_data.pop("is_blocked", None)
    poster_data.pop("is_disappear", None)


def _remove_logged_in_user_data_from_thread_data(thread_data: dict) -> None:
    thread_data.pop("me", None)
    thread_data.pop("vote_status", None)
    thread_data.pop("is_bookmarked", None)
    thread_data.pop("is_replied", None)
    thread_data.pop("last_read", None)
    thread_data.pop("last_replied", None)
    _remove_logged_in_user_data_from_poster_data(thread_data.get("user", {}))

    thread_data.get("pinned_post", {}).pop("vote_status", None)
    _remove_logged_in_user_data_from_poster_data(
        thread_data.get("pinned_post", {}).get("user", {})
    )

    if "parent_thread" in thread_data:
        _remove_logged_in_user_data_from_thread_data(thread_data["parent_thread"])

    for x in thread_data.get("child_threads", []):
        _remove_logged_in_user_data_from_thread_data(x)


def _remove_logged_in_user_data_from_messages(messages: list[dict]) -> None:
    for message in messages:
        while message.pop("vote_status", None) is not None:
            _remove_logged_in_user_data_from_poster_data(message.get("user", {}))
            message = message.get("quote", {})


def _remove_logged_in_user_data_from_page_data(page_data: dict) -> None:
    _remove_logged_in_user_data_from_thread_data(page_data["response"])

    messages = page_data["response"]["item_data"]
    _remove_logged_in_user_data_from_messages(messages)


@singledispatch
def remove_logged_in_user_data() -> None:
    pass


@remove_logged_in_user_data.register
def _remove_logged_in_user_data(thread_dao: ThreadDao, page_dao: PageDao) -> None:
    topic = thread_dao.load_topic()
    _remove_logged_in_user_data_from_thread_data(topic)
    thread_dao.save_topic(topic)

    page_numbers = page_dao.get_available_page_numbers()
    for page_number in page_numbers:
        page_data = page_dao.load_page(page_number)
        _remove_logged_in_user_data_from_page_data(page_data)
        page_dao.save_page(page_number, page_data)

    try:
        messages = thread_dao.load_messages()
        _remove_logged_in_user_data_from_messages(messages)
        thread_dao.save_messages(messages)
    except FileNotFoundError:
        pass


@remove_logged_in_user_data.register
def _remove_logged_in_user_data(topic_list_dao: TopicListDao) -> None:
    topic_list = topic_list_dao.load_topic_list()
    for topic in topic_list:
        _remove_logged_in_user_data_from_thread_data(topic)
    topic_list_dao.save_topic_list(topic_list)
