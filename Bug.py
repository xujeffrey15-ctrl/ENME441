import random
import Shifter
import time

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}

class bug():
	def __init__(self,LightningBug,timestep=0.5,x=3,isWrapOn=True):
		self.LightningBug = LightningBug
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.x = x

	def ShiftCall(self,b):
		self.LightningBug.shiftByte(b)
		time.sleep(self.timestep)

	def bugging(self):
		b = LEDS[str(self.x)]

		while True:
			jumper = random.randint(0,1)
			if self.isWrapOn == False:
				if b <= 2:
					b = b<<1
					self.ShiftCall(b)
				if b >= 64:
					b = b>>1
					self.ShiftCall(b)
				else:
					if jumper == 1:
						b = b<<1
						self.ShiftCall(b)
					elif jumper == 0:
						b = b>>1
						self.ShiftCall(b)

			if self.isWrapOn == True:
				if b < 1:
					b = 128
				if b > 128:
					b = 1
				else:
					if jumper == 1:
						b = b<<1
						self.ShiftCall(b)
					elif jumper == 0:
						b = b>>1
						self.ShiftCall(b)

Test = bug(Shifter.shifter(23,25,24))
Test.bugging()









































































