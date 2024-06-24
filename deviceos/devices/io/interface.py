"""
Interface is the base class for all IO objects
"""
import json


illegal_chars = [" "]


class Interface:
    # pylint: disable = too-many-arguments
    """
    Baseclass to mark the instance of one HA interface

    These correspond to each individual entity in HA

    Args:
        name: subsensor name
        icon: subsensor icon
        unit: subsensor unit
        diagnostic: flag this sensor as "diagnostic"
        format_mod: format modifer (eg round(2))
        force_update: adds force_update flag to discovery if True (Default True)
    """

    __slots__ = [
        "_name", 
        "_icon", 
        "_force_update", 
        "_is_diagnostic",
        "_component",
        "_parent",
        ]

    def __init__(
        self,
        name: str,
        icon: str,
        component: str,
        diagnostic: bool = False,
        force_update: bool = True,
    ):
        self._name = name
        self._icon = icon

        self._component = component

        self._parent = None

        self._force_update = force_update

        for char in illegal_chars:
            if char in name:
                raise ValueError(f"Name cannot contain illegal characters: {illegal_chars}")

        self._is_diagnostic = diagnostic

    def __repr__(self) -> str:
        return f"Interface({self.name})"

    @property
    def parent(self) -> "Board":
        """Allows access to the parent Board object"""
        if self._parent is None:
            raise ValueError(f"Parent has not been updated for {self.name}")
        return self._parent

    @parent.setter
    def parent(self, parent: "Board"):
        print(f"Setting parent for {self.name}")
        self._parent = parent

    @property
    def name(self) -> str:
        """Returns the specified name"""
        return self._name

    @property
    def icon(self) -> str:
        """Returns the specified icon"""
        return self._icon

    @icon.setter
    def icon(self, icon: str):
        self._icon = icon
        self.discover()

    @property
    def diagnostic(self) -> bool:
        """Returns True if this output is flagged as Diagnostic"""
        return self._is_diagnostic

    @property
    def base_discovery_payload(self) -> dict:
        """Returns the discovery payload"""
        payload = {
            "name": self.name,
            "icon": self.icon,
            }

        if self.diagnostic:
            payload["entity_category"] = "diagnostic"

        if self._force_update:
            payload["force_update"] = True

        return payload

    @property
    def discovery_payload(self):
        return NotImplemented

    def discover(self) -> None:
        """
        Perform discovery for this entity
        """
        payload = self.discovery_payload

        payload["device"] = self.parent.device_info

        base_topic = self.parent.base_topic(self._component)

        payload["state_topic"] = f"{base_topic}/state"
        payload["unique_id"] = f"{self.parent.uid}_{self.name}"

        discovery_topic = f"{base_topic}/{self.name}/config"

        print(self.name)
        print(discovery_topic)
        print(payload)

        self.parent.publish(
            topic=discovery_topic,
            message=json.dumps(payload),
            retain=False
            )
