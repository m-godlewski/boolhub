"""
Messenger module is used for communication with users.
"""

import logging
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests

from models.database import PostgreSQL


def send_notification(text: str, title: str, priority: int = 3) -> int:
    """Sends notification to 'ntfy' app server with predefined subject
    and string received by argument as notification content. Returns HTTP status code.
    """
    try:
        with PostgreSQL(settings=True) as postgresql_database:
            # current settings
            response = requests.post(
                url=f"https://ntfy.sh/{postgresql_database.settings.get('ntfy_token')}",
                data=text.encode("utf-8"),
                headers={"Title": title.encode("utf-8"), "Priority": str(priority)},
            )
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"MESSENGER | HTTP ERROR: {e}")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"MESSENGER | HTTP CONNECTION ERROR: {e}")
    except requests.exceptions.Timeout as e:
        logging.error(f"MESSENGER | HTTP TIMEOUT ERROR: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"MESSENGER | HTTP UNKNOWN ERROR: {e}")
    except:
        logging.error(f"MESSENGER | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
    else:
        return response.status_code
