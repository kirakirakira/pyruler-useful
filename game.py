import os
import board
from digitalio import DigitalInOut, Direction
import time
import touchio
import adafruit_dotstar

leddot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
leddot[0] = (128, 0, 128)
leddot.brightness = 0.3

# print(dir(board), os.uname()) # Print a little about ourselves

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

touches = [DigitalInOut(board.CAP0)]
for p in (board.CAP1, board.CAP2, board.CAP3):
    touches.append(touchio.TouchIn(p))

leds = []
for p in (board.LED4, board.LED5, board.LED6, board.LED7):
    led = DigitalInOut(p)
    led.direction = Direction.OUTPUT
    led.value = True
    time.sleep(0.25)
    leds.append(led)
for led in leds:
    led.value = False


cap_touches = [False, False, False, False]


def read_caps():
    t0_count = 0
    t0 = touches[0]
    t0.direction = Direction.OUTPUT
    t0.value = True
    t0.direction = Direction.INPUT
    # funky idea but we can 'diy' the one non-hardware captouch device by hand
    # by reading the drooping voltage on a tri-state pin.
    t0_count = t0.value + t0.value + t0.value + t0.value + t0.value + \
        t0.value + t0.value + t0.value + t0.value + t0.value + \
        t0.value + t0.value + t0.value + t0.value + t0.value
    cap_touches[0] = t0_count > 2
    cap_touches[1] = touches[1].raw_value > 3000
    cap_touches[2] = touches[2].raw_value > 3000
    cap_touches[3] = touches[3].raw_value > 3000
    return cap_touches

while True:
    caps = read_caps()
    time_now = time.monotonic()
    # light up the matching LED
    for i, c in enumerate(caps):
        leds[i].value = c
    if caps[0]:
        time_pressed = time.monotonic()
        print(time_pressed)
        print("time passed ", time_pressed - time_now)
    if caps[1]:
        time_pressed = time.monotonic()
        print(time_pressed)
        print("time passed ", time_pressed - time_now)
    if caps[2]:
        time_pressed = time.monotonic()
        print(time_pressed)
        print("time passed ", time_pressed - time_now)
    if caps[3]:
        time_pressed = time.monotonic()
        print(time_pressed)
        print("time passed ", time_pressed - time_now)
    time.sleep(0.1)
