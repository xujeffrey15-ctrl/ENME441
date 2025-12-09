#Code to stitch together JSON Reader and Motor Code while recording crucial data for calibration

#Imports
from Motor_Code_Project import Stepper
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

   def Calibration():
      calibration_magnitude = 120
      calibration_direction = 1

      # Calibrate motors to 90 degrees
      while calibration_magnitude >= 0.5:
         self.m1.goAngle(calibration_magnitude)
         self.m2.goAngle(calibration_magnitude)
         calibration_magnitude = calibration_magnitude + calibration_magnitude/2
         calibration_direction = -calibration_direction
      print("Motors Calibrated")

      # Test Laser
      GPIO.output(11,1)
      time.sleep(3)
      GPIO.output(11,0)
      print("Laser Primed")
   
   def Automated_Motors():
      for turrets in range(1, numturrets):
         self.m1.goAngle(XY[f"turret_{t}"])
         self.m2.goAngle(Z[f"turret_{t}"])
         self.m1.both.wait()
         self.m2.both.wait()

         GPIO.output(11,1)
         print("Laser Engaged")
         time.sleep(3)
         GPIO.output(11,0)
    
      for balls in range(1, numball):
         self.m1.goAngle(XY[f"ball_{b}"])
         self.m2.goAngle(Z[f"ball_{b}"])
         self.m1.both.wait()
         self.m2.both.wait()
    
         GPIO.output(11,1)
         print("Laser Engaged")
         time.sleep(3)
         GPIO.output(11,0)
         

        
        

class calibration():
    def self_calibration(): #Can be used if you know the magnitude and direction of the previous rotation
        
            #motor continously rotate between 1.5 times the other direction, eventually it should rest close to 90 which is the desired starting line
        #Preferably the code will interupt the automation code


        
