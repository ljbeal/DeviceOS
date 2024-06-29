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

        self.value = True

    def callback(self, msg: str):
        if msg == "ON":
            print("switch value set to True")
            self.value = True
        else:
            print("switch value set to False")
            self.value = False

    def read(self):
        return {"test": "ON" if self.value else "OFF"}
