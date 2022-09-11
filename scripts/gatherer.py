"""
Script responsible for gathering data from local network.
"""

import argparse
import os
import traceback
from datetime import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from scapy.all import arping

import config


# parsing script arguments
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
            url = config.DB["INFLUX"]["URL"],
            token = config.DB["INFLUX"]["API_TOKEN"],
            org = config.DB["INFLUX"]["ORGANIZATION"]
        )
        self.database_api = self.database_client.write_api(write_options=SYNCHRONOUS)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Closes connection to influx database"""
        self.database_api.close()
        self.database_client.close()


class Network(Gatherer):
    """Gathering information about devices connected to local network."""

    # set of available network metrics
    METRICS = ("number_of_devices", "active_devices")

    # influx database bucket name
    BUCKET = "network"

    def __init__(self, metric: str):
        """Scan local network and insert data to influx database depends on given metric."""

        # calling base class constructor
        super().__init__()

        # performing arp scan of local network
        arp_scan_results = self.__arp_scan()

        # if not available metric was given
        if metric not in self.METRICS:
            print(f"{datetime.now()} Incorrect metric! '{metric}'")

        # number of active devices
        elif metric == "number_of_devices":
            number_of_devices = len(arp_scan_results)
            point = influxdb_client.Point("devices").tag("metric", "number").field("quantity", number_of_devices)
            self.database_api.write(
                bucket = self.BUCKET,
                org = config.DB["INFLUX"]["ORGANIZATION"],
                record = point
            )
            print(f"{datetime.now()} \t\t METRIC: {metric} \t\t VALUES: {number_of_devices}")

        # active devices mac addresses
        elif metric == "active_devices":
            for mac_address in arp_scan_results:
                point = influxdb_client.Point("devices").tag("metric", "availability").field("mac_address", mac_address)
                self.database_api.write(
                    bucket  = self.BUCKET,
                    org = config.DB["INFLUX"]["ORGANIZATION"],
                    record = point
                )
            print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {arp_scan_results}")

    def __arp_scan(self) -> set:
        """Performs arp scan of local network and returns list of mac addresses."""
        try:
            # previous version of arp-scan, that using bash command
            """
            # performs arp scan
            arp_scan_results = os.popen("sudo arp-scan -l").read()
            arp_scan_results = arp_scan_results.split("\n")
            arp_scan_results = arp_scan_results[2:-4]
            mac_addresses = set(row.split("\t")[1] for row in arp_scan_results)
            """
            # performs arp scan
            answered, unanswered = arping("192.168.0.0/24", verbose=0)
            # set of mac addresses
            mac_addresses = set(destination["Ether"].src for source, destination in answered)
        except Exception:
            print(traceback.format_exc())
        else:
            return mac_addresses


class Air(Gatherer):
    """"""

    # influx database bucket name
    BUCKET = "air"

    def __init__(self):
        """"""

        # calling base class constructor
        super().__init__()

    def __air_scan(self):
        """"""
        try:
            results = os.popen()
        except:
            pass
        else:
            pass


# main section of script
if __name__ == "__main__":

    # gathering data, depends on given argument
    if arguments.data == "network":
        Network(metric=arguments.metric)
    if arguments.data == "air":
        Air()
