import re


def determine_left_panel_content_identifier(res_url: str, res_body: dict) -> str | None:
    left_panel_content_identifier = None

    if "lihkg.com/api_v2/thread/bookmark" in res_url:
        left_panel_content_identifier = (
            "bookmark_" + res_body["response"]["me"]["user_id"]
        )
    elif "lihkg.com/api_v2/thread/" in res_url and "cat_id=" in res_url:
        left_panel_content_identifier = "cat_" + re.search(
            "cat_id=(\d+)", res_url
        ).group(1)
    elif "lihkg.com/api_v2/user/" in res_url:
        left_panel_content_identifier = "user_" + re.search(
            "lihkg.com/api_v2/user/(\d+)/thread?", res_url
        ).group(1)

    return left_panel_content_identifier
