"""
Contains the Board class, the toplevel class for all sensors

Also handles wifi and mqtt functionality
"""

import json
import time

import network  # pylint: disable=import-error
import ubinascii  # pylint: disable=import-error
from machine import unique_id  # pylint: disable=import-error

import DeviceOS
from DeviceOS.board.mqttmixin import MQTTMixin
from DeviceOS.board.wifimixin import WiFiMixin
from DeviceOS.sensors.sensordevice import SensorDevice


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
        "area",
        "discovery_prefix",
        "interval",
        "_discovered"
    ]

    def __init__(
        self,
        wlan_ssid: str,
        wlan_pass: str,
        mqtt_host: str,
        mqtt_user: str,
        mqtt_pass: str,
        mqtt_port: int = 1883,
        discovery_prefix: str = "homeassistant",
        interval: int = 15,
        name: str = "DeviceOS_Test",
        area: str | None = None
    ):
        network.hostname(name)
        self.name = name
        self.area = area

        self.discovery_prefix = discovery_prefix

        self.interval = interval

        self._wlan_ssid = wlan_ssid
        self._wlan_pass = wlan_pass
        self._mqtt_host = mqtt_host
        self._mqtt_user = mqtt_user
        self._mqtt_pass = mqtt_pass
        self._mqtt_port = mqtt_port

        self.devices = []

        self.connect()

        self._discovered = False

    @property
    def uid(self) -> str:
        """Returns the board UID"""
        return ubinascii.hexlify(unique_id()).decode()

    @property
    def identifiers(self) -> list:
        """Return identifiers for discovery payload"""
        return [self.uid]

    def connect(self) -> None:
        """Attempt to connect to wifi and broker"""
        if not self.has_wifi:
            self.connect_to_wifi()
        if not self.has_mqtt:
            self.connect_to_mqtt()

    def add_sensor(self, sensor: SensorDevice) -> None:
        """Add a preconfigured sensor to the board"""
        self.devices.append(sensor)

    @property
    def sensors(self) -> list:
        """Returns a list of sensors"""
        return [item for item in self.devices if isinstance(item, SensorDevice)]

    @property
    def device_info(self) -> dict:
        """Device info stub for discovery"""
        payload = {
            "sw_version": DeviceOS.__version__,
            "identifiers": self.identifiers,
            "name": self.name,
            "manufacturer": "ljbeal",
            "support_url": "https://github.com/ljbeal/DeviceOS"
            }

        if self.area is not None:
            payload["suggested_area"] = self.area

        return payload

    def base_topic(self, component: str = "sensor") -> str:
        """Generate discovery topic for `component`
        See docs here: https://www.home-assistant.io/integrations/mqtt/#discovery-messages

        Args:
            component (str, optional): Component type. Defaults to "sensor".
        """
        return f"{self.discovery_prefix}/{component}/{self.uid}"

    def discover(self) -> None:
        """Initiate discovery"""
        for sensor in self.sensors:
            for interface in sensor.interfaces:
                name = interface.name
                payload = interface.discovery_payload

                payload["device"] = self.device_info

                base_topic = self.base_topic(sensor.component)

                payload["state_topic"] = f"{base_topic}/state"

                discovery_topic = f"{base_topic}/{name}/config"

                print(name)
                print(discovery_topic)
                print(payload)

                self.publish(
                    topic=discovery_topic,
                    message=json.dumps(payload),
                    retain=False
                    )  # TODO: update retain

        self._discovered = True

    def read_sensors(self) -> dict:
        """Read all of the sensor data into their respective names"""
        cache = {}
        for sensor in self.sensors:
            tmp = sensor.read()

            for key, val in tmp.items():
                if key in cache:
                    raise ValueError(f"key {key} already exists, do you have a sensor name clash?")
                cache[key] = val

        return cache

    def run(self) -> None:
        """Run, forever"""
        while True:

            self.one_shot()

            time.sleep(self.interval)

    def one_shot(self) -> None:
        """Run, once"""
        payload = self.read_sensors()

        topic = f"{self.base_topic("sensor")}/state"

        print(topic)
        print(payload)
        self.publish(topic=topic, message=json.dumps(payload))
