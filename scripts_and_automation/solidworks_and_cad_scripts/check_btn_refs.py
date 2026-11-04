import os

idx_path = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    html = f.read()

# Check what btnBrake, btnAscend, timeSlider are in index.html
print("Contains 'const btnBrake' or 'let btnBrake':")
for b in ["btnAscend", "btnDescend", "btnBrake", "timeSlider"]:
    idx = html.find(b)
    print(f"{b} found at {idx}:", html[idx:idx+80].encode('ascii', errors='replace').decode('ascii') if idx != -1 else "NOT FOUND")
