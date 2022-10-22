"""
Script responsible for detecting suspicious behaviours of system.
"""

import sqlite3
import os
import sys
from typing import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config
from messenger import Messenger


class Sentry:
    """Checks if any of predefined alarm conditions are met.
    If any of them are, notification are sent.
    - unregistered device is connected to local network.
    - temperature/aqi/humidity threshold became exceeded.
    """

    def __init__(self, data: str, dataset: Any) -> None:
        """Creates connection to sqlite3 database and
        calls proper method depends on 'data' argument.
        """
        # create connection with local sqlite3 database
        self.database_client = sqlite3.connect(config.DB["sqlite"]["path"])
        self.database_api = self.database_client.cursor()
        # verifies dataset base on data source
        if data == "network":
            self.__check_network(mac_addresses=dataset)
        if data == "air":
            self.__check_air(air_data=dataset)

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Closes connection to sqlite3 database"""
        self.database_client.close()

    def __check_air(self, air_data: List[dict]) -> None:
        """Checks if air temperature, quality or humidity does not exceed defined tresholds in any of rooms."""
        # iterate over air devices data
        for data in air_data:
            # checks if air temperature exceeds threshold
            if (
                config.SCRIPTS["MESSENGER"]["NOTIFIES"]["TEMPERATURE"]
                and data.get("temperature") <= config.SCRIPTS["MESSENGER"]["THRESHOLDS"]["TEMPERATURE"]
            ):
                Messenger.send_notification(
                    text=f"Temperatura w pomieszczeniu {data.get('location')} wynosi {data.get('temperature')}°C"
                )
            # checks if air quality exceeds threshold
            if (
                data.get("aqi")
                and config.SCRIPTS["MESSENGER"]["NOTIFIES"]["AQI"]
                and data.get("aqi") >= config.SCRIPTS["MESSENGER"]["THRESHOLDS"]["AQI"]
            ):
                Messenger.send_notification(
                    text=f"Jakość powietrza w pomieszczeniu {data.get('location')} wynosi {data.get('aqi')}μg/m³"
                )
            # checks if air humidity exceeds threshold
            if (
                data.get("humidity")
                and config.SCRIPTS["MESSENGER"]["NOTIFIES"]["HUMIDITY"]
                and (data.get("humidity") >= config.SCRIPTS["MESSENGER"]["THRESHOLDS"]["HUMIDITY"]["UP"]
                    or data.get("humidity") <= config.SCRIPTS["MESSENGER"]["THRESHOLDS"]["HUMIDITY"]["BOTTOM"])
            ):
                Messenger.send_notification(
                    text=f"Wilgotność powietrza w pomieszczeniu {data.get('location')} wynosi {data.get('humidity')}%"
                )

    def __check_network(self, mac_addresses: Set = {}) -> None:
        """Verifies if there is no unregistered device MAC address
        in set of gatherec MAC addresses by gatherer script.
        """
        # set of registered devices MAC addresses
        known_devices = self.__get_devices_mac_addresses()
        # set that contains unregistered devices MAC addresses
        unknown_devices = mac_addresses - known_devices
        # if above set contains any address and notification flag is set to True
        if unknown_devices and config.SCRIPTS["MESSENGER"]["NOTIFIES"]["UNKNOWN_DEVICE"]:
            # TODO add some if statement to avoid spamming
            Messenger.send_notification(
                text="Nieznane urządzenie połączyło się z siecią lokalną!"
            )

    def __get_devices_mac_addresses(self) -> Set[str]:
        """Makes query to sqlite database and returns set of registered MAC addresses."""
        return {
            mac_address[0]
            for mac_address in self.database_api.execute(
                "SELECT mac_address FROM devices_device;"
            )
        }
