import os

path = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace duplicated currentSpeed
c = re_sub = c.replace(
"""      // Compute Physics Telemetry

      const currentSpeed = climbDirection * nominalSpeedKmh;



      // Compute Physics Telemetry
      const currentSpeed = climbDirection * nominalSpeedKmh;
      const p = computePhysics(climbAltitudeKm, currentSpeed, currentLat);""",
"""      // Compute Physics Telemetry
      const currentSpeed = climbDirection * nominalSpeedKmh;
      const p = computePhysics(climbAltitudeKm, currentSpeed, currentLat);"""
)

# Remove any remaining updateDrive calls
c = c.replace("updateDrive('AT APEX STATION', btnBrake);", "// at apex station")
c = c.replace("updateDrive('AT EARTH PORT', btnBrake);", "// at earth port")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Cleaned duplicate and updateDrive calls successfully.")
