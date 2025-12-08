#Code to stitch together JSON Reader and Motor Code while recording crucial data for calibration

#Imports
import Json_Reader
import multiprocessing 

#Global variables
XY = Json_Reader.goanglexy                        #Calculated in-plane rotations
Z = Json_Reader.goanglez                          #Calculated out-of-plane rotations
numturrets = len(Json_Reader.TurretData)          #Number of turrets for automation
numball = len(Json_Reader.BallData)               #Number of stationary ball targets for automation

class Stepper_Motors():
    def Motor_To_Shift_Register(self, desired_angle):            #Converts both desired angles to a single string of 8 bit binary code for shift register
        #Has to be able to take in angle requests and combine the results from both process into a single 8 bit string
        Motor_wiring = [
        
        

class calibration():
    def self_calibration(): #Can be used if you know the magnitude and direction of the previous rotation
        calibration_magnitude = mag
        calibration_direction = dir
        while calibration_magnitude >= 0.5:
            calibration_magnitude = calibration_magnitude + calibration_magnitude/2
            calibration_direction = -calibration_direction
            #motor continously rotate between 1.5 times the other direction, eventually it should rest close to 90 which is the desired starting line
        #Preferably the code will interupt the automation code


        
