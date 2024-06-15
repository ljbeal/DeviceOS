from DeviceOS.sensors.subsensors.output import Output


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

    __slots__ = ["_name", "interfaces"]

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f"Sensor({self.name})"
    
    @property
    def name(self):
        return self._name
        
    def discover(self) -> list:
        return [output.discovery_payload for output in self.interfaces]
