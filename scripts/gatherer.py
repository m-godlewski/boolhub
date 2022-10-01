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
    """Base script class.
    Initializes and closes database connection.
    """

    def __init__(self):
        """Constructor of this class creates influx database and api instances."""
        self.database_client = influxdb_client.InfluxDBClient(
            url = config.DB["influx"]["url"],
            token = config.DB["influx"]["api_token"],
            org = config.DB["influx"]["organization"]
        )
        self.database_api = self.database_client.write_api(write_options=SYNCHRONOUS)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Closes connection to influx database"""
        self.database_api.close()
        self.database_client.close()


class Network(Gatherer):
    """Gathers information about devices connected to local network.
    If "active_devices metric is used, sentry.py script also verifies if there
    are a unknown devices connected to local network.
    """

    # set of available network metrics
    METRICS = ("number_of_devices", "active_devices")

    # influx database bucket name
    BUCKET = "network"

    def __init__(self, metric: str):
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
            self.__number_of_devices(data=arp_scan_results)
        # active devices mac addresses
        elif metric == "active_devices":
            self.__active_devices(data=arp_scan_results)

    def __active_devices(self, data: set) -> None:
        """Writes mac addresses of active devices to database.
        Before data are written to database, sentry.py script is used to verify
        if there are unknown mac_addresses in received data argument.
        """
        # verifies if there is a new mac address in received list
        Sentry(mac_addresses_list=data)
        # iterates over mac addresses
        for mac_address in data:
            # writes single data entity to database
            point = influxdb_client.Point("devices").tag("metric", "availability").field("mac_address", mac_address)
            self.database_api.write(
                bucket  = self.BUCKET,
                org = config.DB["influx"]["organization"],
                record = point
            )
        print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {data}")

    def __arp_scan(self) -> set:
        """Performs arp scan of local network and returns list of mac addresses."""
        try:
            # performs arp scan
            answered, unanswered = arping("192.168.0.0/24", verbose=0)
            # set of mac addresses
            mac_addresses = set(destination["Ether"].src for source, destination in answered)
        except Exception:
            print(traceback.format_exc())
        else:
            return mac_addresses

    def __number_of_devices(self, data: set) -> None:
        """Write number of active devices to database."""
        # number of active devices in network
        number_of_devices = len(data)
        # writes data to database
        point = influxdb_client.Point("devices").tag("metric", "number").field("quantity", number_of_devices)
        self.database_api.write(
            bucket = self.BUCKET,
            org = config.DB["influx"]["organization"],
            record = point
        )
        print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {number_of_devices}")


class Air(Gatherer):
    """Gathers information about air devices connected to local network."""

    # influx database bucket name
    BUCKET = "air"

    def __init__(self):
        """Constructor and main class method."""

        # calls base class constructor
        super().__init__()

        # performs air scan
        air_scan_results = self.__air_scan()

        # air data
        aqi = air_scan_results[0]
        humidity = air_scan_results[1]
        temperature = air_scan_results[2]

        # prepares data for inserts to influx database
        point = influxdb_client.Point("air").tag("room", "bedroom").field("aqi", aqi).field("humidity", humidity).field("temperature", temperature)

        # inserts data to influx database
        self.database_api.write(
            bucket = self.BUCKET,
            org = config.DB["influx"]["organization"],
            record = point
        )
        print(f"{datetime.now()} \t\t METRIC: bedroom \t\t VALUES: {aqi}, {humidity}, {temperature}")

    def __air_scan(self) -> Union[int, int, float]:
        """Gathers air data from all devices tagged as "air" in local network."""
        try:
            # retrives air status from device
            air_status = os.popen(
                f"miiocli airpurifiermiot --ip 192.168.0.101 --token {config.DEVICES['tokens']['purifier']} status"
            ).read()
            air_status = air_status.split("\n")
            # variables that stores air status
            aqi = int(air_status[2].split(":")[1].strip().split(" ")[0])
            humidity = int(air_status[5].split(":")[1].strip().split(" ")[0])
            temperature = float(air_status[6].split(":")[1].strip().split(" ")[0])
        except Exception:
            print(traceback.format_exc())
        else:
            return (aqi, humidity, temperature)


# main section of script
if __name__ == "__main__":

    # gathers data, depends on given argument
    if arguments.data == "network":
        Network(metric=arguments.metric)
    if arguments.data == "air":
        Air()
