import random
import Shifter
import time

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}
LightningBug = Shifter.shifter(23,25,24)

class Bug():
	def __init__(self,LightningBug, timestep = 0.05, x = 3, isWrapOn = False):
		self.LightningBug = LightningBug
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.x = x
		global b
		b = LEDS[str(self.x)]

	def ShiftCall(self,a):
		self.LightningBug.shiftByte(a)
		time.sleep(self.timestep)

	def Bugging(self):
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

	def stop(self):
		self.Bugging(0)
		print("Stopped")
		
	def start(self):
		print("Started")
		self.Bugging(b)

	def ChangeSpeed(self,r):
		timestep = timestep/r

	def ChangeWrap(self,boo):
		isWrapOn = boo
s1 = 17
s2 = 27
s3 = 22
GPIO.setup(s1, GPIO.IN)
GPIO.setup(s2, GPIO.IN)
GPIO.setup(s3, GPIO.IN)
BugSet = Bug(Shifter.shifter(23,25,24))

if GPIO.INPUT(s1,1):
	BugSet.start()
if GPIO.INPUT(s1,0):
	BugSet.stop()
if GPIO.INPUT(s2,1):
	BugSet.ChangeSpeed(3)
if GPIO.INPUT(s2,0):
	BugSet.ChangeSpeed(1)
if GPIO.INPUT(s3,1):
	BugSet.ChangeWrap(True)
if GPIO.INPUT(s3,0):
	BugSet.ChangeWrap(False)












































































