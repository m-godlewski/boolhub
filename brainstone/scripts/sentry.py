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

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import messenger
from models.database import PostgreSQL


# constant values
DEVICE_HEALTH_KEY_TRANSLATE_MAP = {
    "battery": "baterii",
    "filter_life_remaining": "filtra",
}


def check_air(air_data: typing.List[typing.Any]) -> typing.Set[str]:
    """Checks if air temperature, quality or humidity does not exceed defined thresholds in any of datasets.
    (For testing purposes only) Returns set of tuples, that informs about detected issues. If there was no
    issues, empty set will be returned.
    """
    try:

        logging.debug(f"DATABASE | SENTRY | Air data verification")

        # empty set of issues
        issues = set()

        # establish connection to settings database
        with PostgreSQL(settings=True) as postgresql_database:
            # current settings
            settings = postgresql_database.settings
            # iterate over air devices data
            for data in air_data:
                # checks if air temperature exceeds threshold
                if (
                    data.temperature
                    and settings.get("notify_temperature")
                    and (
                        data.temperature >= settings.get("temperature_max")
                        or data.temperature <= settings.get("temperature_min")
                    )
                ):
                    messenger.send_notification(
                        text=f"Temperatura wynosi {data.temperature}°C",
                        title=data.device.location.capitalize(),
                        priority=3,
                    )
                    issues.add(("temperature", data.device.location))
                # checks if air quality exceeds threshold
                if (
                    data.aqi
                    and settings.get("notify_aqi")
                    and data.aqi >= settings.get("aqi_threshold")
                ):
                    messenger.send_notification(
                        text=f"Jakość powietrza wynosi {data.aqi}μg/m³",
                        title=data.device.location.capitalize(),
                        priority=3,
                    )
                    issues.add(("aqi", data.device.location))
                # checks if air humidity exceeds threshold
                if (
                    data.humidity
                    and settings.get("notify_humidity")
                    and (
                        data.humidity >= settings.get("humidity_max")
                        or data.humidity <= settings.get("humidity_min")
                    )
                ):
                    messenger.send_notification(
                        text=f"Wilgotność powietrza wynosi {data.humidity}%",
                        title=data.device.location.capitalize(),
                        priority=3,
                    )
                    issues.add(("humidity", data.device.location))

    except Exception:
        logging.error(f"SENTRY | AIR | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
    finally:
        logging.debug(f"DATABASE | SENTRY | Air data verified")
        return issues


def check_network(mac_addresses: typing.Set = {}) -> typing.Set[str]:
    """Checks if following conditions are met:
    - number of connected devices to local network is more than predefined value.
    - unknown device has connected to local network.
    (For testing purposes only) Returns set of strings representing detected issues.
    If there is no issues, empty set will be returned.
    """
    try:

        logging.debug(f"DATABASE | SENTRY | Network data verification")

        # empty set of issues
        issues = set()

        # establish connection to settings database
        with PostgreSQL(settings=True) as postgresql_database:

            # current settings
            settings = postgresql_database.settings

            # checks if number of connected devices to local network is more than predefined value
            # number of active devices in local network
            number_of_devices = len(mac_addresses)
            # if number of active devices is equal or higher than predefined value
            if settings.get(
                "notify_network_overload"
            ) and number_of_devices >= settings.get("network_overload_threshold"):
                logging.warning(
                    f"SENTRY | Network overload! Number of active devices = {number_of_devices}"
                )
                messenger.send_notification(
                    text=f"Liczba aktywnych urządzeń = {number_of_devices}",
                    title="Sieć",
                    priority=2,
                )
                issues.add("overload")

            # checks if unknown device has connected to local network
            # set of registered devices MAC addresses
            known_devices = {
                device.mac_address for device in postgresql_database.devices
            }
            # set that contains unregistered devices MAC addresses
            unknown_devices = mac_addresses - known_devices
            # if above set contains any address
            if unknown_devices:
                # if notification flag is set to true
                if settings.get("notify_unknown_device"):
                    messenger.send_notification(
                        text="Nieznane urządzenie jest podłączone do sieci lokalnej",
                        title="Sieć",
                        priority=4,
                    )
                    issues.add("unknown_device")
                logging.warning(
                    "SENTRY | Unknown device is connected to local network!"
                )
                # adds unknown device to database
                for address in unknown_devices:
                    postgresql_database.add_unknown_device(address)

    except Exception:
        logging.error(
            f"SENTRY | NETWORK | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
        )
    finally:
        logging.debug(f"DATABASE | SENTRY | Network data verified")
        return issues


def check_diagnostic(diagnostic_data: typing.List[typing.Any]) -> typing.Set[str]:
    """Verifies that the battery, filter or other consumable parts of the device
    are not at the end of their life.
    (For testing purposes only) Returns set of strings representing detected issues.
    If there is no issues, empty set will be returned.
    """
    try:

        logging.debug(f"DATABASE | SENTRY | Diagnostic data verification")

        # empty set of issues
        issues = set()

        # establish connection to settings database
        with PostgreSQL(settings=True) as postgresql_database:
            # current settings
            settings = postgresql_database.settings
            # iteration over diagnostic data
            for data in diagnostic_data:
                # iterate over health fields
                for field, value in data.health_data.items():
                    # if consumable part level exceeds predefined level
                    if (
                        settings.get("notify_health")
                        and value
                        and value <= settings.get("health_threshold")
                    ):
                        logging.warning(
                            f"SENTRY | Level of {field} in device {data.device.name} in location {data.device.location} is {value}"
                        )
                        messenger.send_notification(
                            text=f"Poziom {DEVICE_HEALTH_KEY_TRANSLATE_MAP[field]} wynosi {value}",
                            title=f"{data.device.name} - {data.device.location}",
                            priority=4,
                        )
                        issues.add((field, data.device.location))

    except Exception:
        logging.error(
            f"SENTRY | DIAGNOSTIC | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}"
        )
    finally:
        logging.debug(f"DATABASE | SENTRY | Diagnostic data verified")
        return issues
