"""
Script responsible for gathering data from local network.
"""

import argparse
import os
import sys
import traceback
from datetime import datetime
from typing import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import influxdb_client
import sqlite3
from influxdb_client.client.write_api import SYNCHRONOUS
from scapy.all import arping

import config
from sentry import Sentry


# parses script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data")
parser.add_argument("-m", "--metric", required=False)
arguments = parser.parse_args()


class Gatherer:
    """Base class of each class in this script.
    Initializes and closes influx database connection.
    """

    def __init__(self) -> None:
        """Creates influx and sqlite databases and api's connections."""
        # influx database
        self.influx_database_client = influxdb_client.InfluxDBClient(
            url=config.DB["influx"]["url"],
            token=config.DB["influx"]["api_token"],
            org=config.DB["influx"]["organization"],
        )
        self.influx_database_api = self.influx_database_client.write_api(
            write_options=SYNCHRONOUS
        )
        # sqlite database
        self.sqlite_database_client = sqlite3.connect(config.DB["sqlite"]["path"])
        self.sqlite_database_api = self.sqlite_database_client.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes connection to influx and sqlite databases."""
        # influx database
        self.influx_database_api.close()
        self.influx_database_client.close()
        # sqlite database
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
            print(f"{datetime.now()} Incorrect metric! '{metric}'")
        # number of active devices
        elif metric == "number_of_devices":
            self.__gather_number_of_devices(data=arp_scan_results)
        # active devices MAC addresses
        elif metric == "active_devices":
            self.__gather_active_devices(data=arp_scan_results)

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
            print(traceback.format_exc())
        else:
            return mac_addresses

    def __gather_active_devices(self, data: set) -> None:
        """Saves MAC addresses of active devices to database.
        Before data are written to database, sentry.py script is used to verify
        if there are unknown MAC addresses in received 'data' set.
        """
        # verifies if there is a new MAC address in received list
        Sentry(data="network", dataset=data)
        # iterates over MAC addresses
        for mac_address in data:
            # writes single data entity to database
            point = (
                influxdb_client.Point("devices")
                .tag("metric", "availability")
                .field("mac_address", mac_address)
            )
            self.influx_database_api.write(
                bucket=self.BUCKET,
                org=config.DB["influx"]["organization"],
                record=point,
            )
        print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {data}")

    def __gather_number_of_devices(self, data: set) -> None:
        """Writes number of active devices to database."""
        # number of active devices in network
        number_of_devices = len(data)
        # writes data to database
        point = (
            influxdb_client.Point("devices")
            .tag("metric", "number")
            .field("quantity", number_of_devices)
        )
        self.influx_database_api.write(
            bucket=self.BUCKET, org=config.DB["influx"]["organization"], record=point
        )
        print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {number_of_devices}")


class Air(Gatherer):
    """Gathers information from air devices connected to local network."""

    # influx database bucket name
    BUCKET = "air"

    def __init__(self):
        """Constructor and main class method."""
        # calls base class constructor
        super().__init__()
        # air data retrieved from each of air devices
        air_data = self.__air_scan()
        # iterate over air data
        for data in air_data:
            # air quality
            aqi = data.get("aqi")
            # air humidity
            humidity = data.get("humidity")
            # air temperature
            temperature = data.get("temperature")
            # prepares data for saving into influx database
            point = (
                influxdb_client.Point("air")
                .tag("room", "bedroom")
                .field("aqi", aqi)
                .field("humidity", humidity)
                .field("temperature", temperature)
            )
            # inserts data to influx database
            self.influx_database_api.write(
                bucket=self.BUCKET,
                org=config.DB["influx"]["organization"],
                record=point,
            )
            print(f"{datetime.now()} \t\t ROOM: {data['location']} \t\t VALUES: {aqi}, {humidity}, {temperature}")

    def __air_scan(self) -> List[dict]:
        """Gathers air data from each device tagged as "air" in local network."""
        try:
            # list that stores air data from all devices
            air_data = []
            # air devices addresses
            air_devices = self.__get_air_devices()
            # iterate over air devices ip and MAC addresses
            for ip_address, mac_address, location in air_devices:
                # gather air data from device
                data = os.popen(
                    f"miiocli airpurifiermiot --ip {ip_address} --token {config.DEVICES['TOKENS'][mac_address]} status"
                ).read()
                data = data.split("\n")
                # packing air data from device into dictionary
                data = {
                    "location": location,
                    "aqi": int(data[2].split(":")[1].strip().split(" ")[0]),
                    "humidity": int(data[5].split(":")[1].strip().split(" ")[0]),
                    "temperature": float(data[6].split(":")[1].strip().split(" ")[0]),
                }
                air_data.append(data)
            # calling sentry script to verifies air data
            Sentry(data="air", dataset=air_data)
        except Exception:
            print(traceback.format_exc())
        else:
            return air_data

    def __get_air_devices(self) -> Set[str]:
        """Makes query to sqlite database and returns set of air devices ip addresses."""
        return {
            device_info
            for device_info in self.sqlite_database_api.execute(
                """
                SELECT devices_device.ip_address, devices_device.mac_address, rooms_room.name
                FROM devices_device
                INNER JOIN rooms_room
                ON devices_device.location_id = rooms_room.id
                WHERE devices_device.category = "air";
                """
            )
        }


# main section of script
if __name__ == "__main__":

    # gathers data, depends on given argument
    if arguments.data == "network":
        Network(metric=arguments.metric)
    if arguments.data == "air":
        Air()
