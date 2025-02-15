"""
This script contains dedicated classes for communication with IoT devices connected to system.
"""

import logging
import traceback
import typing
from abc import ABC, abstractmethod
from dataclasses import fields

import bluepy
import miio
import miio.exceptions
from lywsd03mmc import Lywsd03mmcClient

from models.data import (
    DeviceData,
    MiAirPurifier3HData,
    MiMonitor2Data,
)


class Device(ABC):
    """Base class of each device class in this script."""

    def __init__(self, device_data: DeviceData) -> None:
        # device metadata
        self.metadata = device_data
        # fetching raw data from device
        self.raw_data = self.fetch()
        # processing raw data
        self.processed_data = self.process_data()

    @property
    def data(self) -> DeviceData:
        """Returns processed data."""
        return self.processed_data

    @abstractmethod
    def fetch(self) -> typing.Any:
        """Should implements the logic of fetching data from device."""
        pass

    @abstractmethod
    def process_data(self) -> DeviceData:
        """Should implements the logic of processing raw data from the device into structured one."""
        pass


class MiAirPurifier3H(Device):
    """Class used for communication with Xiaomi Mi Air Purifier 3H.
    https://mi-home.pl/products/mi-air-purifier-3h
    """

    def fetch(self) -> miio.DeviceStatus:
        """Connects to device and fetches data."""
        try:
            logging.debug(
                f"DEVICE | MiAirPurifier3H | Connecting to {self.metadata.ip_address}"
            )
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
            logging.error(
                f"DEVICE | MiAirPurifier3H | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return miio.DeviceStatus()
        else:
            logging.debug(
                f"DEVICE | MiAirPurifier3H | Connected to {self.metadata.ip_address}"
            )
            return data

    def process_data(self) -> MiAirPurifier3HData:
        """Processes data from device and returns it as instance of dataclass."""
        try:
            # parses dataset
            parsed_data = self.__parse(self.raw_data)
            # create dataclass instance
            processed_data = MiAirPurifier3HData(self.metadata, **parsed_data)
        except Exception:
            logging.error(
                f"DEVICE | MiAirPurifier3H | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return MiAirPurifier3HData(self.metadata)
        else:
            return processed_data

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
            logging.error(
                f"DEVICE | MiAirPurifier3H | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return {}
        else:
            return parsed_data


class MiMonitor2(Device):
    """Class used for communication with Xiaomi Mi Monitor 2.
    https://mi-home.pl/products/mi-temperature-humidity-monitor-2
    """

    def fetch(self) -> dict:
        """Connects to device and fetches data."""
        try:
            logging.debug(
                f"DEVICE | MiMonitor2 | Connecting to {self.metadata.ip_address}"
            )
            # fetches data from device using external library
            client = Lywsd03mmcClient(self.metadata.mac_address)
            # converts data to dictionary
            data = client.data._asdict()
        except bluepy.btle.BTLEDisconnectError:
            logging.error("Error occurred when trying connect to device!")
            return {}
        except Exception:
            logging.error(
                f"DEVICE | MiMonitor2 | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return {}
        else:
            logging.debug(
                f"DEVICE | MiMonitor2 | Connected to {self.metadata.ip_address}"
            )
            return data

    def process_data(self) -> MiMonitor2Data:
        """Processes raw data and returns it as instance of dataclass."""
        try:
            processed_data = MiMonitor2Data(self.metadata, **self.raw_data)
        except Exception:
            logging.error(
                f"DEVICE | MiMonitor2 | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
            )
            return MiMonitor2Data(self.metadata)
        else:
            return processed_data
