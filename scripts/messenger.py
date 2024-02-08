"""
Messenger module is used for communication with users.
"""

import logging
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests

from scripts.models.database import Redis


def send_notification(text: str, title: str, priority: int = 3) -> int:
    """Sends notification to 'ntfy' app server with predefined subject
    and string received by argument as notification content. Returns HTTP status code.
    """
    try:
        with Redis() as redis:
            response = requests.post(
                url=redis.ntfy_url,
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
