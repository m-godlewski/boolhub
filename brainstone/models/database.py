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
import psycopg2.extras
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from models.data import DeviceData, UnknownDeviceData, AirData


class PostgreSQL:
    """Class responsible for PostgreSQL database communication."""

    def __init__(self, settings: bool = False) -> None:
        """Initializes database and api connection."""
        logging.debug(f"DATABASE | {self.__class__.__name__} | Connecting")
        self.client = psycopg2.connect(
            host=config.DATABASE["POSTGRE"]["HOST"],
            database=config.DATABASE["POSTGRE"]["NAME"],
            user=config.DATABASE["POSTGRE"]["USER"],
            password=config.DATABASE["POSTGRE"]["PASSWORD"],
        )
        self.client.autocommit = True
        # in case connection with settings flag set to true
        if settings:
            self.api = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            self.api = self.client.cursor()
        logging.debug(f"DATABASE | {self.__class__.__name__} | Connected")

    def __enter__(self) -> object:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes database and api connection."""
        # log error if any exception ocurred during context process
        if any((exc_type, exc_value, exc_traceback)):
            logging.error(exc_value)
        # closes connection and api
        self.api.close()
        self.client.close()
        logging.debug(f"DATABASE | {self.__class__.__name__} | Connection closed")

    @property
    def devices(self) -> typing.Set[DeviceData]:
        """Returns set of registered devices."""
        try:
            self.api.execute(
                """
                SELECT d.name, r.name, d.category, d.brand, d.mac_address, d.ip_address, d.token
                FROM devices_device as d
                LEFT JOIN rooms_room as r
                ON r.id = d.location_id;
                """
            )
            devices = set(DeviceData(*row) for row in self.api.fetchall())
        except Exception:
            logging.error(
                f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return set()
        else:
            return devices

    @property
    def settings(self) -> typing.Dict:
        """Returns current system settings."""
        try:
            self.api.execute("SELECT * FROM settings;")
            result = self.api.fetchone()
            settings = dict(result)
        except Exception:
            logging.error(
                f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return {}
        else:
            return settings

    @property
    def unknown_devices(self) -> typing.Set[UnknownDeviceData]:
        """Returns set of unregistered devices."""
        try:
            self.api.execute("SELECT * FROM unknown_devices;")
            unknown_devices = set(
                UnknownDeviceData(**row) for row in self.api.fetchall()
            )
        except Exception:
            logging.error(
                f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return set()
        else:
            return unknown_devices

    def add_unknown_device(self, mac_address: str) -> bool:
        """Checks if given mac address exists in database. If it doesn't insert new row.
        Otherwise, update existed row with current date and time.
        Returns True if operation succeed. Otherwise, returns False.
        """
        try:
            # if given mac address is not present in unknown_devices database
            if mac_address not in {
                device.mac_address for device in self.unknown_devices
            }:
                self.api.execute(
                    "INSERT INTO unknown_devices(mac_address, last_time) VALUES(%s, %s);",
                    (
                        mac_address,
                        datetime.now(),
                    ),
                )
            # otherwise update 'last_time' column
            else:
                self.api.execute(
                    "UPDATE unknown_devices SET last_time = %s WHERE mac_address = %s;",
                    (
                        datetime.now(),
                        mac_address,
                    ),
                )
        except Exception:
            logging.error(
                f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return False
        else:
            return True

    def get_device_by_name(self, device_name: str = "") -> DeviceData:
        """Returns set of DeviceData objects of given device name."""
        try:
            self.api.execute(
                """
                SELECT d.name, r.name, d.category, d.brand, d.mac_address, d.ip_address, d.token
                FROM devices_device as d
                INNER JOIN rooms_room as r
                ON r.id = d.location_id
                WHERE d.name = %s;
                """,
                (device_name,),
            )
            device = DeviceData(*self.api.fetchone())
        except Exception:
            logging.error(
                f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return None
        else:
            return device

    def get_device_by_type(self, device_type: str = "") -> typing.Set[DeviceData]:
        """Returns set of DeviceData objects of given device type."""
        try:
            devices_data = set(
                device for device in self.devices if device.category == device_type
            )
        except Exception:
            logging.error(
                f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return set()
        else:
            return devices_data


class InfluxDB:
    """Class responsible for Influx database connection."""

    def __enter__(self) -> object:
        # initializes database connection
        logging.debug(f"DATABASE | {self.__class__.__name__} | Connecting")
        self.client = influxdb_client.InfluxDBClient(
            url=config.DATABASE["INFLUX"]["URL"],
            token=config.DATABASE["INFLUX"]["API_TOKEN"],
            org=config.DATABASE["INFLUX"]["ORGANIZATION"],
        )
        self.api = self.client.write_api(write_options=SYNCHRONOUS)
        logging.debug(f"DATABASE | {self.__class__.__name__} | Connected")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        # closes database connection
        # if any exception ocurred during context process
        if any((exc_type, exc_value, exc_traceback)):
            logging.error(exc_value)
        # closes database connection
        self.api.close()
        self.client.close()
        logging.debug(f"DATABASE | {self.__class__.__name__} | Connection closed")

    def add_point_network(
        self, measurement: str, metric: str, field: str, value: typing.Any
    ) -> bool:
        """Writes single network data entity to database.
        Returns True, if operation succeed. Otherwise returns False.
        """
        try:
            point = Point(measurement).tag("metric", metric).field(field, value)
            self.api.write(
                bucket="network",
                org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                record=point,
            )
        except Exception:
            logging.error(
                f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
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
            logging.error(
                f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return False
        else:
            return True

    def add_point_health(self, air_data: AirData) -> bool:
        """Writes single health data entity to database.
        Returns True, if operation succeed. Otherwise returns False.
        """
        try:
            point = (
                Point("health")
                .tag("room", air_data.device.location)
                .field("battery/filter", air_data.health_data_indicator)
            )
            self.api.write(
                bucket="health",
                org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                record=point,
            )
        except Exception:
            logging.error(
                f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return False
        else:
            return True

    def add_point_forecast(self, forecast_data) -> bool:
        """Writes single forecast data entity to database.
        Returns True, if operation succeed. Otherwise returns False.
        """
        try:
            point = (
                Point("forecast")
                .field("temperature", forecast_data.temperature)
                .field("humidity", forecast_data.humidity)
                .time(forecast_data.date)
            )
            self.api.write(
                bucket="forecast",
                org=config.DATABASE["INFLUX"]["ORGANIZATION"],
                record=point,
            )
        except Exception:
            logging.error(
                f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return False
        else:
            return True
