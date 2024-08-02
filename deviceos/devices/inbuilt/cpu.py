from deviceos import Output, Device

import machine  # pylint: disable=import-error


class CPU(Device):
    """
    Basic Sensor for reporting CPU temp

    Functions as an example for simple devices
    """

    def __init__(self):
        super().__init__(name="CPU")

        self.interfaces = [
            Output(
                name="CPU_Temp",
                unit="C",
                icon="mdi:thermometer",
                format_mod="round(2)",
                diagnostic=True,
            )
        ]

    def read(self):
        adc = machine.ADC(4)
        voltage = adc.read_u16() * (3.3 / 65536)
        temp_c = 27 - (voltage - 0.706) / 0.001721

        return {"CPU_Temp": temp_c}
