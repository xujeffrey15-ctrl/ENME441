import json
import math
import time

# LOAD JSON
with open("backup_data.json", "r") as f:
    data = json.load(f)

print(data)

TurretData = data["turrets"]        # dict of turret objects
BallData = data["globes"]           # list of ball objects

numturrets = len(TurretData)
numball = len(BallData)

# We are team 18
ownxcoord = 300*math.cos(1.117010721276371)
ownycoord = 300*math.sin(1.117010721276371)

goanglexy = {}
goanglez = {}

# XY ANGLE CONVERSION
def AngleConversion():

    # Turrets
    for tnum, tinfo in TurretData.items():

        r = tinfo["r"]
        theta = tinfo["theta"]

        xcoord = r * math.cos(theta)
        ycoord = r * math.sin(theta)
        if (xcoord - ownxcoord) != 0:
            m = (ycoord - ownycoord)/(xcoord - ownxcoord)
    
            goanglet = math.degrees(math.atan(m))
    
            goanglexy[f"turret_{tnum}"] = round(goanglet, 2)
            print(tnum)
            print(goanglexy[f"turret_{tnum}"])
            time.sleep(1)
        else:
            pass

    # Balls
    for i, binfo in enumerate(BallData, start=1):

        r = binfo["r"]
        theta = binfo["theta"]
        z = binfo["z"]

        xcoordb = r * math.cos(theta)
        ycoordb = r * math.sin(theta)
        if (xcoordb - ownxcoord) != 0:
            m = (ycoordb - ownycoord)/(xcoordb - ownxcoord)
            dx = xcoordb - ownxcoord
            dy = ycoordb - ownycoord
            dz = z
    
            goangleb = math.degrees(math.atan(m))
            horiz = math.sqrt(dx*dx + dy*dy)
            heightangle = dz/horiz
            angle_z = math.atan(heightangle)
            
            goanglexy[f"ball_{i}"] = round(goangleb, 2)
            goanglez[f"ball_{i}"] = round(angle_z, 2)
            print(i)
            print(goanglexy[f"ball_{i}"])
            print(goanglez[f"ball_{i}"])
            time.sleep(1)
        else:
            pass


# RUN THE CONVERSIONS
AngleConversion()














