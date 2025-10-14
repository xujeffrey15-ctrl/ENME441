class Shifter:
  import RPi.GPIO as GPIO
  import time
  
  def __init__ (self,serialPin,clockPin,latchPin,b):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    self.b = b

  def setup(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.serialPin, GPIO.OUT)
    GPIO.setup(self.latchPin, GPIO.OUT, initial=0)
    GPIO.setup(self.clockPin, GPIO.OUT, initial=0)  

  def __ping(self,p):
    GPIO.output(p,1)
    time.sleep(0)
    GPIO.output(p,0)

  def shiftByte(self,b):
    for i in range(8):
      GPIO.output(self.serialPin, self.b & (1<<i))
      __ping(self.clockPin)
    __ping(self.latchPin)
















