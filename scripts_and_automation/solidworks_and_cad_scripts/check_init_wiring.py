import os

idx_path = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect the bottom of the script where SpaceElevatorUI is initialized
idx = html.find("SpaceElevatorUI.init")
print("SpaceElevatorUI.init around:", idx)
print(html[idx-100:idx+800].encode('ascii', errors='replace').decode('ascii'))
