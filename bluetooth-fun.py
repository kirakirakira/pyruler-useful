# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic structure example for using the BLE Connect Control Pad
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select Controller-> Control Pad.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket

from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.01
cp.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

while True:
    print("WAITING...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    ble.stop_advertising()
    print("CONNECTED")

    # Loop and read packets
    while ble.connected:

        # Keeping trying until a good packet is received
        try:
            packet = Packet.from_stream(uart_server)
        except ValueError:
            continue

        # Only handle button packets
        if isinstance(packet, ButtonPacket) and packet.pressed:
            if packet.button == ButtonPacket.UP:
                cp.red_led = True
                print("Button UP")
            if packet.button == ButtonPacket.DOWN:
                cp.red_led = False
                print("Button DOWN")
            if packet.button == ButtonPacket.LEFT:
                cp.pixels[2] = (0, 255, 0)
                print("Button LEFT")
            if packet.button == ButtonPacket.RIGHT:
                cp.pixels[2] = (255, 0, 255)
                print("Button RIGHT")
            if packet.button == ButtonPacket.BUTTON_1:
                cp.pixels[7] = (0, 255, 255)
                print("Button 1")
            if packet.button == ButtonPacket.BUTTON_2:
                cp.pixels[7] = (0, 0, 0)
                print("Button 2")
            if packet.button == ButtonPacket.BUTTON_3:
                cp.pixels[4] = (54, 25, 158)
                print("Button 3")
            if packet.button == ButtonPacket.BUTTON_4:
                cp.pixels[4] = (255, 0, 255)
                print("Button 4")

    # Disconnected
    print("DISCONNECTED")