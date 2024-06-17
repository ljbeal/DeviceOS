"""
main.py always runs on pico startup
"""

import secrets as s

from DeviceOS.board import Board
from DeviceOS.sensors.inbuilt.cpu import CPU  # type:  ignore
from DeviceOS.sensors.inbuilt.network import Network  # type:  ignore


board = Board(wlan_ssid=s.wifi["ssid"],
              wlan_pass=s.wifi["pass"],
              mqtt_host=s.mqtt["host"],
              mqtt_user=s.mqtt["user"],
              mqtt_pass=s.mqtt["pass"],
              name="DeviceOS_Test",
              area="Desk")

board.add_sensor(CPU())
board.add_sensor(Network(ip=board.ip))

from sensors.bme280 import BME280_MQTT
board.add_sensor(BME280_MQTT(sda=16, scl=17, interval=5))

board.discover()
board.run()
