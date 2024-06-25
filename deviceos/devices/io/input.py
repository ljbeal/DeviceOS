from deviceos.devices.io.interface import Interface


class Input(Interface):

    __slots__ = ["callback", "value"]

    def __init__(
        self,
        name: str,
        icon: str,
        component: str = "switch",
        diagnostic: bool = False,
        force_update: bool = True,
        callback: "Callable" | None = None,
    ):
        super().__init__(
            name=name,
            icon=icon,
            component=component,
            diagnostic=diagnostic,
            force_update=force_update,
        )

        self.callback = callback
        self.value = True

    @property
    def command_topic(self):
        base_topic = self.parent.base_topic(self._component)
        return f"{base_topic}/set"

    @property
    def discovery_payload(self) -> dict:
        """Returns the discovery payload"""
        payload = self.base_discovery_payload
        payload["value_template"] = f"{{{{ value_json.{self.name }}}}}"
        payload["command_topic"] = self.command_topic

        return payload
