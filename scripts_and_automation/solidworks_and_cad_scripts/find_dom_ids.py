with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'id=["\']([^"\']+)["\']', text)
for m in matches:
    if any(k in m for k in ['deck', 'orb', 'env', 'mat', 'tether', 'health', 't-', 'val']):
        print(m)
