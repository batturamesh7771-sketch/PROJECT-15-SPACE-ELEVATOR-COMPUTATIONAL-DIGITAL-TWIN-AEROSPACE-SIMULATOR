with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'se-bottom-deck' in line:
        for j in range(i, min(len(lines), i+150)):
            print(f'{j+1}: {lines[j].strip()}')
        break
