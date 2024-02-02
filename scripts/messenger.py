"""
Messenger module is used for communication with users.
"""

import config
import logging
import traceback

import requests


def send_notification(text: str, title: str, priority: int = 3) -> int:
    """Sends notification to 'ntfy' app server with predefined subject
    and string received by argument as notification content. Returns HTTP status code.
    """
    try:
        response = requests.post(
            url=config.SCRIPTS["MESSENGER"]["NTFY_SERVER_URL"],
            data=text.encode("utf-8"),
            headers={"Title": title.encode("utf-8"), "Priority": str(priority)},
        )
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return response.status_code
    else:
        logging.debug(
            f"MESSENGER | NOTIFICATION SENDING RESPONSE CODE = {response.status_code}"
        )
        return response.status_code
