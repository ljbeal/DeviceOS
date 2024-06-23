"""
Contains the Board class, the toplevel class for all sensors

Also handles wifi and mqtt functionality
"""

import json
import time

import network  # pylint: disable=import-error
import ubinascii  # pylint: disable=import-error
from machine import unique_id  # pylint: disable=import-error

import deviceos
from deviceos.board.mqttmixin import MQTTMixin
from deviceos.board.wifimixin import WiFiMixin
from deviceos.sensors.device import Device


class Board(WiFiMixin, MQTTMixin):
    # pylint: disable = too-many-arguments, too-many-instance-attributes
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
        "devices",
        "name",
        "area",
        "discovery_prefix",
        "interval",
        "last_update_time",
        "_discovered",
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
        self._discovered = False

        self.interval = interval
        self.last_update_time = 0

        self._wlan_ssid = wlan_ssid
        self._wlan_pass = wlan_pass
        self._mqtt_host = mqtt_host
        self._mqtt_user = mqtt_user
        self._mqtt_pass = mqtt_pass
        self._mqtt_port = mqtt_port

        self.devices = []

        self.setup()

    def setup(self):
        """Performs any setup steps"""
        # ensure wifi and mqtt connections
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
        while not self.connect_to_wifi():
            pass
        while not self.connect_to_mqtt():
            pass

    def add_device(self, sensor: Device) -> None:
        """Add a preconfigured sensor to the board"""
        for interface in sensor.interfaces:
            interface.parent = self
        self.devices.append(sensor)

    @property
    def sensors(self) -> list:
        """Returns a list of sensors"""
        return [item for item in self.devices if isinstance(item, Device)]

    @property
    def device_info(self) -> dict:
        """Device info stub for discovery"""
        payload = {
            "sw_version": deviceos.__version__,
            "identifiers": self.identifiers,
            "name": self.name,
            "manufacturer": "ljbeal"
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
                interface.discover()

        self._discovered = True

    def read_sensors(self) -> bool:
        """
        Read all of the sensor data into their respective names
        
        Returns True if there is something to publish, else False
        """
        update = False
        for sensor in self.sensors:
            if sensor.internal_device_read():
                update = True
        return update

    def run(self) -> None:
        """Run, forever"""
        if hasattr(self, "_reset_flag") and self._reset_flag:
            print("we are in a reset state, attempting a reconnect")
            self.setup()

        if not self._discovered:
            self.discover()

        topic = f"{self.base_topic("sensor")}/state"

        while True:
            self.read_sensors()

            now = int(time.time())

            if self.last_update_time + self.interval > now:
                continue

            self.last_update_time = now

            payload = {}
            for sensor in self.sensors:
                payload.update(sensor.data)

            print(f"{now}: {topic}")
            print(payload)
            self.publish(topic=topic, message=json.dumps(payload))
