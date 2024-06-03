try:
    from umqtt.simple import MQTTClient, MQTTException
except ImportError:
    import mip
    mip.install("umqtt.simple")
    from umqtt.simple import MQTTClient, MQTTException


class MQTTMixin:
    """
    Adds MQTT related functionality
    
    expects a host and password at _mqtt_host and _mqtt_pass
    """

    __slots__ = ["_mqtt"]

    @property
    def mqtt(self):
        return self._mqtt

    def connect_to_mqtt(self):
        self._mqtt = MQTTClient(client_id="", 
                                server=self._mqtt_host, 
                                port=self._mqtt_port, 
                                user=self._mqtt_user, 
                                password=self._mqtt_pass, 
                                keepalive=61, 
                                ssl=False
                                )
        
        try:
            print("Connecting to MQTT Broker... ", end = "")
            self.mqtt.connect()
        except Exception as ex:
            print(f"Error:\n{str(ex)}")
        else:
            print("Done.")
