import json
import math
import time

# LOAD JSON
with open("backup_data.json", "r") as f:
    data = json.load(f)

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

        dx = xcoord - ownxcoord
        dy = ycoord - ownycoord

        target_angle = math.degrees(math.atan2(dy, dx))

        goanglexy[f"turret_{tnum}"] = round(target_angle, 2)

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

        # XY angle
        target_angle = math.degrees(math.atan2(dy, dx))

        # Z angle
        horiz = math.sqrt(dx*dx + dy*dy)
        angle_z = math.atan2(dz, horiz)

        goanglexy[f"ball_{i}"] = round(target_angle, 2)
        goanglez[f"ball_{i}"] = round(angle_z, 2)


# RUN THE CONVERSIONS
AngleConversion()

print('\n')
print("XY Angles:", goanglexy)
print('\n')
print("Z Angles:", goanglez)
























