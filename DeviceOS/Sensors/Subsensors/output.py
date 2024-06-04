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
        self, name: str, icon: str, unit: str | None = None, diagnostic: bool = False
    ):
        self._name = name
        self._icon = icon
        self._unit = unit

        self._is_diagnostic = diagnostic

    @property
    def name(self) -> str:
        """Returns the specified name"""
        return self._name

    @property
    def icon(self) -> str:
        """Returns the specified icon"""
        return self._icon

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
