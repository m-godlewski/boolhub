"""
This script is used for storing classes used to communicate with databases.
"""

import config
import logging
from typing import *

import influxdb_client
import psycopg2
from influxdb_client.client.write_api import SYNCHRONOUS


class Database:
    """Base class of each other classes in this script."""

    pass


class PostgreSQL(Database):
    """Class responsible for PostgreSQL database connection."""

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
        """Return object itself."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes database and api connection."""
        # if any exception ocurred during context process
        if any((exc_type, exc_value, exc_traceback)):
            logging.error(exc_traceback)
        # closes connection
        logging.debug(f"Closing {self.__class__.__name__} connection")
        self.api.close()
        self.client.close()
        logging.debug(f"{self.__class__.__name__} connection has been closed")

    def known_devices_mac_addresses(self) -> Set[str]:
        """Returns mac addresses of registered devices."""
        self.api.execute("SELECT mac_address FROM devices_device;")
        return {mac_address[0] for mac_address in self.api.fetchall()}

    def unknown_devices_mac_addresses(self) -> Set[str]:
        """Returns mac addresses of unregistered devices."""
        self.api.execute("SELECT mac_address FROM unknown_devices;")
        return {mac_address[0] for mac_address in self.api.fetchall()}


class InfluxDB(Database):
    """Class responsible for Influx database connection."""

    def __enter__(self) -> influxdb_client.WriteApi:
        # initializes database connection
        logging.debug("Connecting to InfluxDB")
        self.client = influxdb_client.InfluxDBClient(
            url=config.DATABASE["INFLUX"]["URL"],
            token=config.DATABASE["INFLUX"]["API_TOKEN"],
            org=config.DATABASE["INFLUX"]["ORGANIZATION"],
        )
        self.api = self.client.write_api(write_options=SYNCHRONOUS)
        logging.debug("Connected to InfluxDB")
        return self.api

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
