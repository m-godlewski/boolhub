"""
Messenger module is used for communication with users.
"""

import config
import logging

import requests


class Messenger:
    """This class contains methods that are used to sending notifications to 'ntfy' mobile application."""

    @classmethod
    def send_notification(self, text: str) -> None:
        """Sends notification to 'ntfy' app server with predefined subject
        and string received by argument as notification content."""
        response = requests.post(
            url=config.SCRIPTS["MESSENGER"]["NTFY_SERVER_URL"],
            data=text.encode("utf-8"),
        )
        logging.debug(
            f"MESSENGER | NOTIFICATION SENDING RESPONSE CODE = {response.status_code}"
        )
