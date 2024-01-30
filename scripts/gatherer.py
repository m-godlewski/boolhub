"""
This script is used for gathering data from devices connected to local network.
"""

import argparse
import copy
import logging
import os
import sys
import traceback
import typing
from abc import ABC

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from scapy.all import arping

from scripts import sentry
from scripts.models.data import (
    DeviceData,
    AirData,
    MiAirPurifier3HData,
    MiMonitor2Data,
    OutsideVirtualThermometerData,
    ForecastData,
)
from scripts.models.database import PostgreSQL, InfluxDB
from scripts.models.device import MiAirPurifier3H, MiMonitor2, OutsideVirtualThermometer


class Gatherer(ABC):
    """Base class of each other classes in this script."""

    pass


class Network(Gatherer):
    """Gathers network data from devices connected to local network."""

    def __init__(self) -> None:
        # saves gathered and processed data from arp scan to database
        self.__gather_network_data(data=self.__arp_scan())

    def __arp_scan(self) -> typing.Set[str]:
        """Performs arp scan of local network and returns set of MAC addresses."""
        try:
            # performs arp scan
            answered, unanswered = arping("192.168.0.0/24", verbose=0)
            # set of MAC addresses
            mac_addresses = set(
                destination["Ether"].src for source, destination in answered
            )
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return set()
        else:
            return mac_addresses

    def __gather_network_data(self, data: typing.Set[str]) -> bool:
        """Saves MAC addresses and number of active devices to database.
        Before data are written to database, sentry.py script is used to verify
        if there are unknown MAC addresses in received 'data' set or
        number of connected devices exceed threshold.
        Returns True, if saving process succeed, otherwise False."""
        try:
            # copying received data
            mac_addresses = copy.deepcopy(data)
            # verifies if there is a new MAC address in received list
            # or number of connected devices exceed threshold
            sentry.check_network(mac_addresses=mac_addresses)
            # connects to influx database
            with InfluxDB() as influx_database:
                # "availability" tag
                # iterates over mac addresses
                for mac_address in mac_addresses:
                    # writes single data entity to database
                    influx_database.add_point_network(
                        measurement="devices",
                        metric="availability",
                        field="mac_address",
                        value=mac_address,
                    )
                # "number" tag
                # number of active devices in local network
                number_of_devices = len(data)
                # writes data to database
                influx_database.add_point_network(
                    measurement="devices",
                    metric="number",
                    field="quantity",
                    value=number_of_devices,
                )
                logging.info(
                    f"GATHERER | "
                    f"LOCATION = local | "
                    f"DATA = network.availability | "
                    f"VALUES = {mac_addresses} | "
                )
                logging.info(
                    f"GATHERER | "
                    f"LOCATION = local | "
                    f"DATA = network.number | "
                    f"VALUES = {number_of_devices} | "
                )
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True


class Air(Gatherer):
    """Gathers information from air devices connected to local network."""

    def __init__(self) -> None:
        # retrieves data from each 'air' device and saves it to database
        self.gather_air_data(self.__air_scan())

    def gather_air_data(self, air_data: typing.List[AirData]) -> bool:
        """Saves retrieved data from each air devices to database.
        Returns True, if saving process succeed, otherwise False."""
        try:
            # connects to influx database
            with InfluxDB() as influx_database:
                # iterates over datasets
                for data in air_data:
                    # prepares data for saving into influx database
                    influx_database.add_point_air(data)
                    logging.info(
                        f"GATHERER | "
                        f"LOCATION = {data.device.location} | "
                        f"DATA = air | "
                        f"VALUES = {data.aqi}, {data.humidity}, {data.temperature} | "
                    )
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True

    def __air_scan(self) -> typing.List[AirData]:
        """Gathers air data from each device tagged as "air" in local network."""
        try:
            # list that stores air data from each device
            results = []
            # iterates over air devices data
            for device_data in PostgreSQL().get_device_by_type(device_type="air"):
                # name of device
                device_name = device_data.name.lower()
                # calls specific method depending on device type
                if "purifier" in device_name:
                    results.append(self.__air_scan_purifier(device_data))
                elif "monitor" in device_name:
                    results.append(self.__air_scan_monitor(device_data))
                elif "outside thermometer" in device_name:
                    results.append(self.__air_scan_outside_thermometer(device_data))
                else:
                    logging.error(f"Device '{device_name}' is not supported!")
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            # calls sentry script to verifies data
            sentry.check_air(results)
            sentry.check_diagnostic(results)
            return results

    def __air_scan_purifier(self, device_data: DeviceData) -> MiAirPurifier3HData:
        """Gathers data from Xiaomi Purifier device."""
        try:
            # fetches data from device
            device = MiAirPurifier3H(device_data)
            # retrieved data
            data = device.data
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __air_scan_monitor(self, device_data: DeviceData) -> MiMonitor2Data:
        """Gathers data from Xiaomi Monitor 2 device."""
        try:
            # fetches data from device
            device = MiMonitor2(device_data)
            # retrieved data
            data = device.data
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __air_scan_outside_thermometer(
        self, device_data: DeviceData
    ) -> OutsideVirtualThermometerData:
        """Gathers data from virtual outside thermometer."""
        try:
            # fetches data from device
            device = OutsideVirtualThermometer(device_data)
            # retrieved data
            data = device.data
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return {}
        else:
            return data


class Forecast(Gatherer):
    """Gathers information about weather forecast from external API."""

    def __init__(self) -> None:
        # retrieves weather forecast and saves it to database
        self.gather_forecast_data(self.__forecast_scan())

    def gather_forecast_data(self, forecast_data: typing.List[ForecastData]) -> bool:
        """Saves retrieved forecast data from virtual thermometer to database.
        Returns True, if saving process succeed, otherwise False."""
        try:
            # connects to influx database
            with InfluxDB() as influx_database:
                # iterates over datasets
                for data in forecast_data:
                    # prepares data for saving into influx database
                    influx_database.add_point_forecast(data)
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True

    def __forecast_scan(self) -> typing.List[ForecastData]:
        """Gathers weather forecast data from virtual thermometer."""
        try:
            # gets virtual thermometer device data from database
            device_data = PostgreSQL().get_device_by_name(
                device_name="Outside Thermometer"
            )
            # fetches forecast data from device
            forecast_device = OutsideVirtualThermometer(
                device_data=device_data,
                forecast=True
            )
            # retrieved data
            forecast_data = forecast_device.data
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            return forecast_data


# main section of script
if __name__ == "__main__":
    # parses script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data")
    arguments = parser.parse_args()
    # gathers data, depends on given argument
    if arguments.data == "network":
        Network()
    if arguments.data == "air":
        Air()
    if arguments.data == "forecast":
        Forecast()
