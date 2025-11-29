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
        target_angle = 0

        xcoord = r * math.cos(theta)
        ycoord = r * math.sin(theta)

        if (ownxcoord-xcoord) != 0:
            alpha = math.degrees(abs(math.atan(ownycoord/ownxcoord)))
            beta = math.degrees(abs(math.atan((ownycoord-ycoord)/(ownxcoord-xcoord))))
    
            if abs(alpha) < abs(beta):
                target_angle = abs(alpha) + abs(beta)
            if abs(alpha) > abs(beta):
                target_angle = abs(alpha) - abs(beta)
    
            if theta > math.pi:
                target_angle = -target_angle
            if theta < math.pi:
                pass
    
            goanglexy[f"turret_{tnum}"] = round(target_angle, 2) 
        else:
            pass

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

        if (ownxcoord-xcoordb) != 0:
            alpha = math.degrees(abs(math.atan(ownycoord/ownxcoord)))
            beta = math.degrees(abs(math.atan((ownycoord-ycoordb)/(ownxcoord-xcoordb))))
    
            if abs(alpha) < abs(beta):
                target_angle = abs(alpha) + abs(beta)
            if abs(alpha) > abs(beta):
                target_angle = abs(alpha) - abs(beta)
    
            if theta > math.pi:
                target_angle * (-1)
            if theta < math.pi:
                pass
    
            horiz = math.sqrt(dx*dx + dy*dy)
            angle_z = math.atan2(dz, horiz)
            
            goanglexy[f"ball_{i}"] = round(target_angle, 2)
            goanglez[f"ball_{i}"] = round(angle_z, 2)
        else:
            pass


# RUN THE CONVERSIONS
AngleConversion()

print('\n')
print("XY Angles:", goanglexy)
print('\n')
print("Z Angles:", goanglez)























