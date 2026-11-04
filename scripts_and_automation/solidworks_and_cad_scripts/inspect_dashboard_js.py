import os

dash_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js'
with open(dash_file, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('updateTelemetry(data) {')
print(code[idx+1000:idx+2500].encode('ascii', errors='replace').decode('ascii'))
