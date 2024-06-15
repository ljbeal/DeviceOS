from DeviceOS.board.wifimixin import WiFiMixin
from DeviceOS.board.mqttmixin import MQTTMixin

from DeviceOS.sensors.sensordevice import SensorDevice
import network


class Board(WiFiMixin, MQTTMixin):
    """
    Baseclass for the board, enabling WiFi and MQTT connectivity

    Args:
        wlan_ssid: ssid for target WiFi
        wlan_pass: password for target WiFi
        hostname: desired hostname (optional)

        mqtt_host: mqtt server hostname
        mqtt_user: mqtt username
        mqtt_pass: mqtt password
        mqtt_port: mqtt port (optional)
    """

    __slots__ = [
        "_wlan_ssid",
        "_wlan_pass",
        "_mqtt_host",
        "_mqtt_user",
        "_mqtt_pass",
        "_mqtt_port",
        "devices"
    ]

    def __init__(
        self,
        wlan_ssid: str,
        wlan_pass: str,
        mqtt_host: str,
        mqtt_user: str,
        mqtt_pass: str,
        mqtt_port: int = 1883,
        name: str = "DeviceOS_Test",
    ):
        network.hostname(name)

        self._wlan_ssid = wlan_ssid
        self._wlan_pass = wlan_pass
        self._mqtt_host = mqtt_host
        self._mqtt_user = mqtt_user
        self._mqtt_pass = mqtt_pass
        self._mqtt_port = mqtt_port

        self.devices = []

        self.connect()       

    def connect(self):
        if not self.has_wifi:
            self.connect_to_wifi()
        if not self.has_mqtt:
            self.connect_to_mqtt()

    def add_sensor(self, sensor: SensorDevice):
        self.devices.append(sensor)

    @property
    def sensors(self) -> list:
        return [item for item in self.devices if isinstance(item, SensorDevice)]
    
    def discover(self):
        for sensor in self.sensors:
            print(f"discovering for sensor {sensor.name}")
            print(sensor.discover())
