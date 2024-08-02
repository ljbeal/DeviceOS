"""
Output is the base class that represents a single sensor output.

For example a light sensor would have one output (the light level),
whereas a combination sensor may have multiple. A particulate sensor may have 
three, for PM10, 2.5 and 1.0.
"""

from deviceos.devices.io.interface import Interface


illegal_chars = [" "]


class Output(Interface):
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
        force_update: adds force_update flag to discovery if True (Default True)
    """

    __slots__ = [
        "_unit",
        "_format",
        "calibration",
    ]

    def __init__(
        self,
        name: str,
        icon: str,
        unit: str | None = None,
        component: str = "sensor",
        diagnostic: bool = False,
        format_mod: str | None = None,
        force_update: bool = True,
        calibration: int | float | None = None,
    ):
        super().__init__(
            name=name,
            icon=icon,
            component=component,
            diagnostic=diagnostic,
            force_update=force_update,
        )

        self._unit = unit
        self.calibration = calibration
        self._format = format_mod  # format modifer such as round(2)

    def __repr__(self) -> str:
        return f"Output({self.name})"

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
    def discovery_payload(self) -> dict:
        """Returns the discovery payload"""
        payload = self.base_discovery_payload

        payload["unit_of_measurement"] = self.unit

        value_template = ["{{ value_json."]
        value_template.append(self.name)

        if self.format is not None:
            value_template.append(f" | {self._format}")
        value_template.append(" }}")
        payload["value_template"] = "".join(value_template)

        return payload
