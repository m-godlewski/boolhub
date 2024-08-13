"""
This script contains dataclasses representation of custom data structures in system.
"""

from dataclasses import dataclass


# region DEVICES


@dataclass
class DeviceData:
    """Dataclass representation of entities stored in
    devices_device PostgreSQL database."""

    # fields
    name: str
    location: str
    category: str
    brand: str
    mac_address: str
    ip_address: str
    token: str


@dataclass
class UnknownDeviceData:
    """Dataclass representation of entities stored in
    unknown_devices PostgreSQL database."""

    # fields
    mac_address: str
    last_time: str


# endregion


# region AIR DATASETS


@dataclass
class Data:
    """Base class of each datasets dataclasses in this module."""

    # fields
    device: DeviceData


@dataclass
class AirData(Data):
    """Dataclass of air devices datasets."""

    # fields
    temperature: float = None
    humidity: int = None
    aqi: int = None

    def __post_init__(self) -> None:
        """Post initialization rounding numerical values."""
        self.temperature = round(self.temperature, ndigits=1) if self.temperature else None


@dataclass
class MiAirPurifier3HData(AirData):
    """Dataclass of Xiaomi Air Purifier 3H device."""

    # fields
    filter_life_remaining: int = None
    filter_hours_used: int = None
    use_time: int = None

    # fields groups
    AIR_DATA_FIELDS = {"aqi", "humidity", "temperature"}
    HEALTH_DATA_FIELDS = {
        "filter_life_remaining",
    }

    @property
    def air_data(self) -> dict:
        return dict(
            [(field, self.__getattribute__(field)) for field in self.AIR_DATA_FIELDS]
        )

    @property
    def health_data(self) -> dict:
        return dict(
            [(field, self.__getattribute__(field)) for field in self.HEALTH_DATA_FIELDS]
        )


@dataclass
class MiMonitor2Data(AirData):
    """Dataclass of Xiaomi Monitor 2 device."""

    # fields
    battery: int = None

    # fields groups
    AIR_DATA_FIELDS = {"temperature", "humidity"}
    HEALTH_DATA_FIELDS = {"battery"}

    @property
    def air_data(self) -> dict:
        return dict(
            [(field, self.__getattribute__(field)) for field in self.AIR_DATA_FIELDS]
        )

    @property
    def health_data(self) -> dict:
        return dict(
            [(field, self.__getattribute__(field)) for field in self.HEALTH_DATA_FIELDS]
        )


@dataclass
class OutsideVirtualThermometerData(AirData):
    """Dataclass of virtual outside thermometer."""

    # fields
    battery: int = 100

    # fields groups
    AIR_DATA_FIELDS = {"temperature", "humidity", "aqi"}
    HEALTH_DATA_FIELDS = {"battery"}

    @property
    def air_data(self) -> dict:
        return dict(
            [(field, self.__getattribute__(field)) for field in self.AIR_DATA_FIELDS]
        )

    @property
    def health_data(self) -> dict:
        return dict(
            [(field, self.__getattribute__(field)) for field in self.HEALTH_DATA_FIELDS]
        )


@dataclass
class ForecastData:
    """Dataclass of forecast data from virtual outside thermometer."""

    # fields
    date: str
    temperature: float
    humidity: int

    def __post_init__(self) -> None:
        """Post initialization rounding numerical values."""
        self.temperature = round(self.temperature, ndigits=1) if self.temperature else None

# endregion
