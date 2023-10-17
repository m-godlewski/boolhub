"""
Unit test of gatherer module.
"""

import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from unittest import TestCase

from scripts.gatherer import Network, Air
from scripts.models.data import DeviceData


class TestGatherer(TestCase):

    # mac address regex pattern
    MAC_ADDRESS_REGEX = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"

    # region NETWORK

    def test_network_gather_network_data(self):
        # calls arp scan
        network_gatherer = Network()
        arp_scan_results = network_gatherer._Network__arp_scan()
        # checks if returned dataset is not empty
        self.assertTrue(arp_scan_results)
        # calls tested method
        output_data = network_gatherer._Network__gather_network_data(data=arp_scan_results)
        # checks if tested method returned True
        self.assertTrue(output_data)

    def test_network_arp_scan(self):
        # calling tested method
        network_gatherer = Network()
        output_data = network_gatherer._Network__arp_scan()
        # checks if returned dataset is not empty
        self.assertTrue(output_data)
        # iterate over set and checks if returned addresses
        # has correct format
        for address in output_data:
            self.assertTrue(re.match(self.MAC_ADDRESS_REGEX, address))

    # endregion

    # region AIR

    def test_air_gather_air_data(self):
        """
        # calls air scan
        air_gatherer = Air()
        air_scan_results = air_gatherer._Air__air_scan()
        # checks if returned dataset is not empty
        self.assertTrue(air_scan_results)
        # calls tested method
        output_data = air_gatherer.gather_air_data(air_data=air_scan_results)
        # checks if tested method returned True
        self.assertTrue(output_data)
        """
        pass

    def test_air_scan(self):
        """
        # calls tested method
        air_gatherer = Air()
        air_scan_results = air_gatherer._Air__air_scan()
        """
        pass

    def test_air_scan_purifier(self):
        pass

    def test_air_scan_monitor(self):
        pass

    def test_air_devices_data(self):
        # calls tested method
        air_gatherer = Air()
        output_data = air_gatherer._Air__get_air_devices()
        # checks if method returned not empty array with dictionaries inside
        self.assertTrue(output_data)
        self.assertTrue(isinstance(output_data, list))
        for data in output_data:
            self.assertTrue(isinstance(data, DeviceData))

    # endregion
