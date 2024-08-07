"""
SensorDevice is the base class that represents a single sensor breakout
"""

import time

from deviceos.devices.io.output import Output


class Device:
    """
    Class to reference a single sensor device,
    this should be at the same level as the sensor's API module

    Then Subsensor object should be specified within the init of that class

    e.g:
    class BME680_Device(SensorDevice):
        def __init__(self, ...):
            self._sensor = BME680(...)

            self.humidity = Subsensor(...)
            ...
    """

    __slots__ = [
        "_name",
        "interfaces",
        "interval",
        "last_read_time",
        "_internal_data",
        "last_print_time",
    ]

    def __init__(self, name: str, interval: int = 15):
        self._name = name

        self.interfaces = []

        self._internal_data = {}

        self.last_read_time = 0
        self.interval = interval

        self.last_print_time = 0

        print(f"created sensor {self.name} with interval {self.interval}")

    def __repr__(self) -> str:
        return f"Sensor({self.name})"

    def get_interface(self, name: str) -> Output | None:
        """Attempt to get an interface by name"""
        for interface in self.interfaces:
            if interface.name == name:
                return interface
        return None

    @property
    def name(self) -> str:
        """Returns the stored name"""
        return self._name

    @property
    def internal_data(self):
        """Provides access to the internal data storage"""
        return self._internal_data

    @internal_data.setter
    def internal_data(self, data):
        self._internal_data = data

    def internal_device_read(self, force: bool = False) -> bool:
        """Internal read, stores the output of the user read() into the data property"""
        now = int(time.time())

        if not force and self.last_read_time + self.interval > now:
            return False

        if self.last_print_time + 1 <= now:
            print(f"updating {self.name}")
            self.last_print_time = now

        self._internal_data = self.read()

        for interface in self.interfaces:
            if getattr(interface, "calibration", None) is not None:
                self._internal_data[interface.name] += interface.calibration
        if not force:
            self.last_read_time = now
        return True

    def read(self):
        """Stub read() method, to be replaced by the user"""
        return NotImplemented
