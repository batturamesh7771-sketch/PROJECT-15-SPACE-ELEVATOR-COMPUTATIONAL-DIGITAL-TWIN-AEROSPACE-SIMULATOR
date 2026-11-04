import os

dash_js_path = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"
with open(dash_js_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find('injectStyles()')
if idx == -1:
    idx = code.find('function injectStyles')
print('injectStyles around:', idx)
print(code[idx:idx+500].encode('ascii', errors='replace').decode('ascii'))
