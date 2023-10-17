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
from lywsd03mmc import Lywsd03mmcClient

from scripts.models.data import DeviceData, MiAirPurifier3HData, MiMonitor2Data


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
            self.__type_conversion(data.split(":")[1].strip().split(" ")[0])
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
