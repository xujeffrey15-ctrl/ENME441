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
   if GPIO.input(v) == True:
      LTB.Start()
   if GPIO.input(v) == False:
      LTB.stop()
      
def sensor2(n):
   if GPIO.input(n) == True:
      LTB.ChangeSpeed(1)
      print(1)
   if GPIO.input(n) == False:
      LTB.ChangeSpeed(10)

def sensor3(g):
   if GPIO.input(g) == True:
      LTB.ChangeWrap(True)
      print(2)
   if GPIO.input(g) == False:
      LTB.ChangeWrap(False)
      
GPIO.add_event_detect(s1, GPIO.BOTH, callback=sensor1, bouncetime=300)
GPIO.add_event_detect(s2, GPIO.BOTH, callback=sensor2, bouncetime=200)
GPIO.add_event_detect(s3, GPIO.BOTH, callback=sensor3, bouncetime=100)

try:
   while True:
      time.sleep(1)
except KeyboardInterrupt:
   GPIO.cleanup()
  























































