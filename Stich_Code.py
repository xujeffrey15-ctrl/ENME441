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
 
    def Calibration(self, toggle):
        Calibration_Angle = 30
        if toggle != 1:
            return
            
        print("Starting calibration sequence...")
        
        for i in range(1,3):
            self.m1.goAngle(Calibration_Angle)
            self.m2.goAngle(Calibration_Angle)
            self.waitBoth()
            self.x_angle_tracking += Calibration_Angle
            self.z_angle_tracking += Calibration_Angle

        for n in range(1,3):
            self.m1.goAngle(-Calibration_Angle)
            self.m2.goAngle(-Calibration_Angle)
            self.waitBoth()
            self.x_angle_tracking += -Calibration_Angle
            self.z_angle_tracking += -Calibration_Angle
            
        self.Engage_Laser()

        print("Calibration complete.")

    def Manual_Motors(self, toggle, x_angle, z_angle):
        if toggle != 1:
            return

        self.m1.goAngle(x_angle)
        self.m2.goAngle(z_angle)
        self.waitBoth()

        self.x_angle_tracking = x_angle
        self.z_angle_tracking = z_angle

        print("Manual movement complete")

    def Automated_Motors(self):
        print("Starting automated turret sequence...")

        # Turrets
        for i in range(1, numturrets):
            x_angle = XY[f"turret_{i}"]
            z_angle = Z[f"turret_{i}"]

            print(f"Turret {i}: moving to X={x_angle}, Z={z_angle}")

            self.m1.goAngle(x_angle)
            self.m2.goAngle(z_angle)
            self.waitBoth()

            self.x_angle_tracking = x_angle
            self.z_angle_tracking = z_angle

            self.Engage_Laser()
            
        # Balls
        for i in range(1, numball):
            x_angle = XY[f"ball_{i}"]
            z_angle = Z[f"ball_{i}"]

            print(f"Ball {i}: moving to X={x_angle}, Z={z_angle}")

            self.m1.goAngle(x_angle)
            self.m2.goAngle(z_angle)
            self.waitBoth()

            self.x_angle_tracking = x_angle
            self.z_angle_tracking = z_angle

            self.Engage_Laser()

        print("Automation sequence complete.")
