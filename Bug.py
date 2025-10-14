import random
import time
import Shifter

b=8
Testing = Shifter.shifter(23,24,25)

while True:
	jumper = random.randint(0,1)
	if jumper == 0:
		b = b << 1
		print(b)
		print(jumper)
		time.sleep(1)
	elif jumper == 1:
		b = b >> 1
		print(b)
		print(jumper)
		time.sleep(1)
		
	























