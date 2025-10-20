import threading
import time
import RPi.GPIO as GPIO
from Bug import Bugg

s1 = 17
s2 = 19
s3 = 26
GPIO.setmode(GPIO.BCM) 
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LTB = Bugg()
      
def sensor2():
   if GPIO.input(s2) == True:
      LTB.ChangeSpeed(1)
   if GPIO.input(s2) == False:
      LTB.ChangeSpeed(10)

def sensor3():
   if GPIO.input(s3) == True:
      LTB.ChangeWrap(True)
   if GPIO.input(s3) == False:
      LTB.ChangeWrap(False)
      
try:
   while True:
      if GPIO.input(s1) == True:
         LTB.Start()
         sensor2()
         sensor3()
      else:
         LTB.stop()
except KeyboardInterrupt:
   GPIO.cleanup()
  






































































