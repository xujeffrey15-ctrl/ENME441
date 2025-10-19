import random
import Shifter
import time

LEDS = {"1":1,"2":2,"3":4,"4":8,"5":16,"6":32,"7":64,"8":128}

class Bugg():
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

	def BugThread(self):
		ThreadBug = threading.Thread(target = self.Bugging(), daemon = True)

	def ChangeSpeed(self,r):
		self.timestep = 0.05/r

	def ChangeWrap(self,b):
		self.isWrapOn = b

	def start(self):
		self.ThreadBug.start()

	def stop(self):
		self.ThreadBug.join()
		self.ShiftCall(0)























