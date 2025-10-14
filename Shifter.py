serialPin = 23
clockPin = 25
latchPin = 24
import random
b = 8

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(serialPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial=0)  # start latch & clock low
GPIO.setup(clockPin, GPIO.OUT, initial=0)  

def ping(p):
  GPIO.output(p,1)
  time.sleep(0)
  GPIO.output(p,0)

def shiftByte(b):
  for i in range(8):
    GPIO.output(serialPin, b & (1<<i))
    ping(clockPin)
  ping(latchPin)

while True:
  jump = random.randint(0,1)
  if jump == 1:
    shiftByte(b)
    if b !=128:
      b = b<<1
    else:
      pass
    time.sleep(0.5)
  elif jump == 0:
    shiftByte(b)
    if b!=1:
      b = b>>1
    else:
      pass
    time.sleep(0.5)











