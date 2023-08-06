"""
Script used for monitoring data flowing over system.
"""

import logging
import os
import sys
import traceback
from typing import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config
from messenger import Messenger
from models.database import PostgreSQL


class Sentry:
    """This class methods checks if any of predefined conditions are met.
    If any of them are, notification are sent.
    - unregistered device is connected to local network.
    - temperature/aqi/humidity threshold became exceeded.
    """

    DEVICE_HEALTH_KEYS = ("battery", "filter")
    DEVICE_HEALTH_KEY_TRANSLATE_MAP = {"battery": "baterii", "filter": "filtra"}

    def __init__(self, data_type: str, dataset: Any) -> None:
        """Verifies dataset base on data source."""
        if data_type == "network":
            self.__check_network(mac_addresses=dataset)
        if data_type == "air":
            self.__check_air(air_data=dataset)
        if data_type == "diagnostic":
            self.__check_diagnostic(diagnostical_data=dataset)

    def __check_air(self, air_data: List[dict]) -> None:
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

    def __check_network(self, mac_addresses: Set = {}) -> None:
        """Verifies if there is no unregistered device MAC address
        in set of gatherec MAC addresses by gatherer script.
        """
        try:
            # numer of active devices in local network
            number_of_devices = len(mac_addresses)
            # set of registered devices MAC addresses
            known_devices = self.__get_known_devices_mac_addresses()
            # set that contains unregistered devices MAC addresses
            unknown_devices = mac_addresses - known_devices
            # if above set contains any address and notification flag is set to True
            if unknown_devices:
                with PostgreSQL() as postgresql_database:
                    # checks if unknown address already exists in database
                    postgresql_database.execute("SELECT * FROM unknown_devices;")
                    query_result = [row for row in postgresql_database.fetchall()]
                    # if not, inserts new mac address to database
                    if not query_result:
                        # saves unknown address to postgresql database
                        for address in unknown_devices:
                            postgresql_database.execute(
                                "INSERT INTO unknown_devices(mac_address) VALUES(%s);",
                                (address,)
                            )
                        if config.SCRIPTS["SENTRY"]["NOTIFIES"]["UNKNOWN_DEVICE"]:
                            logging.warning(
                                "SENTRY | Unknown device has connected to local network!"
                            )
                            Messenger.send_notification(
                                text="Nieznane urządzenie połączyło się z siecią lokalną!"
                            )
            # if number of active devices in local network is equal or higher than predefined value
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
        except Exception:
            logging.error(f"Unknown error occured!\n{traceback.format_exc()}")

    def __check_diagnostic(self, diagnostical_data: List[dict]):
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

    def __get_known_devices_mac_addresses(self) -> Set[str]:
        """Makes query to postgre database and returns set of registered MAC addresses."""
        with PostgreSQL() as postgresql_database:
            postgresql_database.execute("SELECT mac_address FROM devices_device;")
            return {mac_address[0] for mac_address in postgresql_database.fetchall()}
