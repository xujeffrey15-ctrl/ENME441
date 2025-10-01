import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
p = 4
GPIO.setup(p, GPIO.OUT)

while True:
	GPIO.output(p, 0)
	sleep(0.5) 
	GPIO.output(p, 1)
	sleep(0.5)