with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div class="se-modal-backdrop"' in line or 'id="se-modal-backdrop"' in line:
        for j in range(max(0, i-2), min(len(lines), i+15)):
            print(f'{j+1}: {lines[j].strip()}')
        break
