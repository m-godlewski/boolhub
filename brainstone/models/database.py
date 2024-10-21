"""
This script is used for storing classes used to communicate with databases.
"""

import config
import logging
import traceback
import typing
from datetime import datetime

import influxdb_client
import pickle
import psycopg2
import redis
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from models.data import DeviceData, UnknownDeviceData, AirData


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
            logging.error(exc_value)
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
                LEFT JOIN rooms_room as r
                ON r.id = d.location_id;
                """
            )
            devices = [DeviceData(*row) for row in self.api.fetchall()]
        except Exception:
            logging.error(f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
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
            logging.error(f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
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
            logging.error(f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return False
        else:
            return True

    def get_device_by_name(self, device_name: str = "") -> DeviceData:
        """Returns list of DeviceData objects of given device name."""
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
            logging.error(f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return None
        else:
            return device

    def get_device_by_type(self, device_type: str = "") -> typing.List[DeviceData]:
        """Returns list of DeviceData objects of given device type."""
        try:
            devices_data = [
                device for device in self.devices if device.category == device_type
            ]
        except Exception:
            logging.error(f"DATABASE | POSTGRESQL | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return []
        else:
            return devices_data


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
            logging.error(exc_value)
        # closes database connection
        logging.debug(f"Closing {self.__class__.__name__} connection")
        self.api.close()
        self.client.close()
        logging.debug(f"{self.__class__.__name__} connection has been closed")

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
            logging.error(f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
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
            logging.error(f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
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
            logging.error(f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
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
            logging.error(f"DATABASE | INFLUXDB | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return False
        else:
            return True


class Redis(Database):
    """Class responsible for Redis database communication."""

    def __init__(self) -> None:
        """Initializes database and api connection."""
        logging.debug(f"Connecting to {self.__class__.__name__}")
        # creates connection pool
        self.client = redis.Redis(
            host=config.DATABASE["REDIS"]["HOST"],
            password=config.DATABASE["REDIS"]["PASSWORD"],
            port=config.DATABASE["REDIS"]["PORT"],
        )
        logging.debug(f"Connected to {self.__class__.__name__}")

    def __enter__(self) -> object:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes database and api connection."""
        # log error if any exception ocurred during context process
        if any((exc_type, exc_value, exc_traceback)):
            logging.error(exc_value)
        # closes connection and api
        logging.debug(f"Closing {self.__class__.__name__} connection")
        self.client.close()
        logging.debug(f"{self.__class__.__name__} connection has been closed")

    # region NOTIFICATION FLAGS

    @property
    def notify_temperatue(self) -> bool:
        return pickle.loads(self.client.get("constance:Powiadamiaj o temperaturze"))

    @property
    def notify_humidity(self) -> bool:
        return pickle.loads(self.client.get("constance:Powiadamiaj o wilgotności"))

    @property
    def notify_aqi(self) -> bool:
        return pickle.loads(self.client.get("constance:Powiadamiaj o zanieczyszczeniu"))

    @property
    def notify_devices_diagnostics(self) -> bool:
        return pickle.loads(
            self.client.get("constance:Powiadamiaj o diagnostyce urządzeń")
        )

    @property
    def notify_network_overload(self) -> bool:
        return pickle.loads(
            self.client.get("constance:Powiadamiaj o przeciążeniu sieci")
        )

    @property
    def notify_network_unknown_device(self) -> bool:
        return pickle.loads(
            self.client.get("constance:Powiadamiaj o nieznanym urządzeniu w sieci")
        )

    # endregion

    # region THRESHOLD VALUES

    @property
    def notify_temperatue_upper(self) -> float:
        return pickle.loads(self.client.get("constance:Maksymalna temperatura"))

    @property
    def notify_temperatue_lower(self) -> float:
        return pickle.loads(self.client.get("constance:Minimalna temperatura"))

    @property
    def notify_humidity_upper(self) -> int:
        return pickle.loads(self.client.get("constance:Maksymalna wilgotność"))

    @property
    def notify_humidity_lower(self) -> int:
        return pickle.loads(self.client.get("constance:Minimalna wilgotność"))

    @property
    def notify_aqi_max(self) -> int:
        return pickle.loads(self.client.get("constance:Próg zanieczyszczenia"))

    @property
    def notify_devices_diagnostics_level(self) -> int:
        return pickle.loads(
            self.client.get("constance:Minimalny poziom baterii/filtra")
        )

    @property
    def notify_network_overload_level(self) -> int:
        return pickle.loads(self.client.get("constance:Próg przeciążenia sieci"))

    # endregion

    # region NTFY

    @property
    def ntfy_url(self) -> int:
        return pickle.loads(self.client.get("constance:NTFY URL"))

    # endregion

    # region WEATHER API

    @property
    def weather_api_url(self) -> int:
        return pickle.loads(self.client.get("constance:WEATHER API URL"))

    @property
    def longitude(self) -> int:
        return pickle.loads(self.client.get("constance:LONGITUDE"))

    @property
    def latitude(self) -> int:
        return pickle.loads(self.client.get("constance:LATITUDE"))

    # endregion
