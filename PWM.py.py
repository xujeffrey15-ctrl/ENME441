import RPi.GPIO as GPIO
import math
import time

GPIO.setmode(GPIO.BCM)
pwmpins =[4,17,27,22,10,9,11,5,6,13]
pwms = {}
Freq = 0.2
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for x in pwmpins:
	GPIO.setup(x,GPIO.OUT)
	pwms[f"pwm{x}"] = GPIO.PWM(x,500)

def ReverseDetection(x):
	print("Reversed!")
	while True:
		t1 = time.time()
		counter1 = 0
		for z in pwmpins:
			pwms[f"pwm{z}"].start((math.sin(2*math.pi*Freq*t1+(counter1*math.pi/11)))**2)
			counter1 += 1
			if GPIO.input(x) == GPIO.LOW:
				break

GPIO.add_event_detect(19, GPIO.FALLING, callback=ReverseDetection, bouncetime=100)

while True:
	try:
		counter = 0
		t = time.time()
		for y in pwmpins:
			pwms[f"pwm{y}"].start((math.sin(2*math.pi*Freq*t-(counter*math.pi/11)))**2)
			counter += 1
	except KeyboardInterrupt:
		print("Code Stopped!")
		exit()	
		
GPIO.cleanup()	














