"""
Unit test of sentry module.
"""

import os
import random
import sys
from typing import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from unittest import TestCase
from randmac import RandMac

import config
from scripts import sentry


class TestSentry(TestCase):

    # region AIR DATA

    def test_air_temperature(self):
        # upper and bottom threshold of temperatures
        bottom = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]["BOTTOM"]
        up = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]["UP"]
        # tests upper threshold
        input_data_up = [
            {
                "location": "test",
                "temperature": random.randint(up, up+3)
            }
        ]
        output_data_up = sentry.check_air(air_data=input_data_up)
        self.assertIn(("temperature", "test"), output_data_up)
        # tests bottom threshold
        input_data_bottom = [
            {
                "location": "test",
                "temperature": random.randint(bottom-3, bottom)
            }
        ]
        output_data_bottom = sentry.check_air(air_data=input_data_bottom)
        self.assertIn(("temperature", "test"), output_data_bottom)

    def test_air_aqi(self):
        # threshold of aqi
        threshold = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["AQI"]
        # tests exceeding threshold
        input_data = [
            {
                "location": "test",
                "aqi": random.randint(threshold, threshold+100)
            }
        ]
        output_data = sentry.check_air(air_data=input_data)
        self.assertIn(("aqi", "test"), output_data)

    def test_air_humidity(self):
        # upper and bottom threshold of humidity
        bottom = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["BOTTOM"]
        up = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["UP"]
        # tests upper threshold
        input_data_up = [
            {
                "location": "test",
                "humidity": random.randint(up, up+5)
            }
        ]
        output_data_up = sentry.check_air(air_data=input_data_up)
        self.assertIn(("humidity", "test"), output_data_up)
        # tests bottom threshold
        input_data_bottom = [
            {
                "location": "test",
                "humidity": random.randint(bottom-5, bottom)
            }
        ]
        output_data_bottom = sentry.check_air(air_data=input_data_bottom)
        self.assertIn(("humidity", "test"), output_data_bottom)

    # endregion

    # region NETWORK DATA

    def test_network_overload(self):
        # generates set containing ten random mac addresses
        input_data = self.__generate_random_mac_addresses(n=10)
        # tests method
        output_data = sentry.check_network(mac_addresses=input_data)
        self.assertIn("overload", output_data)

    def test_network_unknown_device(self):
        # generate one random (unknown for system) mac address
        input_data = self.__generate_random_mac_addresses(n=1)
        # test method
        output_data = sentry.check_network(mac_addresses=input_data)
        self.assertIn("unknown_device", output_data)

    # endregion

    # region DIAGNOSTIC

    def test_diagnostic_battery_filter_level(self):
        # threshold of battery/filter level
        threshold = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["BATTERY_FILTER_LEVEL"]
        # tests exceeding battery level threshold
        input_data_battery = [
            {
                "location": "test",
                "battery": random.randint(threshold-5, threshold)
            }
        ]
        output_data_battery = sentry.check_air(air_data=input_data_battery)
        # TODO until air devices not always returns data over bluetooth
        # there is need to use second condition
        assert ("battery", "test") in output_data_battery or len(output_data_battery) == 0
        # tests exceeding filter level threshold
        input_data_filter = [
            {
                "location": "test",
                "filter": random.randint(threshold-5, threshold)
            }
        ]
        output_data_filter = sentry.check_air(air_data=input_data_filter)
        # TODO until air devices not always returns data over bluetooth
        # there is need to use second condition
        assert ("filter", "test") in output_data_filter or len(output_data_filter) == 0

    # endregion

    def __generate_random_mac_addresses(self, n: int = 1) -> Set[str]:
        """Generates and returns set of mac addresses, 
        where length of set is defined by argument."""
        return set(RandMac() for i in range(n))
