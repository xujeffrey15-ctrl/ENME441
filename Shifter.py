import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class shifter:
  def __init__ (self,serialPin,clockPin,latchPin):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    
  def setup(self):
    GPIO.setup(self.serialPin, GPIO.OUT)
    GPIO.setup(self.latchPin, GPIO.OUT, initial=0)
    GPIO.setup(self.clockPin, GPIO.OUT, initial=0)  

  def ping(self,p):
    GPIO.output(p,1)
    time.sleep(0)
    GPIO.output(p,0)

  def shiftByte(self,b):
    for i in range(8):
      GPIO.output(self.serialPin, b & (1<<i))
      self.ping(self.clockPin)
    self.ping(self.latchPin)


























