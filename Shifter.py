import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)  

class shifter:
  def __init__ (self,serialPin,clockPin,latchPin):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    GPIO.setup(serialPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)  

  def _ping(self,p):
      GPIO.output(p,1)
      time.sleep(0)
      GPIO.output(p,0)

  def shiftByte(self,b):
    for i in range(8):
      GPIO.output(self.serialPin, b & (1<<i))
      self._ping(self.clockPin)
    self._ping(self.latchPin)









































