from DeviceOS.sensors.subsensors.output import Output
from DeviceOS.sensors.sensordevice import SensorDevice


class Network(SensorDevice):
    def __init__(self, ip):
        super().__init__(name="network")
        self.ip = ip
        self.interfaces = [Output(name="ip", icon="mdi:network-outline", diagnostic=True)]

    def read(self):
        return {"ip": self.ip}
    