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

    def __init__(self, name: str):
        self._name = name
        
    @property
    def outputs(self):
        subsensors = []
        for item in self.__dict__.values():
            if isinstance(item, Output):
                subsensors.append(item)

        return subsensors
        
    def discover(self) -> list:
        return [output.discovery_payload for output in self.outputs]
            
