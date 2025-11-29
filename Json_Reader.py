import json
import math

# LOAD JSON
with open("backup_data.json", "r") as f:
    data = json.load(f)

TurretData = data["turrets"]        # dict of turret objects
BallData = data["globes"]           # list of ball objects

# We are team 18
ownxcoord = 300 * math.cos(1.117010721276371)
ownycoord = 300 * math.sin(1.117010721276371)

goanglexy = {}
goanglez = {}

def compute_angles(target_x, target_y, target_z=0):

    dx = target_x - ownxcoord
    dy = target_y - ownycoord
    horiz = math.sqrt(dx*dx + dy*dy)

    # XY angle
    xy_angle = math.degrees(math.atan2(dy, dx))

    # Z angle (0 if target_z=0)
    z_angle = math.degrees(math.atan2(target_z, horiz))
    z_angle = (180 - z_angle) % 360

    return xy_angle, z_angle

def AngleConversion():

    # ---- TURRETS ----
    for tnum, tinfo in TurretData.items():
        r = tinfo["r"]
        theta = tinfo["theta"]

        # Convert polar to XY
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        xy_angle, _ = compute_angles(x, y)   # turrets have no Z angle
    
        goanglexy[f"turret_{tnum}"] = round((xy_angle % 360), 2)

    # ---- BALLS ----
    for i, binfo in enumerate(BallData, start=1):

        r = binfo["r"]
        theta = binfo["theta"]
        z = binfo["z"]

        x = r * math.cos(theta)
        y = r * math.sin(theta)

        xy_angle, z_angle = compute_angles(x, y, z)

        goanglexy[f"ball_{i}"] = round((xy_angle % 360), 2)
        goanglez[f"ball_{i}"]  = round(z_angle, 2)

AngleConversion()

print("\nXY Angles:", goanglexy)
print("\nZ Angles:", goanglez)


































