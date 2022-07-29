import argparse
import os

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--metric", required=True)
args = parser.parse_args()

token = "z7q718_iZMU2WeCebcrnIJsCp2nCMBufdqvLskp4OaKKpB5-gC6OzYoUYBUC13u0gISa5Z6IDzAIc3FLEL4ZmA=="
org = "MG"
bucket = "network"
client = influxdb_client.InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


def scan(metric: str) -> None:
    """Gathers information about number of active devices in network."""

    # performs arp scan
    arp_results = os.popen("sudo arp-scan -l").read()
    arp_results = arp_results.split("\n")
    arp_results = arp_results[2:-4]
    number_of_devices = len(arp_results)

    # inserting data to influx
    if metric == "count":
        amount_point = influxdb_client.Point("devices").tag("metric", "amount").field("count", number_of_devices)
        print("-----------------")
        print(number_of_devices)
        write_api.write(bucket=bucket, org=org, record=amount_point)
    elif metric == "availability":
        for row in arp_results:
            splitted_row = row.split("\t")
            mac_point = influxdb_client.Point("devices").tag("metric", "availability").tag("mac", splitted_row[1]).field("active", 1)
            write_api.write(bucket=bucket, org=org, record=mac_point)

    print(f"Inserted '{metric}' data!")
    print("-----------------")


if __name__ == "__main__":
    scan(metric=args.metric)
