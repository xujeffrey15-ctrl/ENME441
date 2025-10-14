class Shifter:
  import RPi.GPIO as GPIO
  import time
  
  def __init__ (self, serialPin,clockPin,latchPin,b):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    self.b = b

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(serialPin, GPIO.OUT)
  GPIO.setup(latchPin, GPIO.OUT, initial=0)  # start latch & clock low
  GPIO.setup(clockPin, GPIO.OUT, initial=0)  

  def __ping(p):
    GPIO.output(p,1)
    time.sleep(0)
    GPIO.output(p,0)

  def shiftByte(b):
    for i in range(8):
      GPIO.output(serialPin, b & (1<<i))
      __ping(clockPin)
    __ping(latchPin)













