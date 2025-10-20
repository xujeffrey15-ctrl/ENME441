import random
import Shifter
import time
import threading

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}

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
		self.Bugging()

	def stop(self):
		self.ShiftCall(0)
		while True:
			pass






































