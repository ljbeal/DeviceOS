import DeviceOS
from DeviceOS.board.wifimixin import WiFiMixin
from DeviceOS.board.mqttmixin import MQTTMixin
from DeviceOS.sensors.sensordevice import SensorDevice

import network
import ubinascii

from machine import unique_id


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
        "devices",
        "name",
        "area"
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
        area: str | None = None
    ):
        network.hostname(name)
        self.name = name
        self.area = area

        self._wlan_ssid = wlan_ssid
        self._wlan_pass = wlan_pass
        self._mqtt_host = mqtt_host
        self._mqtt_user = mqtt_user
        self._mqtt_pass = mqtt_pass
        self._mqtt_port = mqtt_port

        self.devices = []

        self.connect()     

    @property
    def uid(self) -> str:
        """Returns the board UID"""
        return ubinascii.hexlify(unique_id()).decode()  
    
    @property
    def identifiers(self):
        return [self.uid]

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
    
    @property
    def device_info(self):
        payload = {
            "sw_version": DeviceOS.__version__,
            "identifiers": self.identifiers,
            "name": self.name,
            "manufacturer": "ljbeal"
            }
        
        if self.area is not None:
            payload["suggested_area"] = self.area

        return payload
    
    def discover(self) -> None:
        for sensor in self.sensors:
            print(f"collecting discovery for sensor {sensor.name}")
            sensor_payloads = sensor.discover(self.device_info)

            for payload in sensor_payloads:
                print(payload)
            