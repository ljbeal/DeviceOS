"""
Mixin class providing MQTT functionality
"""
import time

try:
    from umqtt.simple import MQTTClient
except ImportError:
    import mip

    try:
        import secrets as s  # type:  ignore

        import network  # pylint: disable=import-error

        wlan = network.WLAN(network.STA_IF)
        wlan.connect(s.wifi["ssid"], s.wifi["pass"])
        while not wlan.isconnected() and wlan.status() >= 0:
            print("waiting for wifi for mip install")
    except Exception as ex:
        print("Failed wifi init when attempting to install umqtt.simple")
        raise ex

    mip.install("umqtt.simple")
    from umqtt.simple import MQTTClient


class MQTTMixin:
    """
    Adds MQTT related functionality

    expects a host and password at _mqtt_host and _mqtt_pass
    """

    __slots__ = [
        "_mqtt",
        "_mqtt_host",
        "_mqtt_user",
        "_mqtt_pass",
        "_mqtt_port",
        "_reset_flag",
        ]

    @property
    def mqtt(self) -> MQTTClient:
        """Returns the internal MQTTClient object"""
        if not hasattr(self, "_mqtt"):
            return None
        return self._mqtt

    def connect_to_mqtt(self) -> bool:
        """Attempts to connect to the broker"""
        self._mqtt = MQTTClient(
            client_id="",
            server=self._mqtt_host,
            port=self._mqtt_port,
            user=self._mqtt_user,
            password=self._mqtt_pass,
            keepalive=61,
            ssl=False,
        )
        connected = False
        n_ellipses = 0
        max_ellipses = 3
        while not connected:
            try:
                n_ellipses += 1
                if n_ellipses > max_ellipses:
                    n_ellipses = 1

                print(
                    "Connecting to MQTT Broker" + "." * n_ellipses,
                    end=" " * max_ellipses + "\r",
                )
                self.mqtt.connect()
                connected = True
            except OSError:  # pylint: disable=broad-exception-caught
                time.sleep(0.5)

        print("Connecting to MQTT Broker... Done.")
        return True


    def publish(self, topic: str, message: str, retain: bool = False) -> None:
        """Passthrough for umqtt.simple MQTTClient.publish"""
        try:
            self.mqtt.publish(topic=topic, msg=message, retain=retain)
        except OSError as exc:
            # if the connection fails, we probably need to go into a reset state
            print(f"OSError: {str(exc)}, entering reset state")
            self._reset_flag = True
