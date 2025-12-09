#Code to stitch together JSON Reader and Motor Code while recording crucial data for calibration

#Imports
from Motor_Code_Project import Stepper
import RPi.GPIO as GPIO
import Json_Reader
import multiprocessing

#Global variables
XY = Json_Reader.goanglexy                        #Calculated in-plane rotations
Z = Json_Reader.goanglez                          #Calculated out-of-plane rotations
numturrets = len(Json_Reader.TurretData)          #Number of turrets for automation
numball = len(Json_Reader.BallData)               #Number of stationary ball targets for automation

class Stepper_Motors():
   def __init__(self):
      self.s = shifter(16, 21, 20)
      self.lock = multiprocessing.Lock()
      self.m1 = Stepper(self.s, self.lock, 0)
      self.m2 = Stepper(self.s, self.lock, 1)
      self.angle = 0

   def Calibration(self,toggle):
      calibration_magnitude = 120
      if toggle == 1:
         # Calibrate motors to 90 degrees
         while abs((self.angle - 90)) >= 0.5:
            self.m1.goAngle(calibration_magnitude)
            self.m2.goAngle(calibration_magnitude)
            self.m1.both.wait()
            self.m2.both.wait()
            self.angle += calibration_magnitude
            calibration_magnitude = (3*(calibration_magnitude - self.angle))/2 
            print(self.angle)
         print("Motors Calibrated")

         # Test Laser
         GPIO.output(11,1)
         time.sleep(3)
         GPIO.output(11,0)
         print("Laser Primed")
      else:
         pass

   def Manual_Motors(self,toggle,diff):
      if toggle == 1:
         self.m1.goAngle(diff)
         self.m2.goAngle(diff)
         self.m1.both.wait()
         self.m2.both.wait()
         print("Motors rotation completed")
      else:
         pass
   
   def Automated_Motors(self):
      for turrets in range(1, numturrets):
         self.m1.goAngle(XY[f"turret_{turrets}"])
         self.m2.goAngle(Z[f"turret_{turrets}"])
         self.m1.both.wait()
         self.m2.both.wait()

         GPIO.output(11,1)
         print("Laser Engaged")
         time.sleep(3)
         GPIO.output(11,0)
    
      for balls in range(1, numball):
         self.m1.goAngle(XY[f"ball_{balls}"])
         self.m2.goAngle(Z[f"ball_{balls}"])
         self.m1.both.wait()
         self.m2.both.wait()
    
         GPIO.output(11,1)
         print("Laser Engaged")
         time.sleep(3)
         GPIO.output(11,0)
