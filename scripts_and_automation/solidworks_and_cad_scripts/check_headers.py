import base64

with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Scripts\check_script_9.js', 'r', encoding='utf-8') as f:
    for line in f:
        line_s = line.strip()
        if line_s.startswith('const SKETCHFAB_LIFT_B64 ='):
            b64 = line_s.split('=')[1].strip().strip(';').strip('"')
            raw = base64.b64decode(b64[:200])
            print('LIFT Magic header:', raw[:4])
        elif line_s.startswith('const SKETCHFAB_BASE_B64 ='):
            b64 = line_s.split('=')[1].strip().strip(';').strip('"')
            raw = base64.b64decode(b64[:200])
            print('BASE Magic header:', raw[:4])
