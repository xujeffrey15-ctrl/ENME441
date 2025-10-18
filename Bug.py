import random
import Shifter
import time

b = 8
Shift = Shifter.shifter(23,25,24)

while True:
	jumper = random.randint(1,2)
	if jumper == 1:
		Shift.shiftByte(b)
		b = b<<1
		time.sleep(0.5)
	elif jumper == 2:
		Shift.shiftByte(b)
		b = b>>1
		time.sleep(0.5)









































