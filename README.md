# DeviceOS

DeviceOS is a framework for creating Homeassistant MQTT enabled devices.

Devices support MQTT Discovery, so no faffing with configuration.yaml files.

> ⚠️ This package is still very much WIP, so the API may change without notice! Contributions are alwawys welcome. ⚠️

## Installation

Installation can be done via micropython's `mip` package. Connect your board to wifi, and do the following:

```
import mip
mip.install("github:ljbeal/DeviceOS", version="main")
```

Note that due to a quirk with mip, the `version="main"` is _required_.

### Installation via Script

For ease of install, a simple script to connect to wifi, import mip, then finally install the package can be run.

However first, we must have the necessary requirements.

### Requirements

Before running this script, the board must know the details of the wifi connection.

To do this, create a `secrets.py` file with the following format:

```py
wifi = {
    "ssid": "your_wifi_ssid",
    "pass": "your_wifi_password"
}

mqtt = {
    "host": "your_mqtt_hostname",
    "user": "your_mqtt_username",
    "pass": "your_mqtt_password"
}
```

> :triangular_flag_on_post: Note:
> 
> The `mqtt` section is optional at this stage, but this file is also used by DeviceOS in the same format.
>
> If you installed MQTT within Home Assistant, your details can be found at:
>
> ```settings -> add-ons -> mosquitto broker -> configuration```

### Script

Now you can use the following script to install the package and its dependencies:

```py
import time
import network  # pylint: disable=import-error
import secrets as s


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(s.wifi["ssid"], s.wifi["pass"])

print("waiting for wlan")
while not not wlan.isconnected() and wlan.status() < 0:
    time.sleep(0.1)

print(wlan.ifconfig())

import mip  # pylint: disable=import-error

mip.install("github:ljbeal/deviceos", version="main")
```

## Configuration

This section covers the basic concepts and configuration information.

For a quickstart, see the `main.py` script. This will create a `DeviceOS` entity within HA that reports its CPU temperature, IP and allows you to toggle the board LED.

### Components

There are 3 "layers" to a device.

- Board
- Device
- Interface

#### Board

The `Board` module is what handles toplevel functionality. It deals with WiFi, MQTT, callbacks, and other "global" functions.

You should create an instance of this within your `main.py`, and add sensors from there.

#### Device

The `Device` module is conceptually a single addition to your board. A sensor breakout board, for example.

Conceptually it is anything that is attached to any GPIO pins. Be it a single pin for a button, or multiple for an i2c device.

#### Interface

`Interface` handles a single data input/output instance. They are attached to a `Device` instance and let it know what sort of data to expect.

A good example of why it is done this way (and not attached directly to `Device`) is the BME280 sensor. This i2c sensor provides data for temperature, humidity and pressure. So a hypothetical `BME280_MQTT(Device)` specification has 3 `Output` interfaces.

`DeviceOS` uses these objects for MQTT discovery and data tracking.

Note: Only `Output` exists at present (still working out the best API for `Input`)

### Polling rate

`Board` has an `interval` property which controls how frequently it reports back to the MQTT broker.

Additionally, `Device` _also_ has an `interval` property which controls how frequently it _updates_.

By default, these are both set to 15s, so they are in sync. But they can be changed for specific use cases.

An example of this is the inbuilt `network` device, which reports the board's IP address back to Homeassistant. It has an internal `interval` of 86400s (1 day), so only updates on first boot, and then every 24h after that (a typical DHCP lease length).

One potential use case of this is to _lower_ the interval, and to keep a running total. Lets say we have a noisy sensor, we can set the `interval` to 0.1s and keep a running total. When `Board` comes around and asks for data (every 15s by default), it can report a statistical value based on this storage.


## Devices

### Base Class

Sensors can be created by subclassing the `Device` class. Define the usual `__init__` method, and be sure to call the `super().__init__()` method. You should specify the sensor name here by passing `name="name"`.

```
from deviceos import Device

class MyTempSensor(Device):
    def __init__(self):
        super().__init__(name="sensor")
```

### Interfaces

You can now specify the expected outputs of your sensor, using the `Ouput` class. Add these to a list called `interfaces`.

It is important that this matches the output of your later `read()` function, but we'll come to this later.

```
from deviceos import Device, Output  # also import Output

class MyTempSensor(Device):
    def __init__(self):
        super().__init__(name="sensor")

        # in a reality, this would be an actual sensor object
        self.sensor = ...

        self.interfaces = [
            Output(
                name="temperature",
                unit="C",
                icon="mdi:thermometer",
                format_mod="round(2)"
            )
        ]
```

### Read function

The final thing to do is to specify the `read()` function that will be called by `Board`. This should return a `dict` that matches the `interfaces` list.

```
from deviceos import Device, Output  # also import Output

class MyTempSensor(Device):
    def __init__(self):
        super().__init__(name="sensor")

        self.interfaces = [
            Output(
                name="temperature",
                unit="C",
                icon="mdi:thermometer",
                format_mod="round(2)"
            )
        ]

    def read(self):
        # read the data from your sensor
        data = self.sensor.temperature

        return {"temperature: data}
```

### Testing your devices

If you are creating your device in a separate file, you can interact with them without worrying about connecting to wifi or mqtt.

It is good practice to create your devices in individual modules and add a testing block to the bottom of each.

```
...

if __name__ == "__main__":
    import time
    test = MyTempSensor():
    
    while True:
        print(test.read())

        time.sleep(1)
```

This will attempt to print the `read()` output every second, until killed. By emulating the run in this way, you can check that the output of the sensor at least looks sensible.

## Adding Devices

Now you have a sensor, you should add it to your `Board`

This can be done by calling the `Board.add_device(device)` method after creating your device.
