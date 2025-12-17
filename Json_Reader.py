import json
import math
import requests

#url = "http://192.168.1.254:8000/positions.json"   # Replace with your URL

#response = requests.get(url)
#response.raise_for_status()             # Raises an error for bad status codes

#data = response.json()                  # Parse JSON directly

with open("backup_data.json", "r") as f:
    data = json.load(f)

print(data)

TurretData = data["turrets"]        # dict of turret objects
BallData = data["globes"]           # list of ball objects

goanglexy = {}
goanglez = {}

#Team 18
Own_R_Value = 300
Own_Theta_Value = TurretData["18"]["theta"]
Own_X_Coord = 300*math.cos(Own_Theta_Value)
Own_Y_Coord = 300*math.sin(Own_Theta_Value)
Own_Z_Coord = 0
slope = Own_X_Coord/Own_Y_Coord
y_intercept = slope*(0-Own_X_Coord) + Own_Y_Coord

def compute_angles(Previous_X, Previous_Y, Previous_Z, Target_X, Target_Y, Target_Z=0):
    if (Own_X_Coord - Target_X) != 0 and (Previous_X - Own_X_Coord) != 0:
        #For In Plane Rotations
        Side_a = math.sqrt((Previous_Y - Own_Y_Coord)**2 + (Previous_X - Own_X_Coord)**2)
        Side_b = math.sqrt((Target_Y - Previous_Y)**2 + (Target_X - Previous_X)**2)
        Side_c = math.sqrt((Own_Y_Coord - Target_Y)**2 + (Own_X_Coord - Target_X)**2)
    
        cosine_val_x = ((-1*Side_b**2) + (Side_a**2) + (Side_c**2))/(2*Side_c*Side_a)
        cosine_val_x = max(-1, min(1, cosine_val_x))
        Angle_diff_x = math.acos(cosine_val_x)
        
        if Target_Y > Previous_Y:
            Angle_diff_x = - Angle_diff_x
        if Target_Y <= Previous_Y:
            Angle_diff_x = Angle_diff_x
    
        #For Out of Plane Rotations
        Side_z = Target_Z - Previous_Z
        Height_Hypotenuse = math.sqrt((Side_c**2) + (Side_z**2))
        
        cosine_val_z = ((-1*Side_z**2) + (Side_c**2) + (Height_Hypotenuse**2))/(2*Side_c*Height_Hypotenuse)
        cosine_val_z = max(-1, min(1, cosine_val_z))
        Angle_diff_z = math.acos(cosine_val_z)
    
        if Target_Z >= Previous_Z:
            Angle_diff_z = Angle_diff_z
        if Target_Z < Previous_Z:
            Angle_diff_z = - Angle_diff_z
    
        return math.degrees(Angle_diff_x), math.degrees(Angle_diff_z)
    else:
        return 0.0, 0.0

def AngleConversion():
    Previous_X = 0
    Previous_Y = y_intercept
    Previous_Z = 0
    
    for tnum, tinfo in TurretData.items():
        r = tinfo["r"]
        theta = tinfo["theta"]

        # Convert polar to XY
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        xy_angle, _ = compute_angles(Previous_X, Previous_Y, Previous_Z, x, y, 0)   # turrets have no Z angle
    
        goanglexy[f"turret_{tnum}"] = round(xy_angle,2)
        goanglez[f"turret_{tnum}"] = round(0,2)
        
        Previous_X = x
        Previous_Y = y

        print(Previous_X)
        print(Previous_Y)

    # ---- BALLS ----
    for i, binfo in enumerate(BallData, start=1):

        r = binfo["r"]
        theta = binfo["theta"]
        z = binfo["z"]

        x = r * math.cos(theta)
        y = r * math.sin(theta)

        xy_angle, z_angle = compute_angles(Previous_X,Previous_Y,Previous_Z,x, y, z)

        goanglexy[f"ball_{i}"] = round(xy_angle, 2)
        goanglez[f"ball_{i}"]  = round(z_angle, 2)

        Previous_X = x
        Previous_Y = y
        Previous_Z = z

AngleConversion()

print("\nXY Angles:", goanglexy)
print("\nZ Angles:", goanglez)


