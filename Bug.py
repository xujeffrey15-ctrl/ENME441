import random
import time
import Shifter

b=8
Testing = Shifter.shifter(23,24,25)

while True:
	jumper = random.randint(0,1)
	if jumper == 0:
		if b <= 128:
			Testing.shiftByte(b)
			b = b << 1
			time.sleep(1)
		else:
			pass
	elif jumper == 1:
		if b >= 4:
			Testing.shiftByte(b)
			b = b >> 1
			time.sleep(1)
		else:
			pass
		
	

























