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
from abc import ABC, abstractmethod

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from scapy.all import arping

import sentry
from models.data import (
    DeviceData,
    AirData,
    MiAirPurifier3HData,
    MiMonitor2Data,
)
from models.database import PostgreSQL, InfluxDB
from models.device import MiAirPurifier3H, MiMonitor2


class Gatherer(ABC):
    """Base class of each other classes in this script."""

    def __init__(self) -> None:
        """Initializes object by calling save method that takes the result of scan method as an argument."""
        self.save(self.scan())

    @abstractmethod
    def save(self, data: typing.Set[str]) -> bool:
        """Should implements the logic of saving data to databases.
        Also, should call Sentry module for verifying data.
        """
        return

    @abstractmethod
    def scan(self) -> typing.Any:
        """Should implements the logic of fetching data from devices."""
        return


class Network(Gatherer):
    """Gathers network data from devices connected to a local network."""

    def scan(self) -> typing.Set[str]:
        """Performs arp scan of local network and returns set of MAC addresses."""
        try:
            logging.debug("GATHERER | NETWORK | Scan started")
            # performs arp scan
            answered, unanswered = arping("192.168.0.0/24", verbose=0)
            # set of MAC addresses
            mac_addresses = set(
                destination["Ether"].src for source, destination in answered
            )
        except Exception:
            logging.error(f"GATHERER | NETWORK\n{traceback.format_exc()}")
            return set()
        else:
            logging.debug("GATHERER | NETWORK | Scan completed")
            return mac_addresses

    def save(self, data: typing.Set[str]) -> bool:
        """Saves MAC addresses and number of active devices to database.
        Before data are written to database, sentry.py script is used to verify
        if there are unknown MAC addresses in received 'data' set or
        number of connected devices exceed threshold.
        Returns True, if saving process succeed, otherwise False."""
        try:
            logging.debug("GATHERER | NETWORK | Data saving")
            # copying received data
            mac_addresses = copy.deepcopy(data)
            # verifies if there is a new MAC address in received set
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
            logging.error(f"GATHERER | NETWORK\n{traceback.format_exc()}")
            return False
        else:
            logging.debug("GATHERER | NETWORK | Data saved")
            return True


class Air(Gatherer):
    """Gathers information from air devices connected to local network."""

    def scan(self) -> typing.Set[AirData]:
        """Gathers air data from each device tagged as "air"."""
        try:
            logging.debug("GATHERER | AIR | Scan started")
            # set that stores air data from each device
            results = set()
            with PostgreSQL() as postgresql:
                # iterates over air devices data
                for device_data in postgresql.get_device_by_type("air"):
                    # name of device
                    device_name = device_data.name.lower()
                    # calls specific method depending on device type
                    if "purifier" in device_name:
                        results.add(self.__scan_purifier(device_data))
                    elif "monitor" in device_name:
                        results.add(self.__scan_monitor(device_data))
                    else:
                        logging.error(f"Device '{device_name}' is not supported!")
        except Exception:
            logging.error(f"GATHERER | AIR\n{traceback.format_exc()}")
            return results
        else:
            # calls sentry script to verifies data
            sentry.check_air(results)
            sentry.check_diagnostic(results)
            logging.debug("GATHERER | AIR | Scan completed")
            return results

    def save(self, air_data: typing.Set[AirData]) -> bool:
        """Saves retrieved data from each air devices to database.
        Returns True, if saving process succeed, otherwise False."""
        try:
            logging.debug("GATHERER | AIR | Data saving")
            # connects to influx database
            with InfluxDB() as influx_database:
                # iterates over datasets
                for data in air_data:
                    # prepares data for saving into influx database
                    influx_database.add_point_health(data)
                    logging.info(
                        f"GATHERER | "
                        f"LOCATION = {data.device.location} | "
                        f"DATA = health | "
                        f"VALUES = {data.health_data_indicator} | "
                    )
                    influx_database.add_point_air(data)
                    logging.info(
                        f"GATHERER | "
                        f"LOCATION = {data.device.location} | "
                        f"DATA = air | "
                        f"VALUES = AQI: {data.aqi}, HUMIDITY: {data.humidity}, TEMPERATURE: {data.temperature} | "
                    )
        except Exception:
            logging.error(f"GATHERER | AIR\n{traceback.format_exc()}")
            return False
        else:
            logging.debug("GATHERER | AIR | Data saved")
            return True

    def __scan_purifier(self, device_data: DeviceData) -> MiAirPurifier3HData:
        """Gathers data from Xiaomi Purifier device."""
        try:
            # fetches data from device
            device = MiAirPurifier3H(device_data)
            # retrieved data
            data = device.data
        except Exception:
            logging.error(f"GATHERER | AIR\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __scan_monitor(self, device_data: DeviceData) -> MiMonitor2Data:
        """Gathers data from Xiaomi Monitor 2 device."""
        try:
            # fetches data from device
            device = MiMonitor2(device_data)
            # retrieved data
            data = device.data
        except Exception:
            logging.error(f"GATHERER | AIR\n{traceback.format_exc()}")
            return {}
        else:
            return data


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
