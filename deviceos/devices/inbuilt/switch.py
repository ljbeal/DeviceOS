"""
Testing module for a simple switch
"""
from deviceos import Device
from deviceos.devices.io import Input

from machine import Pin


class Switch(Device):
    """
    One way switch, available only on the web side
    """

    def __init__(self, name="Switch"):
        super().__init__(name=name)

        self.interfaces = [
            Input(name="Board_LED", icon="mdi:toggle-switch", callback=self.callback)
        ]

        self.led = Pin("LED", Pin.OUT)
        self.value = self.led.value()

    def callback(self, msg: str):
        """
        Callback receives msg from home assistant

        ON/OFF as set by payload_on/off properties
        """
        if msg == "ON":
            print("switch value set to True")
            self.value = True
            self.led.value(1)
        else:
            print("switch value set to False")
            self.value = False
            self.led.value(0)

    def read(self):
        return {"Board_LED": "ON" if self.value else "OFF"}
