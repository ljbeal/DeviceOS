"""
SensorDevice is the base class that represents a single sensor breakout
"""


class SensorDevice:
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

    __slots__ = ["_name", "interfaces", "component"]

    def __init__(self, name: str, component: str = "sensor"):
        self._name = name

        self.component = component

        self.interfaces = []

    def __repr__(self) -> str:
        return f"Sensor({self.name})"

    @property
    def name(self) -> str:
        """Returns the stored name"""
        return self._name

    def read(self):
        """Stub read() method, to be replaced by the user"""
        return NotImplemented
