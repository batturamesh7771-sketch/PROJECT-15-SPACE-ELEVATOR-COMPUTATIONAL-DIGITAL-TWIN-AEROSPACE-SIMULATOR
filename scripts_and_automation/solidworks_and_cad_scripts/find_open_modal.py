with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'openToolModal(' in line or 'classList.add(\'open\')' in line:
        print(f'{i+1}: {line.strip()}')
