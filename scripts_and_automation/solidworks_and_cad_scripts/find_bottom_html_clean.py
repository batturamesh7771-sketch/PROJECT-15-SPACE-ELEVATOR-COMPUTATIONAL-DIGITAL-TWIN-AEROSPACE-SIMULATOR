with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1340, min(len(lines), 1430)):
    # encode to ascii with replace to avoid cp1252 crash
    clean_line = lines[i].strip().encode('ascii', 'replace').decode('ascii')
    print(f'{i+1}: {clean_line}')
