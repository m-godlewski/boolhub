"""
This script contains dedicated classes for communication with IoT devices connected to system.
"""

import logging
import os
import traceback
import typing
from abc import ABC
from dataclasses import fields

import bluepy
import requests
from lywsd03mmc import Lywsd03mmcClient

import config
from scripts.models.data import (
    DeviceData,
    MiAirPurifier3HData,
    MiMonitor2Data,
    OutsideVirtualThermometerData,
    ForecastData,
)


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
        # fetches raw data from device
        raw_data = self.__fetch_data()
        # processes raw data
        self.__processed_data = self.__process_data(raw_data)

    @property
    def data(self) -> dict:
        """Returns device air data."""
        return self.__processed_data

    def __fetch_data(self) -> MiAirPurifier3HData:
        """Connects to device and fetches data."""
        try:
            # fetching data from device using miiocli shell command
            # TODO - shell command fetching should be replaced by python library
            data = os.popen(
                f"miiocli airpurifiermiot \
                --ip \{self.metadata.ip_address} \
                --token {self.metadata.token} \
                status"
            ).read()
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return ""
        else:
            return data

    def __parse(self, data: str) -> dict:
        """Parses raw dataset and returns it's processed form."""
        try:
            # dictionary that will store parsed dataset
            parsed_data = {}
            # iterates over dataset
            for row in data:
                # parse single row of data
                key, value = self.__parse_row(row)
                # if current key is an field in dataclass
                if key in [field.name for field in fields(MiAirPurifier3HData)]:
                    parsed_data[key] = value
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return {}
        else:
            return parsed_data

    def __parse_row(self, data: str) -> typing.Union[str, typing.Any]:
        """Parses single line of raw data from dataset and returns it's processed form."""
        return (
            data.split(":")[0].lower().replace(" ", "_"),
            self.__type_conversion(data.split(":")[1].strip().split(" ")[0]),
        )

    def __process_data(self, raw_data: str) -> MiAirPurifier3HData:
        """Processes raw data and returns it as instance of dataclass."""
        try:
            # splits received string by newline chars
            raw_data = raw_data.strip().split("\n")
            # prase dataset
            parsed_data = self.__parse(raw_data)
            # create dataclass instance
            processed_data = MiAirPurifier3HData(self.metadata, **parsed_data)
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return MiAirPurifier3HData(self.metadata)
        else:
            return processed_data

    def __type_conversion(self, value: str) -> typing.Any:
        """Converts data from individual fields in a dataset."""
        # integer
        if value.isdigit():
            return int(value)
        # float
        elif "." in value:
            try:
                return float(value)
            except:
                return value
        # boolean
        elif value == "False" or value == "True":
            return bool(value)
        # none
        elif value == "None":
            return None
        # device on/off status
        elif value == "on":
            return True
        elif value == "off":
            return False
        else:
            return value


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
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __process_data(self, raw_data: dict) -> MiMonitor2Data:
        """Processes raw data and returns it as instance of dataclass."""
        try:
            processed_data = MiMonitor2Data(self.metadata, **raw_data)
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
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
            # sending request to weather api
            response = requests.get(
                url=f"{config.SCRIPTS['GATHERER']['VIRTUAL_THERMOMETER']['API_URL']}/forecast.json",
                params={
                    "key": self.metadata.token,
                    "q": f"{config.SCRIPTS['GATHERER']['VIRTUAL_THERMOMETER']['LATITUDE']}, {config.SCRIPTS['GATHERER']['VIRTUAL_THERMOMETER']['LONGITUDE']}",
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
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
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
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return []
        else:
            return processed_data

    # endregion

    # region WEATHER

    def __fetch_weather_data(self) -> dict:
        """Connects to device and fetches data."""
        try:
            # sending request to weather api
            response = requests.get(
                url=f"{config.SCRIPTS['GATHERER']['VIRTUAL_THERMOMETER']['API_URL']}/current.json",
                params={
                    "key": self.metadata.token,
                    "q": f"{config.SCRIPTS['GATHERER']['VIRTUAL_THERMOMETER']['LATITUDE']}, {config.SCRIPTS['GATHERER']['VIRTUAL_THERMOMETER']['LONGITUDE']}",
                    "aqi": "yes",
                },
            )
            # if returned status code indicates external server error
            if response.status_code == 500:
                raise Exception("External Server Error!")
            # retrieving data in JSON format
            data = response.json()
        except Exception:
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
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
            logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
            return MiMonitor2Data(self.metadata)
        else:
            return processed_data

    # endregion
