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

# leds = []
# for p in (board.LED4, board.LED5, board.LED6, board.LED7):
#     led = DigitalInOut(p)
#     led.direction = Direction.OUTPUT
#     led.value = True
#     time.sleep(0.25)
#     leds.append(led)
# for led in leds:
#     led.value = False

cap_to_led = {0: board.LED4, 1: board.LED5, 2: board.LED6, 3: board.LED7}
led_0 = DigitalInOut(board.LED4)
led_1 = DigitalInOut(board.LED5)
led_2 = DigitalInOut(board.LED6)
led_3 = DigitalInOut(board.LED7)
led_0.direction = Direction.OUTPUT
led_1.direction = Direction.OUTPUT
led_2.direction = Direction.OUTPUT
led_3.direction = Direction.OUTPUT

leds = [led_0, led_1, led_2, led_3]

def light_up_sequence(sequence):
    for cap in sequence:
        leds[cap].value = True
        time.sleep(0.25)
        leds[cap].value = False

light_up_sequence([0, 1, 2, 3, 2, 1, 0])


cap_touches = [False, False, False, False]
time_now = time.monotonic()
caps_touched = []

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

time_now = time.monotonic()

def time_passed():
    time_pressed = time.monotonic()
    time_passed = time_pressed - time_now
    return time_passed

while True:
    caps = read_caps()
    # light up the matching LED
    for i, c in enumerate(caps):
        leds[i].value = c
    if caps[0]:
        caps_touched.append(0)
        print(caps_touched)
        print("time passed ", time_passed())
        time_now = time.monotonic()
    if caps[1]:
        caps_touched.append(1)
        print(caps_touched)
        print("time passed ", time_passed())
        time_now = time.monotonic()
    if caps[2]:
        caps_touched.append(2)
        print(caps_touched)
        print("time passed ", time_passed())
        time_now = time.monotonic()
    if caps[3]:
        caps_touched.append(3)
        print(caps_touched)
        print("time passed ", time_passed())
        time_now = time.monotonic()
    time.sleep(0.1)

