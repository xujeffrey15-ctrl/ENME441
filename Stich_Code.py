from Motor_Code_Project import Stepper
import Json_Reader
import multiprocessing
import RPi.GPIO as GPIO
import time

#Calculated Target Data
XY = Json_Reader.goanglexy #In-plane angles
Z = Json_Reader.goanglez   #Height angles
numturrets = len(Json_Reader.TurretData)   #Number of turrets in Json
numball = len(Json_Reader.BallData)        #Number of ball targets in Json

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)

class Stepper_Motors:
    def __init__(self):
        self.lock = multiprocessing.Lock()
        self.m1 = Stepper(self.lock, 0)    #Initiate Motor 1 with self.index = 0
        self.m2 = Stepper(self.lock, 1)    #Initiate Motor 2 with self.index = 1

        self.x_angle_tracking = 0
        self.z_angle_tracking = 0
        
    def waitBoth(self):
        self.m1.event.wait()               #Each motor process has its own multiprocessing.event that signals its own completion. 
        self.m2.event.wait()               #By waiting for both to finish, you can gurantee that the entire turret won't move on until both mtors are done.

    def Engage_Laser(self):
        print("Laser Engaging!")
        GPIO.output(11,1)
        time.sleep(3)
        GPIO.output(11,0)
        print("Target Eliminated")
 
    def Calibrate_X_Angles(self, toggle):
        if toggle !=1:
            return
        self.x_angle_tracking = 0 = 0
        print("X Origin Calibrated!")

    def Calibrate_Z_Angles(self, toggle):
        if toggle !=1:
            return
        self.z_angle_tracking = 0 = 0
        print("Z Origin Calibrated!")
        
    def Manual_Motors(self, toggle, x_angle_diff, z_angle_diff):
        if toggle != 1:
            return

        self.m1.goAngle(x_angle_diff)
        self.m2.goAngle(z_angle_diff)
        self.waitBoth()

        self.x_angle_tracking += x_angle_diff
        self.z_angle_tracking += z_angle_diff

        print("Manual movement complete")

    def Automated_Motors(self):
        print("Starting automated turret sequence...")

        # Turrets
        for i in range(1, numturrets):
            x_angle_diff = XY[f"turret_{i}"]
            z_angle_diff = Z[f"turret_{i}"]

            print(f"Turret {i}: moving to X={x_angle_diff}, Z={z_angle_diff}")

            self.m1.goAngle(x_angle_diff)
            self.m2.goAngle(z_angle_diff)
            self.waitBoth()

            self.x_angle_tracking = x_angle_diff
            self.z_angle_tracking = z_angle_diff

            self.Engage_Laser()
            
        # Balls
        for i in range(1, numball):
            x_angle_diff = XY[f"ball_{i}"]
            z_angle_diff = Z[f"ball_{i}"]

            print(f"Ball {i}: moving to X={x_angle_diff}, Z={z_angle_diff}")

            self.m1.goAngle(x_angle_diff)
            self.m2.goAngle(z_angle_diff)
            self.waitBoth()

            self.x_angle_tracking = x_angle_diff
            self.z_angle_tracking = z_angle_diff

            self.Engage_Laser()

        print("Automation sequence complete.")
