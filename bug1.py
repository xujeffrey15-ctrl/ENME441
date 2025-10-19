import threading
import RPi.GPIO as GPIO
import Bug

(s1,s2,s3) = (17,27,22)
Buggg = Bug.Bugg(Shifter.shifter(23,25,24))
GPIO.setmode(GPIO.BCM) 
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
	if GPIO.input(s1) == 0:
		Buggg.stop()
	if GPIO.input(s1) == 1:
		Buggg.start()

