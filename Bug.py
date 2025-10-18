import random
import Shifter
import time

LEDS = {"0":0,"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64}
LightningBug = Shifter.shifter(23,25,24)

class bug():
	def __init__(self,timestep=0.5,x=7,isWrapOn=False):
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.x = x

	def bugging(self):
		b = LEDS[str(self.x)]
		while True:
			jumper = random.randint(0,1)
			if self.isWrapOn == False:
				if jumper == 1:
					LightningBug.shiftByte(b)
					b = b<<1
					time.sleep(self.timestep)
				elif jumper == 0:
					LightningBug.shiftByte(b)
					b = b>>1
					time.sleep(self.timestep)
			if self.isWrapOn == True:
				if b <= 1:
					if jumper == 0:
						LightningBug.shiftByte(b)
						time.sleep(self.timestep)
					elif jumper == 1:
						LightningBug.shiftByte(b)
						b = b<<1
						time.sleep(self.timestep)
				if b >= 32:
					if jumper == 0:
						LightningBug.shiftByte(b)
						b = b>>1
						time.sleep(self.timestep)
					elif jumper == 1:
						LightningBug.shiftByte(b)
						time.sleep(self.timestep)
				else:
					if jumper == 1:
						LightningBug.shiftByte(b)
						b = b<<1
						time.sleep(self.timestep)
					elif jumper == 0:
						LightningBug.shiftByte(b)
						b = b>>1

Test = bug()
Test.bugging()





















































