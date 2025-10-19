import random
import Shifter
import time
import threading
import RPi.GPIO as GPIO

(s1,s2,s3) = (17,27,22)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}

class Bug():
	def __init__(self,LightningBug, timestep = 0.05, x = 3, isWrapOn = False):
		self.LightningBug = LightningBug
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.x = x


	def ShiftCall(self,bytedata):
		self.LightningBug.shiftByte(bytedata)
		time.sleep(self.timestep)

	def BoundedJump(self,jumper):
		RightBoundedShift = lambda rbx: max(rbx>>1,2)
		LeftBoundedShift = lambda lbx: min(lbx<<1,64)

		if jumper == 0:
			self.x = LeftBoundedShift(self.x)
			self.ShiftCall(self.x)
		if jumper == 1:
			self.x = RightBoundedShift(self.x)
			self.ShiftCall(self.x)

	def UnboundedJump(self,jumper):
		if self.x < 1:
			self.x = 128
		if self.x > 128:
			self.x = 1
		else:
			if jumper == 1:
				self.x = self.x<<1
				self.ShiftCall(self.x)
			elif jumper == 0:
				self.x = self.x>>1
				self.ShiftCall(self.x)

	def Bugging(self):
		self.ShiftCall(LEDS[str(self.x)])
		while True:
			print(self.isWrapOn)
			jumper = random.randint(0,1)
			if self.isWrapOn == False:
				self.BoundedJump(jumper)
			if self.isWrapOn == True:
				self.UnboundedJump(jumper)

	def stop(self):
		BugThread.join()
		self.ShiftCall(0)
		print("Stopped")
		
	def start(self):
		print("Started")
		BugThread.start()

	def ChangeSpeed(self,r):
		Bug.timestep = self.timestep/r

	def ChangeWrap(self,boo):
		Bug.isWrapOn = boo

BugSet = Bug(Shifter.shifter(23,25,24))
BugThread = threading.Thread(target=(BugSet.Bugging))
BugThread.daemon = True

while True:
	GPIO.add_event_detect(s1, GPIO.RISING, callback=BugSet.start(), bouncetime = 500)
	GPIO.add_event_detect(s1, GPIO.FALLING, callback=BugSet.stop(), bouncetime = 500)





















