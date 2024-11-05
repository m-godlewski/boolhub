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
from models.database import PostgreSQL, Redis


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
        # establish connection to Redis
        with Redis() as redis:
            # empty set of issues
            issues = set()

            # iterate over air devices data
            for data in air_data:
                # checks if air temperature exceeds threshold
                if (
                    data.temperature
                    and redis.notify_temperatue
                    and (
                        data.temperature >= redis.notify_temperatue_upper
                        or data.temperature <= redis.notify_temperatue_lower
                    )
                ):
                    messenger.send_notification(
                        text=f"Temperatura wynosi {data.temperature}°C",
                        title=data.device.location.capitalize(),
                        priority=3,
                    )
                    issues.add(("temperature", data.device.location))
                # checks if air quality exceeds threshold
                if data.aqi and redis.notify_aqi and data.aqi >= redis.notify_aqi_max:
                    messenger.send_notification(
                        text=f"Jakość powietrza wynosi {data.aqi}μg/m³",
                        title=data.device.location.capitalize(),
                        priority=3,
                    )
                    issues.add(("aqi", data.device.location))
                # checks if air humidity exceeds threshold
                if (
                    data.humidity
                    and redis.notify_humidity
                    and (
                        data.humidity >= redis.notify_humidity_upper
                        or data.humidity <= redis.notify_humidity_lower
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
        return issues


def check_network(mac_addresses: typing.Set = {}) -> typing.Set[str]:
    """Checks if following conditions are met:
    - number of connected devices to local network is more than predefined value.
    - unknown device has connected to local network.
    (For testing purposes only) Returns set of strings representing detected issues.
    If there is no issues, empty set will be returned.
    """
    try:
        # establish connection to Redis
        with Redis() as redis:
            # empty set of issues
            issues = set()

            # CHECKS IF NUMBER OF CONNECTED DEVICES TO LOCAL NETWORK IS MORE THAN PREDEFINED VALUE.
            # number of active devices in local network
            number_of_devices = len(mac_addresses)
            # if number of active devices is equal or higher than predefined value
            if (
                redis.notify_network_overload
                and number_of_devices >= redis.notify_network_overload_level
            ):
                logging.warning(
                    f"SENTRY | Network overload! Number of active devices = {number_of_devices}"
                )
                messenger.send_notification(
                    text=f"Liczba aktywnych urządzeń = {number_of_devices}",
                    title="Sieć",
                    priority=2,
                )
                issues.add("overload")

            # CHECKS IF UNKNOWN DEVICE HAS CONNECTED TO LOCAL NETWORK.
            # set of registered devices MAC addresses
            with PostgreSQL() as postgresql_database:
                known_devices = {
                    device.mac_address for device in postgresql_database.devices
                }
                # set that contains unregistered devices MAC addresses
                unknown_devices = mac_addresses - known_devices
                # if above set contains any address
                if unknown_devices:
                    # if notification flag is set to true
                    if redis.notify_network_unknown_device:
                        messenger.send_notification(
                            text="Nieznane urządzenie połączyło się z siecią lokalną!",
                            title="Sieć",
                            priority=4,
                        )
                        issues.add("unknown_device")
                    logging.warning(
                        "SENTRY | Unknown device has connected to local network!"
                    )
                    # adds unknown device to database
                    for address in unknown_devices:
                        postgresql_database.add_unknown_device(address)

    except Exception:
        logging.error(f"SENTRY | NETWORK | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
    finally:
        return issues


def check_diagnostic(diagnostic_data: typing.List[typing.Any]) -> typing.Set[str]:
    """Verifies that the battery, filter or other consumable parts of the device
    are not at the end of their life.
    (For testing purposes only) Returns set of strings representing detected issues.
    If there is no issues, empty set will be returned.
    """
    try:
        # establish connection to Redis
        with Redis() as redis:
            # empty set of issues
            issues = set()

            # iteration over diagnostic data
            for data in diagnostic_data:
                # iterate over health fields
                for field, value in data.health_data.items():
                    # if consumable part level exceeds predefined level
                    if (
                        redis.notify_devices_diagnostics
                        and value
                        and value <= redis.notify_devices_diagnostics_level
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
        logging.error(f"SENTRY | DIAGNOSTIC | UNKNOWN ERROR OCURRED\n{traceback.format_exc()}")
    finally:
        return issues
