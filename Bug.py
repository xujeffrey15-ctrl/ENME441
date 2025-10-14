import random
import time
import Shifter

b = 8

while True:
	Testing = Shifter.shifter(23,24,25,b)
	jumper = random.randint(1,2)
	if jumper == 1:
		Testing.shiftByte()
		b = b<<1
		time.sleep(0.5)
	elif jumper == 2:
		Testing.shiftByte()
		b = b>>1
		time.sleep(0.5)












