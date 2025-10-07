import RPi.GPIO as GPIO
import math

pwmpins =[4,17,27,22,10,9,11,5,6,13]
pwms = {}
Freq = 0.2

for x in pwmpins:
	GPIO.setup(x,GPIO.OUT)
	pwms[f"pwm{x}"] = GPIO.PWM(x,500)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
	import time
	counter = 0
	time = time.time()

	if GPIO.input(19) == GPIO.HIGH:
		for y in pwmpins:
			pwms[f"pwm{y}"].start((math.sin(2*math.pi*Freq*time-(counter*math.pi/11)))**2)
			counter += 1
	else:
		for z in pwmpins:
			pwms[f"pwm{z}"].start((math.sin(2*math.pi*Freq*time+(counter*math.pi/11)))**2)
			counter += 1