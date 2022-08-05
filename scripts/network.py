"""
Local network observer script.
"""

import argparse
import copy
import os
import traceback
from datetime import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from scapy.all import arping

import config


# set of available scan metrics
METRICS = ("number_of_devices", "active_devices")

# influx database bucket name
BUCKET = "network"


def arp_scan() -> set:
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
        mac_addresses = set(m["Ether"] for _, m in answered)
        print(mac_address)
    except Exception:
        print("Exception ocurred during arp_scan!")
        print(traceback.format_exc())
    else:
        return mac_addresses


# parsing script argument
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--metric")
arguments = parser.parse_args()

# initializing database connection
database_client = influxdb_client.InfluxDBClient(
    url = config.DB["INFLUX"]["URL"],
    token = config.DB["INFLUX"]["API_TOKEN"],
    org = config.DB["INFLUX"]["ORGANIZATION"]
)

# database api
database_api = database_client.write_api(write_options=SYNCHRONOUS)

# performing arp scan of local network
arp_scan_results = arp_scan()

# if not available metric was given
if arguments.metric not in METRICS:
    print(f"{datetime.now()} Incorrect metric! '{arguments.metric}'")
# number of devices metric
# inserts number of active devices to database
elif arguments.metric == "number_of_devices":
    number_of_devices = len(arp_scan_results)
    point = influxdb_client.Point("devices").tag("metric", "number").field("quantity", number_of_devices)
    database_api.write(
        bucket = BUCKET,
        org = config.DB["INFLUX"]["ORGANIZATION"],
        record = point
    )
    print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {number_of_devices}")
# active devices metric
# inserts mac addresses of active devices to database
elif arguments.metric == "active_devices":
    mac_addresses = copy.deepcopy(arp_scan_results)
    for mac_address in mac_addresses:
        point = influxdb_client.Point("devices").tag("metric", "availability").field("mac_address", mac_address)
        database_api.write(
            bucket  = BUCKET,
            org = config.DB["INFLUX"]["ORGANIZATION"],
            record = point
        )
    print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {mac_addresses}")