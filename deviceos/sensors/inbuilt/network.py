from deviceos.sensors.subsensors.output import Output
from deviceos.sensors.sensordevice import SensorDevice


class Network(SensorDevice):
    def __init__(self, ip):
        super().__init__(name="network")
        self.ip = ip
        self.interfaces = [Output(name="IP", icon="mdi:ip-network-outline", diagnostic=True)]

    def read(self):
        return {"IP": self.ip}
    