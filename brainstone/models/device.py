"""
This script contains dedicated classes for communication with IoT devices connected to system.
"""

import logging
import traceback
import typing
from abc import ABC
from dataclasses import fields

import bluepy
import miio
import miio.exceptions
import requests
from lywsd03mmc import Lywsd03mmcClient

from models.data import (
    DeviceData,
    MiAirPurifier3HData,
    MiMonitor2Data,
    OutsideVirtualThermometerData,
    ForecastData,
)
from .database import Redis


class Device(ABC):
    """Base class of each device class in this script."""

    def __init__(self, device_data: DeviceData) -> None:
        # device metadata
        self.metadata = device_data


class MiAirPurifier3H(Device):
    """Class used for communication with Xiaomi Mi Air Purifier 3H.
    https://mi-home.pl/products/mi-air-purifier-3h
    """

    def __init__(self, device_data: DeviceData) -> None:
        # calls super class constructor
        super().__init__(device_data)
        # fetches data object from device
        device_status = self.__fetch_data()
        # processes data retrieved from device to dataclass object
        self.__processed_data = self.__process_data(device_status)

    @property
    def data(self) -> dict:
        """Returns device air data."""
        return self.__processed_data

    def __fetch_data(self) -> miio.DeviceStatus:
        """Connects to device and fetches data."""
        try:
            logging.debug(f"Connecting to {self.metadata.ip_address}")
            # fetches data from device using miio library
            device = miio.AirPurifierMiot(
                ip=self.metadata.ip_address,
                token=self.metadata.token,
            )
            # retrieving data from device
            data = device.status()
        except miio.exceptions.DeviceException:
            logging.error(f"DEVICE | MiAirPurifier3H | UNABLE TO DISCOVER DEVICE")
            return miio.DeviceStatus()
        except Exception:
            logging.error(f"DEVICE | MiAirPurifier3H | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return miio.DeviceStatus()
        else:
            logging.debug(f"Connected to {self.metadata.ip_address}")
            return data

    def __parse(self, data) -> dict:
        """Parses data received from device into dictionary."""
        try:
            # dictionary that will store parsed dataset
            parsed_data = {}
            # iterates over device data properties
            for key, value in data.data.items():
                # filters out only fields that are used in target dataclass
                if key in [field.name for field in fields(MiAirPurifier3HData)]:
                    parsed_data[key] = value
        except Exception:
            logging.error(f"DEVICE | MiAirPurifier3H | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return {}
        else:
            return parsed_data

    def __process_data(self, raw_data: str) -> MiAirPurifier3HData:
        """Processes data from device and returns it as instance of dataclass."""
        try:
            # parses dataset
            parsed_data = self.__parse(raw_data)
            # create dataclass instance
            processed_data = MiAirPurifier3HData(self.metadata, **parsed_data)
        except Exception:
            logging.error(f"DEVICE | MiAirPurifier3H | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return MiAirPurifier3HData(self.metadata)
        else:
            return processed_data


class MiMonitor2(Device):
    """Class used for communication with Xiaomi Mi Monitor 2.
    https://mi-home.pl/products/mi-temperature-humidity-monitor-2
    """

    def __init__(self, device_data: DeviceData) -> None:
        # calls super class constructor
        super().__init__(device_data)
        raw_data = self.__fetch_data()
        self.__processed_data = self.__process_data(raw_data)

    @property
    def data(self) -> MiMonitor2Data:
        """Returns processed data."""
        return self.__processed_data

    def __fetch_data(self) -> dict:
        """Connects to device and fetches data."""
        try:
            # fetches data from device using external library
            client = Lywsd03mmcClient(self.metadata.mac_address)
            # converts data to dictionary
            data = client.data._asdict()
        except bluepy.btle.BTLEDisconnectError:
            logging.error("Error occurred when trying connect to device!")
            return {}
        except Exception:
            logging.error(f"DEVICE | MiMonitor2 | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return {}
        else:
            logging.debug(f"Connected to {self.metadata.mac_address}")
            return data

    def __process_data(self, raw_data: dict) -> MiMonitor2Data:
        """Processes raw data and returns it as instance of dataclass."""
        try:
            processed_data = MiMonitor2Data(self.metadata, **raw_data)
        except Exception:
            logging.error(f"DEVICE | MiMonitor2 | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return MiMonitor2Data(self.metadata)
        else:
            return processed_data


class OutsideVirtualThermometer(Device):
    """Class used for communication with external API (https://weatherapi.com) to fetch weather data."""

    def __init__(self, device_data: DeviceData, forecast: bool = False) -> None:
        # calls super class constructor
        super().__init__(device_data)
        # fetches weather data, if flag was set to False
        if not forecast:
            raw_data = self.__fetch_weather_data()
            self.__processed_data = self.__process_weather_data(raw_data)
        # otherwise, fetches forecast data
        else:
            raw_data = self.__fetch_forecast_data()
            self.__processed_data = self.__process_forecast_data(raw_data)

    @property
    def data(self) -> OutsideVirtualThermometerData:
        """Returns processed data."""
        return self.__processed_data

    # region FORECAST

    def __fetch_forecast_data(self) -> dict:
        """Connects to device and fetches data."""
        try:
            # connect to redis
            with Redis() as redis:
                # sending request to weather api
                response = requests.get(
                    url=f"{redis.weather_api_url}/forecast.json",
                    params={
                        "key": self.metadata.token,
                        "q": f"{redis.latitude}, {redis.longitude}",
                        "aqi": "yes",
                        "days": 3,
                    },
                )
            # if returned status code indicates external server error
            if response.status_code == 500:
                raise Exception("External Server Error!")
            # retrieving data in JSON format
            data = response.json()
        except Exception:
            logging.error(f"DEVICE | OutsideVirtualThermometer | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __process_forecast_data(self, raw_data: dict) -> typing.List[ForecastData]:
        """Processes raw data and returns it as instance of dataclass."""
        try:
            # empty list to store dataclass instances
            processed_data = []
            # list of daily forecasts
            forecast_data = raw_data.get("forecast").get("forecastday")
            # iterate over daily forecast
            for daily_forecast in forecast_data:
                # iterate over hourly forecast
                for hourly_forecast in daily_forecast.get("hour"):
                    # create forecast dataclass and append it to final list
                    processed_data.append(
                        ForecastData(
                            date=hourly_forecast.get("time"),
                            temperature=hourly_forecast.get("temp_c"),
                            humidity=hourly_forecast.get("humidity"),
                        )
                    )
        except Exception:
            logging.error(f"DEVICE | OutsideVirtualThermometer | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return []
        else:
            return processed_data

    # endregion

    # region WEATHER

    def __fetch_weather_data(self) -> dict:
        """Connects to device and fetches data."""
        try:
            # connect to redis
            with Redis() as redis:
                # sending request to weather api
                response = requests.get(
                    url=f"{redis.weather_api_url}/current.json",
                    params={
                        "key": self.metadata.token,
                        "q": f"{redis.latitude}, {redis.longitude}",
                        "aqi": "yes",
                    },
                )
            # if returned status code indicates external server error
            if response.status_code == 500:
                raise Exception("External Server Error!")
            # retrieving data in JSON format
            data = response.json()
        except Exception:
            logging.error(f"DEVICE | OutsideVirtualThermometer | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __process_weather_data(self, raw_data: dict) -> OutsideVirtualThermometerData:
        """Processes raw data and returns it as instance of dataclass."""
        try:
            data = {
                "temperature": raw_data.get("current").get("temp_c"),
                "humidity": raw_data.get("current").get("humidity"),
                "aqi": max(
                    round(raw_data.get("current").get("air_quality").get("pm2_5")), 1
                ),
            }
            processed_data = OutsideVirtualThermometerData(self.metadata, **data)
        except Exception:
            logging.error(f"DEVICE | OutsideVirtualThermometer | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
            return MiMonitor2Data(self.metadata)
        else:
            return processed_data

    # endregion
