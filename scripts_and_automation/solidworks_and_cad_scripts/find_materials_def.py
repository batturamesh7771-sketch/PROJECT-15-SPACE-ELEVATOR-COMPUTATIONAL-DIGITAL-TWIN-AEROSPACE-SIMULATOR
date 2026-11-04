with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'const MATERIALS =' in line:
        for j in range(i, min(len(lines), i+35)):
            clean_line = lines[j].strip().encode('ascii', 'replace').decode('ascii')
            print(f'{j+1}: {clean_line}')
        break
