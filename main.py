from DeviceOS.Board import Board

import secrets as s


board = Board(wlan_ssid=s.wifi["ssid"], 
              wlan_pass=s.wifi["pass"],
              mqtt_host=s.mqtt["host"],
              mqtt_user=s.mqtt["user"],
              mqtt_pass=s.mqtt["pass"])

print(board.ip)
print(board.hostname)
