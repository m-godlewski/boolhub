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
from influxdb_client import Point

import config
from scripts import sentry
from scripts.models.data import DeviceData, AirData, MiAirPurifier3HData, MiMonitor2Data
from scripts.models.database import PostgreSQL, InfluxDB
from scripts.models.device import MiAirPurifier3H, MiMonitor2


class Gatherer(ABC):
    """Base class of each other classes in this script."""

    pass


class Network(Gatherer):
    """Gathers network data from devices connected to local network."""

    # influx database bucket name
    BUCKET = "network"

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
                    point = (
                        Point("devices")
                        .tag("metric", "availability")
                        .field("mac_address", mac_address)
                    )
                    influx_database.write(
                        bucket=self.BUCKET,
                        org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                        record=point,
                    )
                # "number" tag
                # number of active devices in local network
                number_of_devices = len(data)
                # writes data to database
                point = (
                    Point("devices")
                    .tag("metric", "number")
                    .field("quantity", number_of_devices)
                )
                influx_database.write(
                    bucket=self.BUCKET,
                    org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                    record=point,
                )
                logging.info(
                    f"GATHERER | "
                    f"LOCATION = local | "
                    f"DATA = {self.BUCKET}.availability | "
                    f"VALUES = {mac_addresses} | "
                )
                logging.info(
                    f"GATHERER | "
                    f"LOCATION = local | "
                    f"DATA = {self.BUCKET}.number | "
                    f"VALUES = {number_of_devices} | "
                )
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True


class Air(Gatherer):
    """Gathers information from air devices connected to local network."""

    # influx database bucket name
    BUCKET = "air"

    def __init__(self) -> None:
        # retrieves data from each 'air' device and saves it to database
        self.gather_air_data(self.__air_scan())

    def gather_air_data(self, air_data: typing.List[dict]) -> bool:
        """Saves retrieved data from each air devices to database.
        Returns True, if saving process succeed, otherwise False."""
        try:
            # connects to influx database
            with InfluxDB() as influx_database:
                # iterates over datasets
                for data in air_data:
                    # data location
                    location = data.device.location
                    # air quality
                    aqi = data.aqi if hasattr(data, "aqi") else None
                    # air humidity
                    humidity = data.humidity
                    # air temperature
                    temperature = data.temperature
                    # prepares data for saving into influx database
                    point = (
                        Point("air")
                        .tag("room", location)
                        .field("aqi", aqi)
                        .field("humidity", humidity)
                        .field("temperature", temperature)
                    )
                    # inserts data to influx database
                    influx_database.write(
                        bucket=self.BUCKET,
                        org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                        record=point,
                    )
                    logging.info(
                        f"GATHERER | "
                        f"LOCATION = {location} | "
                        f"DATA = {self.BUCKET} | "
                        f"VALUES = {aqi}, {humidity}, {temperature} | "
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
            for device_data in self.__get_air_devices():
                # name of device
                device_name = device_data.name.lower()
                # calls specific method depending on device type
                if "purifier" in device_name:
                    results.append(self.__air_scan_purifier(device_data))
                elif "monitor" in device_name:
                    results.append(self.__air_scan_monitor(device_data))
                else:
                    logging.error(f"Device '{device_name}' is not supported!")
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            # calls sentry script to verifies data
            sentry.check_air(dataset=results)
            sentry.check_diagnostic(dataset=results)
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

    def __get_air_devices(self) -> typing.List[DeviceData]:
        """Returns air devices data from database."""
        try:
            # connects to postgresql
            with PostgreSQL() as postgresql_database:
                air_devices_data = [device for device in postgresql_database.devices if device.category == "air"]
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            return air_devices_data


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
