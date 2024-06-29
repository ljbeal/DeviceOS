from deviceos import Device
from deviceos.devices.io import Input


class Switch(Device):
    """
    One way switch, available only on the web side
    """

    def __init__(self, *args, **kwargs):
        super().__init__(name="Switch")

        self.interfaces = [
            Input(name="test", icon="mdi:toggle-switch-off", callback=self.callback)
        ]

    def callback(self, msg: str):
        print("Switch was flipped on the UI")
        switch = self.get_interface("test")
        if msg == "ON":
            switch.value = True
        else:
            switch.value = False

    def read(self):
        switch = self.get_interface("test")
        try:
            value = switch.value
        except AttributeError:
            value = False
        return {"test": "ON" if value else "OFF"}
