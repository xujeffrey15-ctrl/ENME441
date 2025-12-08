#Code to stitch together JSON Reader and Motor Code while recording crucial data for calibration
import Json_Reader
import multiprocessing 

class calibration():
    def self_calibration(): #Can be used if you know the magnitude and direction of the previous rotation
        calibration_magnitude = mag
        calibration_direction = dir
        while calibration_magnitude >= 0.5:
            calibration_magnitude = calibration_magnitude + calibration_magnitude/2
            calibration_direction = -calibration_direction
            #motor continously rotate between 1.5 times the other direction, eventually it should rest close to 90 which is the desired starting line
        #Preferably the code will interupt the automation code

    def engage_motors():    #Ideally this code takes on the multithreading instead of Motor_Code for better control. Ideally this code will be able to start two independent motor code and then join them when done
        calibration_thread.start()
        
