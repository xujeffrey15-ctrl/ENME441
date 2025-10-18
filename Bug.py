import random
import Shifter
import time

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}
LightningBug = Shifter.shifter(23,25,24)

class bug():
	def __init__(self,timestep=0.5,x=3,isWrapOn=True):
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.x = x

	def bugging(self):
		b = LEDS[str(self.x)]
		LightningBug.shiftByte(b)
		time.sleep(self.timestep)
		while True:
			jumper = random.randint(0,1)
			if self.isWrapOn == False:
				if jumper == 1:
					b = b<<1
					LightningBug.shiftByte(b)
					time.sleep(self.timestep)
				elif jumper == 0:
					b = b>>1
					LightningBug.shiftByte(b)
					time.sleep(self.timestep)
			if self.isWrapOn == True:
				if b <= 2:
					b = b<<1
					LightningBug.shiftByte(b)
					time.sleep(self.timestep)
				if b >= 64:
					b = b>>1
					LightningBug.shiftByte(b)
					time.sleep(self.timestep)
				else:
					if jumper == 1:
						b = b<<1
						LightningBug.shiftByte(b)
						time.sleep(self.timestep)
					elif jumper == 0:
						b = b>>1
						LightningBug.shiftByte(b)
						time.sleep(self.timestep)

Test = bug()
Test.bugging()


































































