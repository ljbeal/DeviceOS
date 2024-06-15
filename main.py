import secrets as s

from DeviceOS.board import Board
from DeviceOS.sensors.inbuilt.cpu import CPU  # type:  ignore


board = Board(wlan_ssid=s.wifi["ssid"], 
              wlan_pass=s.wifi["pass"],
              mqtt_host=s.mqtt["host"],
              mqtt_user=s.mqtt["user"],
              mqtt_pass=s.mqtt["pass"])

print(board.ip)
print(board.hostname)

board.add_sensor(CPU())

print(board.sensors)
print(board.sensors[0].outputs)
