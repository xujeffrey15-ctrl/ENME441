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

        goanglet = math.degrees(math.atan2((ycoord - ownycoord), (xcoord - ownxcoord)))

        goanglexy[f"turret_{tnum}"] = round(goanglet, 2)
        print(goanglexy[f"turret_{tnum}"])
        time.sleep(0.5)

    # Balls
    for i, binfo in enumerate(BallData, start=1):

        r = binfo["r"]
        theta = binfo["theta"]
        z = binfo["z"]

        xcoordb = r * math.cos(theta)
        ycoordb = r * math.sin(theta)
        dx = xcoordb - ownxcoord
        dy = ycoordb - ownycoord
        dz = z

        goangleb = math.degrees(math.atan2((ycoordb - ownycoord), (xcoordb - ownxcoord)))
        horiz = math.sqrt(dx*dx + dy*dy)
        angle_z = math.atan2(dz, horiz)
        
        goanglexy[f"ball_{i}"] = round(goangleb, 2)
        goanglez[f"ball_{i}"] = round(angle_z, 2)
        print(goanglexy[f"ball_{i}"])
        print(goanglexy[f"ball_{i}"])
        time.sleep(0.5)


# RUN THE CONVERSIONS
AngleConversion()







