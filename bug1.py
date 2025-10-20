import threading
import RPi.GPIO as GPIO
from Bug import Bugg

(s1,s2,s3) = (17,27,22)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LTB = Bugg()

while True:
   GPIO.add_event_detect(s1, GPIO.RISING, callback=Bugg.Started, bouncetime=1000)
   GPIO.add_event_detect(s1, GPIO.FALLING, callback=Bugg.stop, bouncetime=1000)
  






















