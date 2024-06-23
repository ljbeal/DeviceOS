# DeviceOS

DeviceOS is a framework for creating Homeassistant MQTT enabled devices.

Devices support MQTT Discovery, so no faffing with configuration.yaml files.

## Installation

Installation can be done via micropython's `mip` package. Connect your board to wifi, and do the following:

```
import mip
mip.install("github:ljbeal/DeviceOS", version="main")
```

Note that due to a quirk with mip, the `version="main"` is _required_.

## Configuration

This package is still very much WIP, so the API may change without notice.

With that said, here are the basic concepts:

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
