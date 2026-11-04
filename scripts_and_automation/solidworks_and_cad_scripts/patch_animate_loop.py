import os

target_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if "const p = computePhysics(climbAltitudeKm, currentSpeed, currentLat);" in line:
        start_idx = i
        break

end_idx = -1
for i, line in enumerate(lines):
    if "if (window.SpaceElevatorUI) {" in line and i > start_idx:
        end_idx = i
        break

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    replacement = """      // Compute Physics Telemetry
      const currentSpeed = climbDirection * nominalSpeedKmh;
      const p = computePhysics(climbAltitudeKm, currentSpeed, currentLat);

"""
    new_lines = lines[:start_idx] + [replacement] + lines[end_idx:]
    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Successfully cleaned up animate loop!")
