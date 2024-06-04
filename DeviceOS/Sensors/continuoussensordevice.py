from DeviceOS.Sensors.sensordevice import SensorDevice


class ContinuousSensorDevice(SensorDevice):
    """
    Class to reference a single sensor device

    This device runs "continuously", read() returns the 
    up to date values (can be latest, rolling avg, etc.)
    """
    
    def read(self):
        """
        Overrides interval read
        """
