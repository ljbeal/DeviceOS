from DeviceOS.Sensors.Subsensors.output import Output
from DeviceOS.Sensors.sensordevice import SensorDevice

import machine  # type: ignore


class CPU(SensorDevice):
    """
    Basic Sensor for reporting CPU temp

    Functions as an example for simple sensors

    TODO: Decide if enforcing an __init__ is worth it (with super())    
    """

    name="CPU"
    temp = Output(name="temp", unit="C", icon="mdi:thermometer", diagnostic=True)

    def read(self):
        adc = machine.ADC(4)
        voltage = adc.read_u16() * (3.3 / 65536)
        temp_c = 27 - (voltage - 0.706) / 0.001721

        return {"temp": temp_c}
