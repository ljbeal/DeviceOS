try:
    from umqtt.simple import MQTTClient, MQTTException
except ImportError:
    import mip

    try:
        import secrets as s  # type:  ignore
        import network

        wlan = network.WLAN(network.STA_IF)
        wlan.connect(s.wifi["ssid"], s.wifi["pass"])
        while not wlan.isconnected() and wlan.status() >= 0:
            print("waiting for wifi for mip install")
    except Exception as ex:
        print(f"Failed wifi init when attempting to install umqtt.simple")
        raise ex

    mip.install("umqtt.simple")
    from umqtt.simple import MQTTClient, MQTTException


class MQTTMixin:
    """
    Adds MQTT related functionality

    expects a host and password at _mqtt_host and _mqtt_pass
    """

    __slots__ = ["_mqtt"]

    _mqtt = None

    @property
    def mqtt(self) -> MQTTClient:
        return self._mqtt

    def connect_to_mqtt(self):
        self._mqtt = MQTTClient(
            client_id="",
            server=self._mqtt_host,
            port=self._mqtt_port,
            user=self._mqtt_user,
            password=self._mqtt_pass,
            keepalive=61,
            ssl=False,
        )

        try:
            print("Connecting to MQTT Broker... ", end="")
            self.mqtt.connect()
        except Exception as ex:
            print(f"Error:\n{str(ex)}")
        else:
            print("Done.")

    @property
    def has_mqtt(self) -> bool:
        """
        Returns True if the mqtt server accepts connections

        WARNING: This will attempt to connect
        """
        try:
            self.mqtt.connect()
            return True
        except Exception:
            return False
