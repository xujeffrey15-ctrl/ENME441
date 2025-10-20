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

def sensor1(v):
   while GPIO.input(v) == False:
      LTB.stop()
      
def sensor2():
   if GPIO.input(s2) == True:
      LTB.ChangeSpeed(1)
      print(1)
   if GPIO.input(s2) == False:
      LTB.ChangeSpeed(10)
      print(3)

def sensor3():
   if GPIO.input(s3) == True:
      LTB.ChangeWrap(True)
      print(2)
   if GPIO.input(s3) == False:
      LTB.ChangeWrap(False)
      print(4)
      
GPIO.add_event_detect(s1, GPIO.FALLING, callback=sensor1, bouncetime=300)

try:
   while True:
      LTB.Start()
      sensor2()
      sensor3()
except KeyboardInterrupt:
   GPIO.cleanup()
  

































































