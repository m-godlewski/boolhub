"""
This script is used for storing classes used to communicate with databases.
"""

import config
import logging
import traceback
import typing
from datetime import datetime

import influxdb_client
import psycopg2
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from scripts.models.data import DeviceData, UnknownDeviceData, AirData


class Database:
    """Base class of each other classes in this script."""

    pass


class PostgreSQL(Database):
    """Class responsible for PostgreSQL database communication."""

    def __init__(self) -> None:
        """Initializes database and api connection."""
        logging.debug(f"Connecting to {self.__class__.__name__}")
        self.client = psycopg2.connect(
            host=config.DATABASE["POSTGRE"]["HOST"],
            database=config.DATABASE["POSTGRE"]["NAME"],
            user=config.DATABASE["POSTGRE"]["USER"],
            password=config.DATABASE["POSTGRE"]["PASSWORD"],
        )
        self.client.autocommit = True
        self.api = self.client.cursor()
        logging.debug(f"Connected to {self.__class__.__name__}")

    def __enter__(self) -> object:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes database and api connection."""
        # log error if any exception ocurred during context process
        if any((exc_type, exc_value, exc_traceback)):
            logging.error(exc_traceback)
        # closes connection and api
        logging.debug(f"Closing {self.__class__.__name__} connection")
        self.api.close()
        self.client.close()
        logging.debug(f"{self.__class__.__name__} connection has been closed")

    @property
    def devices(self) -> typing.List[DeviceData]:
        """Returns list of registered devices."""
        try:
            self.api.execute(
                """
                SELECT d.name, r.name, d.category, d.brand, d.mac_address, d.ip_address, d.token
                FROM devices_device as d
                INNER JOIN rooms_room as r
                ON r.id = d.location_id;
                """
            )
            devices = [DeviceData(*row) for row in self.api.fetchall()]
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            return devices

    @property
    def unknown_devices(self) -> typing.List[UnknownDeviceData]:
        """Returns list of unregistered devices."""
        try:
            self.api.execute("SELECT * FROM unknown_devices;")
            unknown_devices = [UnknownDeviceData(*row) for row in self.api.fetchall()]
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            return unknown_devices

    def add_unknown_device(self, mac_address: str) -> bool:
        """Checks if given mac address exists in database. If it doesn't insert new row.
        Otherwise, update existed row with current date and time.
        Returns True if operation succeed. Otherwise, returns False.
        """
        try:
            # if given mac address is not present in unknown_devices database
            if mac_address not in {device.mac_address for device in self.unknown_devices}:
                self.api.execute(
                    "INSERT INTO unknown_devices(mac_address, last_time) VALUES(%s, %s);",
                    (mac_address, datetime.now(),)
                )
            # otherwise update 'last_time' column
            else:
                self.api.execute(
                    "UPDATE unknown_devices SET last_time = %s WHERE mac_address = %s;",
                    (datetime.now(), mac_address,)
                )  
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True


class InfluxDB(Database):
    """Class responsible for Influx database connection."""

    def __enter__(self) -> object:
        # initializes database connection
        logging.debug("Connecting to InfluxDB")
        self.client = influxdb_client.InfluxDBClient(
            url=config.DATABASE["INFLUX"]["URL"],
            token=config.DATABASE["INFLUX"]["API_TOKEN"],
            org=config.DATABASE["INFLUX"]["ORGANIZATION"],
        )
        self.api = self.client.write_api(write_options=SYNCHRONOUS)
        logging.debug("Connected to InfluxDB")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        # closes database connection
        # if any exception ocurred during context process
        if any((exc_type, exc_value, exc_traceback)):
            logging.error(exc_traceback)
        # closes database connection
        logging.debug(f"Closing {self.__class__.__name__} connection")
        self.api.close()
        self.client.close()
        logging.debug(f"{self.__class__.__name__} connection has been closed")

    def add_point_network(self, measurement: str, metric: str, field: str, value: typing.Any) -> bool:
        """Writes single network data entity to database.
        Returns True, if operation succeed. Otherwise returns False.
        """
        try:
            point = (
                Point(measurement)
                .tag("metric", metric)
                .field(field, value)
            )
            self.api.write(
                bucket="network",
                org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                record=point,
            )
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True

    def add_point_air(self, air_data: AirData) -> bool:
        """Writes single air data entity to database.
        Returns True, if operation succeed. Otherwise returns False.
        """
        try:
            point = (
                Point("air")
                .tag("room", air_data.device.location)
                .field("aqi", air_data.aqi)
                .field("humidity", air_data.humidity)
                .field("temperature", air_data.temperature)
            )
            self.api.write(
                bucket="air",
                org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                record=point,
            )
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return False
        else:
            return True
