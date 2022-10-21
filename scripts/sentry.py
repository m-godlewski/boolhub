"""
Script responsible for detecting suspicious behaviours of system.
"""

import sqlite3
import os
import sys
from typing import *

import config
from messenger import Messenger


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


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
                data.get("temperature") <= 20.0
                and config.SCRIPTS["MESSENGER"]["TEMPERATURES"]
            ):
                Messenger.send_notification(
                    text=f"W pomieszczeniu {data.get('location')} jest {data.get('temperature')}"
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
        if unknown_devices and config.SCRIPTS["MESSENGER"]["UNKNOWN_DEVICES"]:
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
