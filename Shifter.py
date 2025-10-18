import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)  

class shifter:
  def __init__ (self,serialPin,clockPin,latchPin):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    GPIO.setup(serialPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT, initial=0)
    GPIO.setup(clockPin, GPIO.OUT, initial=0)  

  def shiftByte(self,b):
    print("I'm running")
    print(b)
    for i in range(8):
      print(self.serialPin)
      print(b)
      print(GPIO.output(self.serialPin, b & (1<<i)))
      GPIO.output(self.serialPin, b & (1<<i))
      print(self.clockPin)
      GPIO.output(self.clockPin,1)
      time.sleep(0)
      GPIO.output(self.clockPin,0)
    GPIO.output(self.latchPin,1)
    print(self.latchPin)
    time.sleep(0)
    GPIO.output(self.latchPin,0) 




































