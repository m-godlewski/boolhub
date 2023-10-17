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
from scripts.models.data import DeviceData, AirData, MiAirPurifier3HData, MiMonitor2Data


class TestSentry(TestCase):

    # region AIR DATA

    def test_air_temperature(self):
        # upper and bottom threshold of temperatures
        bottom = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]["BOTTOM"]
        up = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]["UP"]
        # generate test dataclass instance
        test_instance = self.__generate_test_instance_air_data()
        # tests upper threshold
        test_instance.temperature = random.randint(up, up+3)
        output_data = sentry.check_air(air_data=[test_instance])
        self.assertIn(("temperature", "test"), output_data)
        # tests bottom threshold
        test_instance.temperature = random.randint(bottom-3, bottom)
        output_data = sentry.check_air(air_data=[test_instance])
        self.assertIn(("temperature", "test"), output_data)

    def test_air_aqi(self):
        # threshold of aqi
        threshold = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["AQI"]
        # generate test dataclass instance
        test_instance = self.__generate_test_instance_air_data()
        # tests exceeding threshold
        test_instance.aqi = random.randint(threshold, threshold+100)
        output_data = sentry.check_air(air_data=[test_instance])
        self.assertIn(("aqi", "test"), output_data)

    def test_air_humidity(self):
        # upper and bottom threshold of humidity
        bottom = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["BOTTOM"]
        up = config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["UP"]
        # generate test dataclass instance
        test_instance = self.__generate_test_instance_air_data()
        # tests upper threshold
        test_instance.humidity = random.randint(up, up+5)
        output_data = sentry.check_air(air_data=[test_instance])
        self.assertIn(("humidity", "test"), output_data)
        # tests bottom threshold
        test_instance.humidity = random.randint(bottom-5, bottom)
        output_data = sentry.check_air(air_data=[test_instance])
        self.assertIn(("humidity", "test"), output_data)

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
        test_instance = self.__generate_test_instance_monitor()
        test_instance.battery = random.randint(threshold-5, threshold)
        output_data = sentry.check_diagnostic(diagnostic_data=[test_instance])
        assert ("battery", "test") in output_data
        # tests exceeding filter level threshold
        test_instance = self.__generate_test_instance_purifier()
        test_instance.filter_life_remaining = random.randint(threshold-5, threshold)
        output_data = sentry.check_diagnostic(diagnostic_data=[test_instance])
        assert ("filter_life_remaining", "test") in output_data

    # endregion

    def __generate_random_mac_addresses(self, n: int = 1) -> Set[str]:
        """Generates and returns set of mac addresses, 
        where length of set is defined by argument."""
        return set(RandMac() for i in range(n))

    def __generate_test_instance_air_data(self) -> AirData:
        """Return predefined, test instance of AirData dataclass."""
        return AirData(
            device=DeviceData(
                name="test", location="test", category="test", brand="test",
                mac_address=self.__generate_random_mac_addresses(n=1), ip_address="192.168.0.255"
            ),
        )

    def __generate_test_instance_purifier(self) -> MiAirPurifier3HData:
        """Return predefined, test instance of MiAirPurifier3HData dataclass."""
        return MiAirPurifier3HData(
            device=DeviceData(
                name="test", location="test", category="test", brand="test",
                mac_address=self.__generate_random_mac_addresses(n=1), ip_address="192.168.0.255"
            ),
        )

    def __generate_test_instance_monitor(self) -> MiMonitor2Data:
        """Return predefined, test instance of MiMonitor2Data dataclass."""
        return MiMonitor2Data(
            device=DeviceData(
                name="test", location="test", category="test", brand="test",
                mac_address=self.__generate_random_mac_addresses(n=1), ip_address="192.168.0.255"
            ),
        )
