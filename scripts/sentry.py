"""
Script used for monitoring data flowing over system.
"""

import logging
import os
import sys
import traceback
from typing import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import sqlite3

import config
from messenger import Messenger


class Sentry:
    """This class methods checks if any of predefined conditions are met.
    If any of them are, notification are sent.
    - unregistered device is connected to local network.
    - temperature/aqi/humidity threshold became exceeded.
    """

    def __init__(self, data_type: str, dataset: Any) -> None:
        """Creates connection to sqlite database and
        calls proper method depends on 'data' argument.
        """
        # create connection with local sqlite3 database
        self.database_client = sqlite3.connect(config.DATABASE["SQLITE"]["PATH"])
        self.database_api = self.database_client.cursor()
        # verifies dataset base on data source
        if data_type == "network":
            self.__check_network(mac_addresses=dataset)
        if data_type == "air":
            self.__check_air(air_data=dataset)

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes connection to sqlite3 database"""
        self.database_api.close()
        self.database_client.close()

    def __check_air(self, air_data: List[dict]) -> None:
        """Checks if air temperature, quality or humidity does not exceed defined tresholds in any of datasets."""
        try:
            # iterate over air devices data
            for data in air_data:
                # checks if air temperature exceeds threshold
                if (
                    data.get("temperature")
                    and config.SCRIPTS["SENTRY"]["NOTIFIES"]["TEMPERATURE"]
                    and data.get("temperature") <= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]
                ):
                    Messenger.send_notification(
                        text=f"Temperatura w {data.get('location')} wynosi {data.get('temperature')}°C"
                    )
                # checks if air quality exceeds threshold
                if (
                    data.get("aqi")
                    and config.SCRIPTS["SENTRY"]["NOTIFIES"]["AQI"]
                    and data.get("aqi") >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["AQI"]
                ):
                    Messenger.send_notification(
                        text=f"Jakość powietrza w {data.get('location')} wynosi {data.get('aqi')}μg/m³"
                    )
                # checks if air humidity exceeds threshold
                if (
                    data.get("humidity")
                    and config.SCRIPTS["SENTRY"]["NOTIFIES"]["HUMIDITY"]
                    and (data.get("humidity") >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["UP"]
                        or data.get("humidity") <= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["BOTTOM"])
                ):
                    Messenger.send_notification(
                        text=f"Wilgotność powietrza w {data.get('location')} wynosi {data.get('humidity')}%"
                    )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")

    def __check_network(self, mac_addresses: Set = {}) -> None:
        """Verifies if there is no unregistered device MAC address
        in set of gatherec MAC addresses by gatherer script.
        """
        try:
            # set of registered devices MAC addresses
            known_devices = self.__get_known_devices_mac_addresses ()
            # set that contains unregistered devices MAC addresses
            unknown_devices = mac_addresses - known_devices
            # if above set contains any address and notification flag is set to True
            if unknown_devices and config.SCRIPTS["SENTRY"]["NOTIFIES"]["UNKNOWN_DEVICE"]:
                # TODO add some if statement to avoid spamming
                logging.warning("SENTRY | Unknown device has connected to local network!")
                Messenger.send_notification(
                    text="Nieznane urządzenie połączyło się z siecią lokalną!"
                )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")

    def __get_known_devices_mac_addresses(self) -> Set[str]:
        """Makes query to sqlite database and returns set of registered MAC addresses."""
        return {
            mac_address[0]
            for mac_address in self.database_api.execute(
                "SELECT mac_address FROM devices_device;"
            )
        }
