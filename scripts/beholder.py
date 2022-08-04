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

import config


# set of available scan metrics
METRICS = ("number_of_devices", "active_devices")

# influx database bucket name
BUCKET = "network"


def arp_scan() -> set:
    """Performs arp scan of local network and returns list of mac addresses."""
    try:
        # performs arp scan
        arp_scan_results = os.popen("sudo arp-scan -l").read()
        arp_scan_results = arp_scan_results.split("\n")
        arp_scan_results = arp_scan_results[2:-4]
        # set of mac addresses
        mac_addresses = set(row.split("\t")[1] for row in arp_scan_results)
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

# value that will be inserted to database
value = None

# if not available metric was given
if arguments.metric not in METRICS:
    print("Incorrect metric!")
# number of devices metric
# inserts number of active devices to database
elif arguments.metric == "number_of_devices":
    value = len(arp_scan_results)
    point = influxdb_client.Point("devices").tag("metric", "number").field("quantity", value)
    database_api.write(
        bucket = BUCKET,
        org = config.DB["INFLUX"]["ORGANIZATION"],
        record = point
    )
# active devices metric
# inserts mac addresses of active devices to database
elif arguments.metric == "active_devices":
    value = copy.deepcopy(arp_scan_results)
    for mac_address in value:
        point = influxdb_client.Point("devices").tag("metric", "availability").field("mac_address", mac_address)
        database_api.write(
            bucket  = BUCKET,
            org = config.DB["INFLUX"]["ORGANIZATION"],
            record = point
        )

print(f"{datetime.now()} \t\t METRIC: {arguments.metric} \t\t VALUES: {value}")
