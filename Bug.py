import random
import Shifter

b = 8

while True:
	jumper = random.randint(1,2)
	if jumper == 1:
		Shifter(23,25,24)
		b = b<<1
		time.sleep(0.5)
	elif jumper == 2:
		Shifter(23,25,24)
		b = b>>1
		time.sleep(0.5)







































