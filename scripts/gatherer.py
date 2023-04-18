"""
Gatherer script is used for gathering data from devices connected to local network.
"""

import argparse
import copy
import logging
import os
import sys
import traceback
from abc import ABC
from datetime import datetime
from typing import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import influxdb_client
import sqlite3
from influxdb_client.client.write_api import SYNCHRONOUS
from lywsd03mmc import Lywsd03mmcClient
from scapy.all import arping

import config
from sentry import Sentry


class Gatherer(ABC):
    """Base class of each class in this script.
    Initializes and closes influx and sqlite databases connections.
    """

    def __init__(self) -> None:
        """Creates influx and sqlite databases and api's connections."""
        # influx database
        self.influx_database_client = influxdb_client.InfluxDBClient(
            url=config.DATABASE["INFLUX"]["URL"],
            token=config.DATABASE["INFLUX"]["API_TOKEN"],
            org=config.DATABASE["INFLUX"]["ORGANIZATION"],
        )
        self.influx_database_api = self.influx_database_client.write_api(
            write_options=SYNCHRONOUS
        )
        # sqlite database
        self.sqlite_database_client = sqlite3.connect(config.DATABASE["SQLITE"]["PATH"])
        self.sqlite_database_api = self.sqlite_database_client.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes connection to influx and sqlite databases."""
        # influx database
        self.influx_database_api.close()
        self.influx_database_client.close()
        # sqlite database
        self.sqlite_database_api.close()
        self.sqlite_database_client.close()


class Network(Gatherer):
    """Gathers information about devices connected to local network."""

    # set of available network metrics
    METRICS = ("number_of_devices", "active_devices")

    # influx database bucket name
    BUCKET = "network"

    def __init__(self, metric: str) -> None:
        """Constructor and main class method."""
        # calls base class constructor
        super().__init__()
        # performs arp scan of local network
        arp_scan_results = self.__arp_scan()
        # if not available metric was given
        if metric not in self.METRICS:
            logging.error(f"Incorrect metric '{metric}'!")
        # number of active devices
        elif metric == "number_of_devices":
            self.gather_number_of_devices(data=arp_scan_results)
        # active devices MAC addresses
        elif metric == "active_devices":
            self.gather_active_devices(data=arp_scan_results)

    def gather_active_devices(self, data: set) -> None:
        """Saves MAC addresses of active devices to database.
        Before data are written to database, sentry.py script is used to verify
        if there are unknown MAC addresses in received 'data' set.
        """
        try:
            # copying received data
            mac_addresses = copy.deepcopy(data)
            # verifies if there is a new MAC address in received list
            Sentry(data_type="network", dataset=mac_addresses)
            # iterates over MAC addresses
            for mac_address in mac_addresses:
                # writes single data entity to database
                point = (
                    influxdb_client.Point("devices")
                    .tag("metric", "availability")
                    .field("mac_address", mac_address)
                )
                self.influx_database_api.write(
                    bucket=self.BUCKET,
                    org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                    record=point,
                )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
        else:
            logging.info(
                f"GATHERER | "
                f"LOCATION = local | "
                f"DATA = {self.BUCKET}.{arguments.metric} | "
                f"VALUES = {mac_address} | "
            )

    def gather_number_of_devices(self, data: set) -> None:
        """Writes number of active devices to database."""
        try:
            # number of active devices in network
            number_of_devices = len(data)
            # writes data to database
            point = (
                influxdb_client.Point("devices")
                .tag("metric", "number")
                .field("quantity", number_of_devices)
            )
            self.influx_database_api.write(
                bucket=self.BUCKET, org=config.DATABASE["INFLUX"]["ORGANIZATION"], record=point
            )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}") 
        else:
            logging.info(
                f"GATHERER | "
                f"LOCATION = local | "
                f"DATA = {self.BUCKET}.{arguments.metric} | "
                f"VALUES = {number_of_devices} | "
            )

    def __arp_scan(self) -> Set[str]:
        """Performs arp scan of local network and returns list of MAC addresses."""
        try:
            # performs arp scan
            answered, unanswered = arping("192.168.0.0/24", verbose=0)
            # set of MAC addresses
            mac_addresses = set(
                destination["Ether"].src for source, destination in answered
            )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}") 
        else:
            return mac_addresses


class Air(Gatherer):
    """Gathers information from air devices connected to local network."""

    # influx database bucket name
    BUCKET = "air"

    def __init__(self) -> None:
        """Constructor and main class method."""
        # calls base class constructor
        super().__init__()
        # retrieves data from each 'air' device
        air_scan_results = self.__air_scan()
        # saves gathered data to database
        self.gather_air_data(air_scan_results)

    def gather_air_data(self, air_data: List[dict]) -> None:
        """Saves retreived data from each air devices to database."""
        try:
            # iterates over datasets
            for data in air_data:
                # data location
                location = data.get("location")
                # air quality
                aqi = data.get("aqi")
                # air humidity
                humidity = data.get("humidity")
                # air temperature
                temperature = data.get("temperature")
                # prepares data for saving into influx database
                point = (
                    influxdb_client.Point("air")
                    .tag("room", location)
                    .field("aqi", aqi)
                    .field("humidity", humidity)
                    .field("temperature", temperature)
                )
                # inserts data to influx database
                self.influx_database_api.write(
                    bucket=self.BUCKET,
                    org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                    record=point,
                )
                logging.info(
                    f"GATHERER | "
                    f"LOCATION = {data.get('location')} | "
                    f"DATA = {self.BUCKET} | "
                    f"VALUES = {aqi}, {humidity}, {temperature} | "
                )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")

    def __air_scan(self) -> List[dict]:
        """Gathers air data from each device tagged as "air" in local network."""
        try:
            # list that stores air data from each device
            air_data = []
            # variable that stores single device data
            data = None
            # air devices data
            air_devices_data = self.__get_air_devices_data()
            # iterates over devices data
            for device_data in air_devices_data:
                # name of device
                device_name = device_data.get("name").lower()
                # calls specific method depending on device type
                if "purifier" in device_name:
                    data = self.__air_scan_purifier(device_data)
                elif "monitor" in device_name:
                    data = self.__air_scan_monitor(device_data)
                else:
                    logging.error(f"Device '{device_name}' is not supported!")
                if data:
                    air_data.append(data)
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
        else:
            # calls sentry script to verifies data
            Sentry(data_type="air", dataset=air_data)
            return air_data

    def __air_scan_purifier(self, device_data: dict) -> dict:
        """Gathers data from Xiaomi Purifier device."""
        try:
            # reads data from device API
            data = os.popen(
                f"miiocli airpurifiermiot \
                --ip \{device_data.get('ip_address')} \
                --token {config.DEVICES['TOKENS'][device_data.get('mac_address')]} \
                status"
            ).read()
            # splits dataset
            data = data.split("\n")
            # parses retrived data and packs it to dictionary
            data = {
                "location": device_data.get("location"),
                "aqi": int(data[2].split(":")[1].strip().split(" ")[0]),
                "humidity": int(data[5].split(":")[1].strip().split(" ")[0]),
                "temperature": float(data[6].split(":")[1].strip().split(" ")[0]),
            }
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __air_scan_monitor(self, device_data: dict) -> dict:
        """Gathers data from Xiaomi Monitor 2 device."""
        try:
            # creates connection with device using external library
            client = Lywsd03mmcClient(device_data.get("mac_address"))
            # retrives data from connection
            data = client.data
            # parses retrived data and packs it to dictionary
            data = {
                "location": device_data.get("location"),
                "aqi": None,
                "humidity": data.humidity,
                "temperature": data.temperature,
            }
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __get_air_devices_data(self) -> List[dict]:
        """Makes query to sqlite database and returns list of air devices data."""
        try:
            # list that stores devices data
            air_devices_data = []
            # makes query to sqlite database
            query_result = {
                device_info
                for device_info
                in self.sqlite_database_api.execute(
                    """
                    SELECT devices_device.name, devices_device.ip_address, devices_device.mac_address, rooms_room.name
                    FROM devices_device
                    INNER JOIN rooms_room
                    ON devices_device.location_id = rooms_room.id
                    WHERE devices_device.category = "air";
                    """
                )
            }
            # transforms query result to list of dictionaries
            for row in query_result:
                air_devices_data.append(
                    {
                        "name": row[0],
                        "ip_address": row[1],
                        "mac_address": row[2],
                        "location": row[3]
                    }
                )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return []
        else:
            return air_devices_data


# main section of script
if __name__ == "__main__":

    # parses script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data")
    parser.add_argument("-m", "--metric", required=False)
    arguments = parser.parse_args()

    # gathers data, depends on given argument
    if arguments.data == "network":
        Network(metric=arguments.metric)
    if arguments.data == "air":
        Air()
