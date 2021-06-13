import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground import cp

class NonBlockingTimer(object):
  """ Non blocking timer class for use with CircuitPython """
  _STOPPED = 'STOPPED'
  _RUNNING = 'RUNNING'

  def __init__(self, interval=-1):
    """Create a new timer with optional interval. Initial state is _STOPPED.
       Call start() to set status to RUNNING. """
    self._interval = interval
    self._status = NonBlockingTimer._STOPPED
    self._start_time = 0

  @property
  def status(self):
    """Get Status"""
    return self._status

  def next(self):
    """Returns true or false according to the following algorithm:
      if interval <= 0 raise RuntimeError
      if status != RUNNING raise RuntimeError
      if time.monotonic() - start_time > interval
      return True and set start_time = time.monotonic()
      else return False """

    if self._interval <= 0:
      raise RuntimeError('Interval must be > 0')

    if self._status != NonBlockingTimer._RUNNING:
      raise RuntimeError(
          'Timer must be in state RUNNING before calling next()')

    current_time = time.monotonic()
    elapsed = current_time - self._start_time

    if elapsed >= self._interval:
      # The timer has been "triggered"
      self._start_time = current_time
      return True

    return False

  def stop(self):
    """Sets status to STOPPED. Do any cleanup here such as releasing pins,
       etc. Call start() to restart. Does not reset start_time."""
    self._status = NonBlockingTimer._STOPPED

  def start(self):
    """Sets status to RUNNING. Sets start_time to time.monotonic(). Call
       next() repeatedly to determine if the timer has been triggered.
       If interval <= 0 raise a RuntimeError """
    if self._interval <= 0:
      raise RuntimeError('Interval must be > 0')

    self._start_time = time.monotonic()
    self._status = NonBlockingTimer._RUNNING

  def set_interval(self, seconds):
    """ Set the trigger interval time in seconds (float). If interval <= 0
        raise a RuntimeError """
    if seconds <= 0:
      raise RuntimeError('Interval must be > 0')
    self._interval = seconds

  def get_interval(self):
    """Get interval"""
    return self._interval


class BlinkDemo(NonBlockingTimer):
  def __init__(self, index, color):
    super(BlinkDemo, self).__init__(0.1)
    self.index = index
    self.color = color
    cp.pixels[self.index] = self.color
    cp.pixels.brightness = 0.05
  def stop(self):
    cp.pixels[self.index] = (0, 0, 0)
  def next(self):
    if (super(BlinkDemo, self).next()):
        if cp.pixels[self.index] == (0, 0, 0):
            cp.pixels[self.index] = self.color
        else:
            cp.pixels[self.index] = (0, 0, 0)

blinkDemo = BlinkDemo(5, (255, 0, 0))
blinkDemo.start()

while True:
    # cp.pixels[5] = (255, 0, 0)
    blinkDemo.next()
    # This is the only place you should use time.sleep: to set the overall
    # "sampling rate" of your program.
    time.sleep(0.001)