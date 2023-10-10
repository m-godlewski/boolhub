"""
Script used for monitoring data flowing over system.
Those methods checks if any of predefined conditions are met.
- unregistered device is connected to local network.
- temperature/aqi/humidity threshold became exceeded.
- diagnostic data of connected devices are incorrect.
If any of them are, notification are sent.
"""

import logging
import os
import sys
import traceback
import typing
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config
from scripts import messenger
from scripts.models.database import PostgreSQL


# constant values
DEVICE_HEALTH_KEYS = ("battery", "filter_life_remaining")
DEVICE_HEALTH_KEY_TRANSLATE_MAP = {"battery": "baterii", "filter": "filtra"}


def check_air(air_data: typing.List[typing.Any]) -> typing.List[str]:
    """Checks if air temperature, quality or humidity does not exceed defined thresholds in any of datasets.
    (For testing purposes only) Returns set of tuples, that informs about detected issues. If there was no
    issues, empty set will be returned.
    """
    try:

        # empty set of issues
        issues = set()

        # iterate over air devices data
        for data in air_data:
            # checks if air temperature exceeds threshold
            if (
                data.air_data.temperature
                and config.SCRIPTS["SENTRY"]["NOTIFIES"]["TEMPERATURE"]
                and (
                    data.air_data.temperature
                    >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"]["UP"]
                    or data.air_data.temperature
                    <= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["TEMPERATURE"][
                        "BOTTOM"
                    ]
                )
            ):
                messenger.send_notification(
                    text=f"Temperatura w {data.device_data.location} wynosi {data.air_data.temperature}°C"
                )
                issues.add(("temperature", data.device_data.location))
            # checks if air quality exceeds threshold
            if (
                data.air_data.aqi
                and config.SCRIPTS["SENTRY"]["NOTIFIES"]["AQI"]
                and data.air_data.aqi >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["AQI"]
            ):
                messenger.send_notification(
                    text=f"Jakość powietrza w {data.device_data.location} wynosi {data.air_data.aqi}μg/m³"
                )
                issues.add(("aqi", data.device_data.location))
            # checks if air humidity exceeds threshold
            if (
                data.air_data.humidity
                and config.SCRIPTS["SENTRY"]["NOTIFIES"]["HUMIDITY"]
                and (
                    data.air_data.humidity
                    >= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["UP"]
                    or data.air_data.humidity
                    <= config.SCRIPTS["SENTRY"]["THRESHOLDS"]["HUMIDITY"]["BOTTOM"]
                )
            ):
                messenger.send_notification(
                    text=f"Wilgotność powietrza w {data.device_data.location} wynosi {data.air_data.humidity}%"
                )
                issues.add(("humidity", data.device_data.location))

    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
    finally:
        return issues


def check_network(mac_addresses: typing.Set = {}) -> typing.List[str]:
    """Checks if following conditions are met:
    - number of connected devices to local network is more than predefined value.
    - unknown device has connected to local network.
    (For testing purposes only) Returns set of strings representing detected issues.
    If there is no issues, empty set will be returned.
    """
    try:

        # empty set of issues
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
            messenger.send_notification(
                text=f"Przeciążenie sieci! Liczba aktywnych urządzeń = {number_of_devices}"
            )
            issues.add("overload")

        # CHECKS IF UNKNOWN DEVICE HAS CONNECTED TO LOCAL NETWORK.
        # set of registered devices MAC addresses
        with PostgreSQL() as postgresql_database:
            known_devices = {device.mac_address for device in postgresql_database.devices}
        # set that contains unregistered devices MAC addresses
        unknown_devices = mac_addresses - known_devices
        # if above set contains any address
        if unknown_devices:
            # if notification flag is set to true
            if config.SCRIPTS["SENTRY"]["NOTIFIES"]["UNKNOWN_DEVICE"]:
                messenger.send_notification(
                    text="Nieznane urządzenie połączyło się z siecią lokalną!"
                )
            logging.warning(
                "SENTRY | Unknown device has connected to local network!"
            )
            issues.add("unknown_device")
            # checks if unknown addresses already exists in database
            with PostgreSQL() as postgresql_database:
                unknown_devices_mac_addresses = {device.mac_address for device in postgresql_database.unknown_devices}
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
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
    finally:
        return issues


def check_diagnostic(diagnostic_data: typing.List[dict]) -> typing.List[str]:
    """Verifies that the battery, filter or other consumable parts of the device
    are not at the end of their life.
    (For testing purposes only) Returns set of strings representing detected issues.
    If there is no issues, empty set will be returned.
    """
    try:

        # empty set of issues
        issues = set()

        # iteration over diagnostic data
        for data in diagnostic_data:
            # iterate over "health keys"
            for key in DEVICE_HEALTH_KEYS:
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
                        messenger.send_notification(
                            text=f"Poziom {DEVICE_HEALTH_KEY_TRANSLATE_MAP[key]} w urządzeniu {data['name']} w lokacji {data['location']} wynosi {data[key]}"
                        )
                        issues.add((key, data.device_data.location))

    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
    finally:
        return issues
