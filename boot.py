# -*- coding: utf-8 -*-

from network import WLAN, STA_IF, AP_IF
from machine import idle

# Constants
WIFI_SSID = 'PressAnyKey'       # WIFI network to connect to
WIFI_PASSWORD = ''              # WIFI password


def main():
    # Connect to wireless
    nic = WLAN(STA_IF)
    nic.active(True)
    nic.connect(WIFI_SSID, WIFI_PASSWORD)

    print('boot::main(): Connecting to WIFI network')

    # Wait for everything to get set up
    while not nic.isconnected():
        idle()

    print('boot::main(): Connected to WIFI network')

    # Disable access point
    ap_if = WLAN(AP_IF)
    ap_if.active(False)


if __name__ == '__main__':
    main()
