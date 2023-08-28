"""
Unit test of sentry module.
"""

import os
import sys
from typing import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from unittest import TestCase
from randmac import RandMac

from scripts.sentry import Sentry


class TestSentry(TestCase):
    """Sentry module test class."""

    def test_network_overload(self):
        """"""
        pass

    def test_network_unknown_device(self):
        """"""
        pass

    def __generate_random_mac_addresses(self, n: int = 1) -> Set[str]:
        """Generate and returns set of mac addresses, 
        where length of set is defined by argument."""
        return set(RandMac() for i in range(n))
