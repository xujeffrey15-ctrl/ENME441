ULL CORRECTED PROGRAM

Copy & paste this exactly.

import json
import math
from StepperMulti import Stepper

# LOAD JSON
with open("backup_data.json", "r") as f:
    data = json.load(f)

TurretData = data["turrets"]
BallData = data["globes"]

# Team 18 robot position & facing
robot_angle = 1.117010721276371
robot_angle_deg = math.degrees(robot_angle)

ownxcoord = 300 * math.cos(robot_angle)
ownycoord = 300 * math.sin(robot_angle)

goanglexy = {}
goanglez = {}

def AngleConversion():

    # ---------- TURRETS ----------
    for tnum, tinfo in TurretData.items():

        r = tinfo["r"]
        theta = tinfo["theta"]

        Tx = r * math.cos(theta)
        Ty = r * math.sin(theta)

        dx = Tx - ownxcoord
        dy = Ty - ownycoord

        # world-space angle to turret
        world_angle = math.degrees(math.atan2(dy, dx))

        # relative angle = world_angle - robot_facing
        rel_angle = world_angle - robot_angle_deg

        # normalize to [-180, 180]
        rel_angle = (rel_angle + 180) % 360 - 180

        # turret can only rotate ±90°
        if -90 <= rel_angle <= 90:
            goanglexy[f"turret_{tnum}"] = round(rel_angle, 2)
        else:
            goanglexy[f"turret_{tnum}"] = None

    # ---------- BALLS ----------
    for i, binfo in enumerate(BallData, start=1):

        r = binfo["r"]
        theta = binfo["theta"]
        z = binfo["z"]

        Bx = r * math.cos(theta)
        By = r * math.sin(theta)

        dx = Bx - ownxcoord
        dy = By - ownycoord
        dz = z

        # world-space XY angle
        world_angle = math.degrees(math.atan2(dy, dx))
        rel_angle_xy = world_angle - robot_angle_deg

        # normalize
        rel_angle_xy = (rel_angle_xy + 180) % 360 - 180

        # horizontal distance
        horiz = math.sqrt(dx*dx + dy*dy)

        # Z-axis angle (up/down)
        angle_z = math.degrees(math.atan2(dz, horiz))

        # turret constraint
        if -90 <= rel_angle_xy <= 90:
            goanglexy[f"ball_{i}"] = round(rel_angle_xy, 2)
            goanglez[f"ball_{i}"] = round(angle_z, 2)
        else:
            goanglexy[f"ball_{i}"] = None
            goanglez[f"ball_{i}"] = None


# RUN
AngleConversion()

print("\nXY Angles:", goanglexy)
print("\nZ Angles:", goanglez)























