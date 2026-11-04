with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'openToolModal\([^)]*\)', text)
for m in matches:
    print(m.group(0))
