import random
import Shifter
import time
import threading
import RPi.GPIO as GPIO

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}
(s1,s2,s3) = (17,27,22)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class Bugg():
	def __init__(self, timestep = 0.05, x = 3, isWrapOn = False):
		self.timestep = timestep
		self.isWrapOn = isWrapOn
		self.x = x
		self.__Shifter = Shifter.shifter(23,25,24)

	def ShiftCall(self,bytedata):
		self.__Shifter.shiftByte(bytedata)
		time.sleep(self.timestep)

	def BoundedJump(self,jumper):
		RightBoundedShift = lambda rbx: max(rbx>>1,2)
		LeftBoundedShift = lambda lbx: min(lbx<<1,64)

		if jumper == 0:
			self.ShiftCall(self.x)
			self.x = LeftBoundedShift(self.x)
		if jumper == 1:
			self.ShiftCall(self.x)
			self.x = RightBoundedShift(self.x)

	def UnboundedJump(self,jumper):
		if self.x < 1:
			self.x = 128
		if self.x > 128:
			self.x = 1
		else:
			if jumper == 1:
				self.ShiftCall(self.x)
				self.x = self.x<<1
			elif jumper == 0:
				self.ShiftCall(self.x)
				self.x = self.x>>1

	def Bugging(self):
		jumper = random.randint(0,1)
		if self.isWrapOn == False:
			self.BoundedJump(jumper)
		if self.isWrapOn == True:
			self.UnboundedJump(jumper)
				
	def ChangeSpeed(self,r):
		self.timestep = 0.05/r

	def ChangeWrap(self,b):
		self.isWrapOn = b

	def Start(self):
		while GPIO.input(s1):
			self.Bugging()
				
	def stop(self):
		self.ShiftCall(0)
		while GPIO.input(s1) == False:
			pass











































