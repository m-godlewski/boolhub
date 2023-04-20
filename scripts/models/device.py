"""
This script contains dedicated classes for comunication with each IoT device connected to system.
"""

import logging
import os
import traceback
import typing
from abc import ABC


class Device(ABC):
    """Base class of each device class in this script."""

    def __init__(self, ip_address: str, mac_address: str) -> None:
        """Initializing class object by assigning ip and mac addresses."""
        self.ip_address = ip_address
        self.mac_address = mac_address


class MiAirPurifier3H(Device):
    """Class used for communication with Xiaomi Mi Air Purifier 3H."""

    # sets of keys for device health and air data
    HEALTH_KEYS = (
        "filter_life_remaining",
        "filter_hours_used",
        "filter_left_time",
        "use_time",
        "purify_volume",
    )
    AIR_DATA_KEYS = ("aqi", "humidity", "temperature")

    def __init__(self, ip_address: str, mac_address: str, token: str) -> None:
        """Class constructor."""
        super().__init__(ip_address, mac_address)
        self.token = token
        self.__raw_data = self.__fetch_data()
        self.__data = self.__process_data()

    @property
    def data(self) -> dict:
        """Returns processed air data from device."""
        return dict(
            [
                (key, value)
                for key, value in self.__data.items()
                if key in self.AIR_DATA_KEYS
            ]
        )

    @property
    def health(self) -> dict:
        """Returns processed health data of device."""
        return dict(
            [
                (key, value)
                for key, value in self.__data.items()
                if key in self.HEALTH_KEYS
            ]
        )

    def __fetch_data(self) -> dict:
        """Connects to device and fetches data."""
        try:
            # fetching data from device using miiocli shell command
            # TODO - shell command fetching should be replaced by python library
            data = os.popen(
                f"miiocli airpurifiermiot \
                --ip \{self.ip_address} \
                --token {self.token} \
                status"
            ).read()
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __process_data(self) -> dict:
        """Processes raw data and returns it in form of structured dataset."""
        try:
            # dictionary that will store processed data
            data = {}
            # splits received string by newline chars
            raw_data = self.__raw_data.strip().split("\n")
            # iterates over dataset
            for row in raw_data:
                # parse single row of data
                key, value = self.__parse(row)
                # converts data types of dictionary values
                data[key] = self.__type_conversion(value)
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
            return {}
        else:
            return data

    def __parse(self, data: str) -> str:
        """Parses single line of raw data from dataset and returns it's processed form."""
        return (
            data.split(":")[0].lower().replace(" ", "_"),
            data.split(":")[1].strip().split(" ")[0],
        )

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
