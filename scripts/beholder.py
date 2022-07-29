import argparse
import config
import os
import traceback
from datetime import datetime
from typing import *

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


# arguments parse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--metric")
arguments = parser.parse_args()


class Beholder:
    """Network observer class."""

    # class constants values
    BUCKET = "network"
    # KNOWN_MACS = list(config.KNOWN_DEVICES.values())

    def __init__(self) -> None:
        """Class constructor."""
        # database client
        self.influxdb_client = influxdb_client.InfluxDBClient(
            url = config.INFLUX["URL"],
            token = config.INFLUX["API_TOKEN"],
            org = config.INFLUX["ORGANIZATION"]
        )
        # database api
        self.influxdb_api = self.influxdb_client.write_api(
            write_options=SYNCHRONOUS
        )

    def scan(self, metric: str) -> None:
        """Performs an arp scan and saves its results to the database depending on the given metric."""
        try:

            # performs arp scan
            arp_scan_results = self.__arp_scan()

            # number of active devices in network
            if metric == "number":
                number_of_devices = len(arp_scan_results)
                point = influxdb_client.Point("devices").tag("metric", "number").field("quantity", number_of_devices)
                self.influxdb_api.write(
                    bucket=self.BUCKET,
                    org=config.INFLUX["ORGANIZATION"],
                    record=point
                )
                print(f"{datetime.now()} \t\t METRIC: {metric} \t\t VALUES: {number_of_devices}")

            # list of active devices mac addresses
            elif metric == "availability":
                for mac in arp_scan_results:
                    point = influxdb_client.Point("devices").tag("metric", "availability").field("mac_address", mac)
                    self.influxdb_api.write(
                        bucket=self.BUCKET,
                        org=config.INFLUX["ORGANIZATION"],
                        record=point
                    )
                print(f"{datetime.now()} \t\t METRIC: {metric} \t\t VALUES: {arp_scan_results}")

            else:
                print("Incorrect metric!")

        except Exception:
            print(traceback.format_exc())
        else:
            self.influxdb_client.close()

    def __arp_scan(self) -> set:
        """Performs arp scan of local network and returns list of mac addresses."""
        try:

            # performs arp scan
            arp_scan_results = os.popen("sudo arp-scan -l").read()
            arp_scan_results = arp_scan_results.split("\n")
            arp_scan_results = arp_scan_results[2:-4]

            # set of mac addresses
            mac_addresses = set(row.split("\t")[1] for row in arp_scan_results)

        except Exception:
            print(traceback.format_exc())
        else:
            return mac_addresses


# main script loop
if __name__ == "__main__":
    Beholder().scan(metric=arguments.metric)
