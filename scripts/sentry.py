"""
Script used for monitoring data flowing over system.
"""

import logging
import os
import sys
import traceback
from datetime import datetime
from typing import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config
from scripts.messenger import Messenger
from scripts.models.database import PostgreSQL


class Sentry:
    """This class methods checks if any of predefined conditions are met.
    - unregistered device is connected to local network.
    - temperature/aqi/humidity threshold became exceeded.
    - diagnostic data of connected devies are incorrect.
    If any of them are, notification are sent.
    """

    DEVICE_HEALTH_KEYS = ("battery", "filter")
    DEVICE_HEALTH_KEY_TRANSLATE_MAP = {"battery": "baterii", "filter": "filtra"}

    @classmethod
    def check_air(self, air_data: List[dict]) -> None:
        """Checks if air temperature, quality or humidity does not exceed defined tresholds in any of datasets."""
        try:
            # iterate over air devices data
            for data in air_data:
                # checks if air temperature exceeds threshold
                if (
                    data.get("temperature")
                    and config.SCRIPTS["SENTRY"]["NOTIFIES"]["TEMPERATURE"]
                    and (
                        data.get("temperature")
                        >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]["UP"]
                        or data.get("temperature")
                        <= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"][
                            "BOTTOM"
                        ]
                    )
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
                    and (
                        data.get("humidity")
                        >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["UP"]
                        or data.get("humidity")
                        <= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["BOTTOM"]
                    )
                ):
                    Messenger.send_notification(
                        text=f"Wilgotność powietrza w {data.get('location')} wynosi {data.get('humidity')}%"
                    )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")

    @classmethod
    def check_network(self, mac_addresses: Set = {}) -> List[str]:
        """Checks if following conditions are met:
        - number of connected devices to local network is more than predefined value.
        - unknown device has connected to local network.
        (For testing purposes only) Returns set of strings representing detected issues.
        If there is no issues, empty set will be returned.
        """
        try:

            # set of issues initialization
            issues = set()

            # CHECKS IF NUMBER OF CONNECTED DEVICES TO LOCAL NETWORK IS MORE THAN PREDEFINED VALUE.
            # number of active devices in local network
            number_of_devices = len(mac_addresses)
            # if number of active devices is equal or higher than predefined value
            if (
                config.SCRIPTS["SENTRY"]["NOTIFIES"]["NETWORK_OVERLOAD"]
                and number_of_devices
                >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["MAX_NUMBER_OF_DEVICES"]
            ):
                logging.warning(
                    f"SENTRY | Network overload! Number of active devices = {number_of_devices}"
                )
                Messenger.send_notification(
                    text=f"Przeciążenie sieci! Liczba aktywnych urządzeń = {number_of_devices}"
                )
                issues.add("overload")

            # CHECKS IF UNKNOWN DEVICE HAS CONNECTED TO LOCAL NETWORK.
            # set of registered devices MAC addresses
            with PostgreSQL() as postgresql_database:
                known_devices = postgresql_database.known_devices_mac_addresses()
            # set that contains unregistered devices MAC addresses
            unknown_devices = mac_addresses - known_devices
            # if above set contains any address
            if unknown_devices:
                # if notification flag is set to true
                if config.SCRIPTS["SENTRY"]["NOTIFIES"]["UNKNOWN_DEVICE"]:
                    Messenger.send_notification(
                        text="Nieznane urządzenie połączyło się z siecią lokalną!"
                    )
                logging.warning(
                    "SENTRY | Unknown device has connected to local network!"
                )
                issues.add("unknown_device")
                # checks if unknown addresses already exists in database
                with PostgreSQL() as postgresql_database:
                    unknown_devices_mac_addresses = postgresql_database.unknown_devices_mac_addresses()
                    for address in unknown_devices:
                        # if not, inserts new mac address to database
                        if address not in unknown_devices_mac_addresses:
                            postgresql_database.api.execute(
                                "INSERT INTO unknown_devices(mac_address, last_time) VALUES(%s, %s);",
                                (address, datetime.now(),)
                            )
                        # otherwise update 'last_time' column
                        else:
                            postgresql_database.api.execute(
                                "UPDATE unknown_devices SET last_time = %s WHERE mac_address = %s;",
                                (datetime.now(), address,)
                            )

        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
        finally:
            return issues

    @classmethod
    def check_diagnostic(self, diagnostical_data: List[dict]) -> None:
        """Verifies that the battery, filter or other consumable parts of the device are not at the end of their life."""
        try:
            # iteration over diagnostical data
            for data in diagnostical_data:
                # iterate over "health keys"
                for key in self.DEVICE_HEALTH_KEYS:
                    # if consumable part level exceeds predefined level
                    if key in data:
                        if (
                            config.SCRIPTS["SENTRY"]["NOTIFIES"]["DIAGNOSTICS"]
                            and data[key]
                            <= config.SCRIPTS["SENTRY"]["THRESHOLDS"][
                                "BATTERY_FILTER_LEVEL"
                            ]
                        ):
                            logging.warning(
                                f"SENTRY | Level of {key} in device {data['name']} in location {data['location']} is {data[key]}"
                            )
                            Messenger.send_notification(
                                text=f"Poziom {self.DEVICE_HEALTH_KEY_TRANSLATE_MAP[key]} w urządzeniu {data['name']} w lokacji {data['location']} wynosi {data[key]}"
                            )
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")
