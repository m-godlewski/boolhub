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
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"MESSENGER | HTTP ERROR:\n{e}")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"MESSENGER | HTTP CONNECTION ERROR:\n{e}")
    except requests.exceptions.Timeout as e:
        logging.error(f"MESSENGER | HTTP TIMEOUT ERROR:\n{e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"MESSENGER | HTTP UNKNOWN ERROR\n:{e}")
    except:
        logging.error(f"MESSENGER | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
    else:
        return response.status_code
