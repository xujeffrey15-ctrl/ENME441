import random
import Shifter
import time

Testing = Shifter.shifter(23,24,25)

try:
	Testing.shiftByte(0b01100110)   # test out the new function
	while 1: pass
except:
 	GPIO.cleanup()



































