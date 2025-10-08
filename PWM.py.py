import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM)
pwmpins =[4,17,27,22,10,9,11,5,6,13]
pwms = {}
Freq = 0.2
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for x in pwmpins:
	GPIO.setup(x,GPIO.OUT)
	pwms[f"pwm{x}"] = GPIO.PWM(x,500)

def ReverseDetection(19):
	print("Reversed!")
	while GPIO.input(19) == GPIO.LOW:
		for z in pwmpins:
			pwms[f"pwm{z}"].start((math.sin(2*math.pi*Freq*time+(counter*math.pi/11)))**2)
			counter += 1


while True:
	try:
		import time
		counter = 0
		time = time.time()
		if GPIO.add_event_detect(19, GPIO.Rising, callback=fn, bouncetime=t_ms) == True:
			for y in pwmpins:
				pwms[f"pwm{y}"].start((math.sin(2*math.pi*Freq*time-(counter*math.pi/11)))**2)
				counter += 1
		else:
			ReverseDetection()

	except KeyboardInterrupt:
		print("Code Stopped!")

pwm.stop()
GPIO.cleanup()