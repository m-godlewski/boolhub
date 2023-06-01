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
from typing import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import influxdb_client
import psycopg2
from influxdb_client.client.write_api import SYNCHRONOUS
from scapy.all import arping

import config
from sentry import Sentry
from models.device import MiAirPurifier3H, MiMonitor2


class Gatherer(ABC):
    """Base class of each class in this script.
    Initializes and closes influx and postgre databases connections.
    """

    def __init__(self) -> None:
        """Creates influx and postgre databases and api's connections."""
        # influx database
        self.influx_database_client = influxdb_client.InfluxDBClient(
            url=config.DATABASE["INFLUX"]["URL"],
            token=config.DATABASE["INFLUX"]["API_TOKEN"],
            org=config.DATABASE["INFLUX"]["ORGANIZATION"],
        )
        self.influx_database_api = self.influx_database_client.write_api(
            write_options=SYNCHRONOUS
        )
        # postgre database
        self.postgre_database_client = psycopg2.connect(
            host=config.DATABASE["POSTGRE"]["HOST"],
            database=config.DATABASE["POSTGRE"]["NAME"],
            user=config.DATABASE["POSTGRE"]["USER"],
            password=config.DATABASE["POSTGRE"]["PASSWORD"],
        )
        self.postgre_database_api = self.postgre_database_client.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes connection to influx and postgre databases."""
        # influx database
        self.influx_database_api.close()
        self.influx_database_client.close()
        # postgre database
        self.postgre_database_api.close()
        self.postgre_database_client.close()


class Network(Gatherer):
    """Gathers information about devices connected to local network."""

    # influx database bucket name
    BUCKET = "network"

    def __init__(self) -> None:
        """Constructor and main class method."""
        # calls base class constructor
        super().__init__()
        # performs arp scan of local network
        arp_scan_results = self.__arp_scan()
        # gathers network data
        self.gather_network_data(data=arp_scan_results)

    def gather_network_data(self, data: Set[str]) -> None:
        """Saves MAC addresses and number of active devices to database.
        Before data are written to database, sentry.py script is used to verify
        if there are unknown MAC addresses in received 'data' set or
        number of connected devices exceedes threshold."""
        try:
            # copying received data
            mac_addresses = copy.deepcopy(data)
            # verifies if there is a new MAC address in received list
            # or number of connected devices exceedes threshold
            Sentry(data_type="network", dataset=mac_addresses)
            # "availability" tag
            # iterates over mac addresses
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
            # "number" tag
            # number of active devices in local network
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
                f"DATA = {self.BUCKET}.availability | "
                f"VALUES = {mac_addresses} | "
            )
            logging.info(
                f"GATHERER | "
                f"LOCATION = local | "
                f"DATA = {self.BUCKET}.number | "
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
            # list that stores diagnostical data from each device
            diagnostical_data = []
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
                    data, health_data = self.__air_scan_purifier(device_data)
                elif "monitor" in device_name:
                    data, health_data = self.__air_scan_monitor(device_data)
                else:
                    logging.error(f"Device '{device_name}' is not supported!")
                if data:
                    air_data.append(data)
                if health_data:
                    diagnostical_data.append(health_data)
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
        else:
            # calls sentry script to verifies data
            Sentry(data_type="air", dataset=air_data)
            Sentry(data_type="diagnostic", dataset=diagnostical_data)
            return air_data

    def __air_scan_purifier(self, device_data: dict) -> Union[dict, dict]:
        """Gathers data from Xiaomi Purifier device."""
        try:
            # fetches data from device
            device = MiAirPurifier3H(
                ip_address=device_data.get("ip_address"),
                mac_address=device_data.get("mac_address"),
                token=config.DEVICES["TOKENS"][device_data.get("mac_address")]
            )
            # merges datasets
            data = {**device.data, **device_data}
            health_data = {**device.health, **device_data}
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return {}, {}
        else:
            return data, health_data

    def __air_scan_monitor(self, device_data: dict) -> Union[dict, dict]:
        """Gathers data from Xiaomi Monitor 2 device."""
        try:
            # fetches data from device
            device = MiMonitor2(
                ip_address=device_data.get("ip_address"),
                mac_address=device_data.get("mac_address")
            )
            # merges datasets
            data = {**device.data, **device_data}
            health_data = {**device.health, **device_data}
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return {}, {}
        else:
            return data, health_data

    def __get_air_devices_data(self) -> List[dict]:
        """Makes query to postgre database and returns list of air devices data."""
        try:
            # list that stores devices data
            air_devices_data = []
            # makes query to postgre database
            self.postgre_database_api.execute(
                    """
                    SELECT devices_device.name, devices_device.ip_address, devices_device.mac_address, rooms_room.name
                    FROM devices_device
                    INNER JOIN rooms_room
                    ON devices_device.location_id = rooms_room.id
                    WHERE devices_device.category = 'air';
                    """
            )
            query_result = [device_info for device_info in self.postgre_database_api.fetchall()]
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
    arguments = parser.parse_args()

    # gathers data, depends on given argument
    if arguments.data == "network":
        Network()
    if arguments.data == "air":
        Air()
