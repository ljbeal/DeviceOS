"""
main.py always runs on pico startup
"""

import secrets as s

from deviceos.board import Board
from deviceos.sensors.inbuilt.cpu import CPU
from deviceos.sensors.inbuilt.network import Network


board = Board(wlan_ssid=s.wifi["ssid"],
              wlan_pass=s.wifi["pass"],
              mqtt_host=s.mqtt["host"],
              mqtt_user=s.mqtt["user"],
              mqtt_pass=s.mqtt["pass"],
              name="DeviceOS_Test",
              area="Desk")

board.add_sensor(CPU())
board.add_sensor(Network(ip=board.ip))

from examples.bme280 import BME280_MQTT
board.add_sensor(BME280_MQTT(sda=16, scl=17))

board.discover()
board.run()
