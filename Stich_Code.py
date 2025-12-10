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
        
    def waitBoth(self):
        self.m1.event.wait()               #Wait() command forces 
        self.m2.event.wait()

    # --------------------------------------------------------
    def Calibration(self, toggle):
        if toggle != 1:
            return

        print("Starting calibration sequence...")

        # Move both motors to 90 degrees absolute
        self.m1.goToAngle(90)
        self.m2.goToAngle(90)
        self.waitBoth()

        print("Motors centered at 90°")

        # Laser test
        GPIO.output(11, 1)
        print("Laser ON for calibration test...")
        time.sleep(3)
        GPIO.output(11, 0)

        print("Calibration complete.")

    # --------------------------------------------------------
    def Manual_Motors(self, toggle, diff):
        if toggle != 1:
            return

        print(f"Manual rotation: delta={diff}")

        self.m1.goAngle(diff)
        self.m2.goAngle(diff)
        self.waitBoth()

        print("Manual movement complete")

    # --------------------------------------------------------
    def Automated_Motors(self):
        print("Starting automated turret sequence...")

        # Turrets
        for i in range(1, numturrets):
            x_angle = XY[f"turret_{i}"]
            z_angle = Z[f"turret_{i}"]

            print(f"Turret {i}: moving to X={x_angle}, Z={z_angle}")

            self.m1.goToAngle(x_angle)
            self.m2.goToAngle(z_angle)
            self.waitBoth()

            GPIO.output(11, 1)
            print("Laser firing...")
            time.sleep(3)
            GPIO.output(11, 0)

        # Balls
        for i in range(1, numball):
            x_angle = XY[f"ball_{i}"]
            z_angle = Z[f"ball_{i}"]

            print(f"Ball {i}: moving to X={x_angle}, Z={z_angle}")

            self.m1.goToAngle(x_angle)
            self.m2.goToAngle(z_angle)
            self.waitBoth()

            GPIO.output(11, 1)
            print("Laser firing...")
            time.sleep(3)
            GPIO.output(11, 0)

        print("Automation sequence complete.")
