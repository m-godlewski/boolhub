"""
Unit test of messenger module.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from unittest import TestCase

from scripts import messenger


class TestMessenger(TestCase):
    """Messenger module unit tests class."""

    def test_notification(self):
        # calls tested method
        status_code = messenger.send_notification(
            text="Lorem Ipsum", title="PyTest message!"
        )
        # checks returned http code
        self.assertEqual(status_code, 200)
