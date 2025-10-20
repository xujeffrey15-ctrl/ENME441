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
	@classmethod
	def __init__(self, timestep = 0.5, x = 3, isWrapOn = False):
		Bugg.timestep = timestep
		Bugg.isWrapOn = isWrapOn
		Bugg.x = x
		self.__Shifter = Shifter.shifter(23,25,24)

	def ShiftCall(self,bytedata):
		self.__Shifter.shiftByte(bytedata)
		time.sleep(Bugg.timestep)

	def BoundedJump(self,jumper):
		RightBoundedShift = lambda rbx: max(rbx>>1,2)
		LeftBoundedShift = lambda lbx: min(lbx<<1,64)

		if jumper == 0:
			self.ShiftCall(self.x)
			Bugg.x = LeftBoundedShift(Bugg.x)
		if jumper == 1:
			self.ShiftCall(self.x)
			Bugg.x = RightBoundedShift(Bugg.x)

	def UnboundedJump(self,jumper):
		if Bugg.x < 1:
			Bugg.x = 128
		if Bugg.x > 128:
			Bugg.x = 1
		else:
			if jumper == 1:
				self.ShiftCall(Bugg.x)
				Bugg.x = Bugg.x<<1
			elif jumper == 0:
				self.ShiftCall(Bugg.x)
				Bugg.x = Bugg.x>>1

	def Bugging(self):
		jumper = random.randint(0,1)
		if Bugg.isWrapOn == False:
			self.BoundedJump(jumper)
		if Bugg.isWrapOn == True:
			self.UnboundedJump(jumper)
			
	def ChangeSpeed(self,r):
		Bugg.timestep = 0.5/r

	def ChangeWrap(self,b):
		Bugg.isWrapOn = b
		return self.isWrapOn

	def Start(self):
		self.Bugging()
				
	def stop(self):
		self.ShiftCall(0)
























































