from DeviceOS.Sensors.Subsensors.output import Output


class ContinuousOutput(Output):
    """
    Class defining a sensor that runs "continuously"

    The read() method here simply collects the most recent data
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
