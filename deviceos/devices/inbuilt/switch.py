from deviceos import Device
from deviceos.devices.io import Input


class Switch(Device):
    """
    One way button, available only on the web side
    """

    def __init___(self, *args, **kwargs):
        super().__init__(name="Switch", *args, **kwargs)

        self.interfaces = [
            Input(name="test", icon="mdi:toggle-switch-off", callback=self.callback)
        ]

    def callback(self):
        print("Switch was flipped on the UI")

        switch = self.get_interface("test")

        icons = [
            "mdi:toggle-switch-on",
            "mdi:toggle-switch-off",
        ]
        switch.icon = icons[0 if switch.value else 1]

    def read(self):
        switch = self.get_interface("test")
        try:
            value = switch.value
        except AttributeError:
            value = False
        return {"test": "ON" if value else "OFF"}
