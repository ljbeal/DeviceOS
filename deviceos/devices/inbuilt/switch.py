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

    def __init__(self, name="Switch", pin: int | None = None):
        super().__init__(name=name)

        self.interfaces = [
            Input(name=name, icon="mdi:toggle-switch", callback=self.callback)
        ]

        if pin is None:
            self.pin = Pin("LED", Pin.OUT)
        else:
            self.pin = Pin(pin, Pin.OUT, Pin.PULL_DOWN)
        self.value = self.pin.value()

    def callback(self, msg: str):
        """
        Callback receives msg from home assistant

        ON/OFF as set by payload_on/off properties
        """
        if msg == "ON":
            print("switch value set to True")
            self.value = True
            self.pin.value(1)
        else:
            print("switch value set to False")
            self.value = False
            self.pin.value(0)

    def read(self):
        return {self.name: "ON" if self.value else "OFF"}
