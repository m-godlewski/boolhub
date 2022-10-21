"""
Script responsible for sending messages and notification to system administrator.
"""

import requests


class Messenger:
    """This class is responsible for communication between server and users."""

    # local address of ntfy server
    NTFY_SERVER_URL = "https://ntfy.sh/boolhub"

    @classmethod
    def send_notification(self, text: str):
        """Send notification to ntfy server with predefined subject
        and string received by argument as notification content."""
        requests.post(url=self.NTFY_SERVER_URL, data=text.encode("utf-8"))
