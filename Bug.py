import random
import time
import Shifter

b=8
Testing = Shifter.shifter(23,24,25)

while True:
	if b < 256:
		Testing.shiftByte(b)
		b = b<<1
		time.sleep(0.5)
	elif b >= 2:
		Testing.shiftByte(b)
		b = b>>1
		time.sleep(0.5)

















