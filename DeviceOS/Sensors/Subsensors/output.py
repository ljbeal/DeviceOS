class Output:
    """
    Baseclass to mark the instance of one sensor reading

    e.g. A BME climate unit would contain an instance for temp, humidity and pressure

    Args:
        name: subsensor name
        icon: subsensor icon
        unit: subsensor unit
        diagnostic: flag this sensor as "diagnostic"
    """

    __slots__ = ["_name", "_icon", "_unit", "_is_diagnostic"]

    def __init__(
        self, 
        name: str, 
        icon: str, 
        unit: str | None = None, 
        diagnostic: bool = False,
        format: str | None = None
    ):
        self._name = name
        self._icon = icon
        self._unit = unit

        self._format = format  # format modifer such as float(2)

        self._is_diagnostic = diagnostic

    def __repr__(self):
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
    def diagnostic(self):
        return self._is_diagnostic
    
    @property
    def discovery_payload(self):
        payload = {
            "unit_of_measurement": self.unit,
            "name": self.name
            }
        
        value_template = ["{{ value_json."]
        value_template.append(self.name)

        if self.format is not None:
            value_template.append(f"| {self._format}")
        value_template.append(" }}")
        payload["value_template"] = "".join(value_template)

        if self.diagnostic:
            payload["entity_category"] = "diagnostic"

        return payload
