"""
Unit test of gatherer module.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from unittest import TestCase

from scripts.gatherer import Network, Air


class TestGatherer(TestCase):
    """Gatherer module test class."""

    def test_network_arp_scan(self):
        """"""
        network_gatherer = Network()
        output_data = network_gatherer._Network__arp_scan()
        print(output_data)
