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
        """Tests if network overload is properly handled by sentry module."""
        # generate set containing ten random mac addresses
        input_data = self.__generate_random_mac_addresses(n=10)
        # test method
        result = Sentry.check_network(mac_addresses=input_data)
        assert "overload" in result

    def test_network_unknown_device(self):
        """Tests if unknown device connected to local network is detected by sentry module."""
        # generate one random (unknown for system) mac address
        input_data = self.__generate_random_mac_addresses(n=1)
        # test method
        result = Sentry.check_network(mac_addresses=input_data)
        assert "unknown_device" in result

    def __generate_random_mac_addresses(self, n: int = 1) -> Set[str]:
        """Generate and returns set of mac addresses, 
        where length of set is defined by argument."""
        return set(RandMac() for i in range(n))
