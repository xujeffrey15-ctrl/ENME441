from Shifter import shifter
from Motor_Code_Project import Stepper
import Json_Reader
import multiprocessing
import RPi.GPIO as GPIO
import time

# Load angle data
XY = Json_Reader.goanglexy
Z = Json_Reader.goanglez

numturrets = len(Json_Reader.TurretData)
numball = len(Json_Reader.BallData)

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)


class Stepper_Motors:
    def __init__(self):
        self.s = shifter(16, 21, 20)
        self.lock = multiprocessing.Lock()

        self.m1 = Stepper(self.s, self.lock, 0)
        self.m2 = Stepper(self.s, self.lock, 1)

    # --------------------------------------------------------
    def waitBoth(self):
        self.m1.event.wait()
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
