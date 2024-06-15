"""
Output is the base class that represents a single sensor output.

For example a light sensor would have one output (the light level),
whereas a combination sensor may have multiple. A particulate sensor may have 
three, for PM10, 2.5 and 1.0.
"""


illegal_chars = [" "]


class Output:
    # pylint: disable = too-many-arguments
    """
    Baseclass to mark the instance of one sensor reading

    e.g. A BME climate unit would contain an instance for temp, humidity and pressure

    Args:
        name: subsensor name
        icon: subsensor icon
        unit: subsensor unit
        diagnostic: flag this sensor as "diagnostic"
        format_mod: format modifer (eg round(2))
    """

    __slots__ = ["_name", "_icon", "_unit", "_format", "_is_diagnostic"]
    def __init__(
        self,
        name: str,
        icon: str,
        unit: str | None = None,
        diagnostic: bool = False,
        format_mod: str | None = None
    ):
        self._name = name
        self._icon = icon
        self._unit = unit

        for char in illegal_chars:
            if char in name:
                raise ValueError(f"Name cannot contain illegal characters: {illegal_chars}")

        self._format = format_mod  # format modifer such as round(2)

        self._is_diagnostic = diagnostic

    def __repr__(self) -> str:
        return f"Output({self.name})"

    @property
    def name(self) -> str:
        """Returns the specified name"""
        return self._name

    @property
    def icon(self) -> str:
        """Returns the specified icon"""
        return self._icon

    @property
    def format(self) -> None | str:
        """Returns the format modifier, for discovery"""
        return self._format

    @property
    def unit(self) -> str | None:
        """
        Returns the specified unit

        ..note::
            Sensors with unit=None will have no graph.
            Set unit to "" for a "unitless" graph
        """
        return self._unit

    @property
    def diagnostic(self) -> bool:
        """Returns True if this output is flagged as Diagnostic"""
        return self._is_diagnostic

    @property
    def discovery_payload(self) -> dict:
        """Returns the discovery payload"""
        payload = {
            "unit_of_measurement": self.unit,
            "name": self.name,
            "icon": self.icon,
            }

        value_template = ["{{ value_json."]
        value_template.append(self.name)

        if self.format is not None:
            value_template.append(f" | {self._format}")
        value_template.append(" }}")
        payload["value_template"] = "".join(value_template)

        if self.diagnostic:
            payload["entity_category"] = "diagnostic"

        return payload
