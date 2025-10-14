import random
import Shifter.py

b = 8
Testing = Shifter(23,24,25,b)

while True:
	jumper = random.randint(1,2)
	if jumper == 1:
		Testing.shiftByte()
		b = b<<1
		time.sleep(0.5)
	elif jumper == 2:
		Testing.shiftByte()
		b = b>>1
		time.sleep(0.5)





