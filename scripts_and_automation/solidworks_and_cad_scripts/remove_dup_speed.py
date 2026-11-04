import os, shutil

target_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for the duplicate
# line 10506 and 10509
new_lines = []
skip_next = 0
for i, line in enumerate(lines):
    if "const currentSpeed = climbDirection * nominalSpeedKmh;" in line:
        # Check if the duplicate follows within 5 lines
        if i + 3 < len(lines) and "const currentSpeed = climbDirection * nominalSpeedKmh;" in lines[i+3]:
            # skip this first one
            continue
        elif i + 1 < len(lines) and "const currentSpeed = climbDirection * nominalSpeedKmh;" in lines[i+1]:
            continue
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Saved cleanly deduplicated index.html!")

# Sync to E:\Downloads\index.html
shutil.copyfile(target_file, r'E:\Downloads\index.html')
print("Synced to E:\\Downloads\\index.html successfully!")
