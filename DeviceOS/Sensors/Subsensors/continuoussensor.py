from DeviceOS.Sensors.Subsensors.basesubsensor import BaseSubSensor


class ContinuousSensor(BaseSubSensor):
    """
    Class defining a sensor that runs "continuously"

    The read() method here simply collects the most recent data
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
