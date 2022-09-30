"""
Script responsible for detecting suspicious behaviours of system.
"""

import sqlite3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from typing import *

import config


class Sentry:
    """Checks if there are any unknown devices in local network.
    In case unknown device, message to system administrator are send.
    """

    def __init__(self, mac_addresses_list: Set={}):
        """Creates connection to sqlite3 database and
        verifies received list of mac addresses."""
        # create connection with local sqlite3 database
        self.database_client = sqlite3.connect(config.DB["SQLITE"]["PATH"])
        self.database_api = self.database_client.cursor()
        # retrieves mac addresses of known devices from database
        known_devices = self.__get_devices_mac_addresses()
        # checks if there are unknown addresses in received set
        unknown_devices = mac_addresses_list - known_devices
        # in case of unknown device
        if unknown_devices:
            # TODO add some if statement to avoid spamming
            print("unknown device found, messaging placeholder log!")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Closes connection to sqlite3 database"""
        self.database_client.close()

    def __get_devices_mac_addresses(self) -> Set[str]:
        """Return list of mac addresses of registered devices."""
        return {
            mac_address[0]
            for mac_address
            in self.database_api.execute("SELECT mac_address FROM devices_device;")
        }
