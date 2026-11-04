with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1580, 1610):
    print(f'{i+1}: {lines[i].strip()}')
