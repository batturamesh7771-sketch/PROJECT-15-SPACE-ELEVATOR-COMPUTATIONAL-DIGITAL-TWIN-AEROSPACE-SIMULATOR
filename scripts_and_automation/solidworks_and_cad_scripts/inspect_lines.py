import os

path = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Update checkLoaded to safety-dismiss after timeout or when models finish
# Find checkLoaded
for i, line in enumerate(lines):
    if "function checkLoaded() {" in line:
        check_idx = i
        break

# Let's see the lines of checkLoaded
print('Found checkLoaded at line', check_idx + 1)

# 2. Find groundElevatorToLatLng HUD updates
hud_update_start = -1
for i in range(10160, 10200):
    if "document.getElementById('val-loc')" in lines[i]:
        hud_update_start = i
        break

print('Found val-loc at line', hud_update_start + 1)
