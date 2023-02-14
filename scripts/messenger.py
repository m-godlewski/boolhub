"""
Messenger module is used for communication with users.
"""

import logging

import requests


class Messenger:
    """This class contains methods that are used in sending notifications
    to 'ntfy' application in local network."""

    # local address of ntfy server
    NTFY_SERVER_URL = "https://ntfy.sh/boolhub"

    @classmethod
    def send_notification(self, text: str) -> None:
        """Sends notification to 'ntfy' app server with predefined subject
        and string received by argument as notification content."""
        response = requests.post(url=self.NTFY_SERVER_URL, data=text.encode("utf-8"))
        logging.debug(f"MESSENGER | NOTIFICATION SENDING RESPONSE CODE = {response.status_code}")
