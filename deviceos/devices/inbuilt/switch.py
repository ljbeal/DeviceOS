"""
Testing module for a simple switch
"""
from deviceos import Device
from deviceos.devices.io import Input


class Switch(Device):
    """
    One way switch, available only on the web side
    """

    def __init__(self, name="Switch"):
        super().__init__(name=name)

        self.interfaces = [
            Input(name="test", icon="mdi:toggle-switch-off", callback=self.callback)
        ]

        self.value = True

    def callback(self, msg: str):
        """
        Callback receives msg from home assistant

        ON/OFF as set by payload_on/off properties
        """
        if msg == "ON":
            print("switch value set to True")
            self.value = True
        else:
            print("switch value set to False")
            self.value = False

    def read(self):
        return {"test": "ON" if self.value else "OFF"}
