"""
Prototypes of future system classes.
"""


import itertools
from typing import *


class Device:
    """"""

    def __init__(self,
        name: str,
        brand: str,
        mac_address: str
    ) -> None:
        """"""
        self.name = name
        self.brand = brand
        self.mac_address = mac_address

    def __repr__(self) -> str:
        """"""
        return f"{self.name}"


class Room:
    """"""

    def __init__(self,
        name: str,
        length: float,
        width: float,
        height: float,
        devices: List[Device] = []
    ) -> None:
        """"""
        self.name = name
        self.lenght = length
        self.width = width
        self.height = height
        self.devices = devices

    def __repr__(self) -> str:
        """"""
        return f"{self.name}"


class House:
    """"""

    def __init__(self,
        length: float,
        width: float,
        height: float,
        rooms: List[Room] = []
    ) -> None:
        """"""
        self.lenght = length
        self.width = width,
        self.height = height
        self.rooms = rooms
        self.rooms_number = len(rooms)

    @property
    def area(self) -> float:
        """"""
        return float(self.lenght * self.width)

    @property
    def volume(self) -> float:
        """"""
        return float(self.lenght * self.width * self.height)

    @property
    def devices(self) -> List[Device]:
        """"""
        return list(itertools.chain.from_iterable([room.devices for room in self.rooms]))


if __name__ == "__main__":

    purifier = Device(
        name="air purifier",
        brand="Xiaomi",
        mac_address="12:ab:34:cd:56:ef"
    )

    bedroom = Room(
        name="bedroom",
        length=4.0,
        width=2.5,
        height=3.0,
        devices=[purifier]
    )

    house = House(
        length=8.0,
        width=7.5,
        height=3.0,
        rooms=[bedroom]
    )
    print(house.rooms)
    print(house.devices)
