import RPi.GPIO as GPIO
import time

class shifter:
  def __init__ (self,serialPin,clockPin,latchPin,b):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    self.b = b
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(serialPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT, initial=0)
    GPIO.setup(clockPin, GPIO.OUT, initial=0)  

  def ping(self,p):
    GPIO.output(p,1)
    time.sleep(0)
    GPIO.output(p,0)

  def shiftByte(self,b):
    for i in range(8):
      GPIO.output(self.serialPin, self.b & (1<<i))
      print('3')
      self.ping(self.clockPin)
      print('4')
      print(b)
    self.ping(self.latchPin)























