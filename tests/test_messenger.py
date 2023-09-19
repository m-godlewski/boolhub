"""
Unit test of messenger module.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from unittest import TestCase

from scripts import messenger


class TestMessenger(TestCase):
    """Messenger module test class."""

    def test_notification(self):
        """Sends test notification and verifies HTTP response code."""
        status_code = messenger.send_notification("PyTest message!")
        self.assertEqual(status_code, 200)
