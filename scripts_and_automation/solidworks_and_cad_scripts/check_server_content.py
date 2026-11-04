import urllib.request
import hashlib
import os

try:
    res = urllib.request.urlopen('http://127.0.0.1:8090/index.html')
    content = res.read()
    h = hashlib.sha256(content).hexdigest()
    print('Served length:', len(content), 'SHA256:', h)
    text = content.decode('utf-8', errors='replace')
    print('--- SEARCH FOR KEY STRINGS IN SERVED CONTENT ---')
    for s in ['controls-panel', 'hud', 'pac-input', 'dashboard_ui.js', 'space-elevator-ui-root', 'SPACE ELEVATOR']:
        print(f'Contains "{s}":', s in text)
        
    ws_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
    with open(ws_file, 'rb') as f:
        ws_bytes = f.read()
    print('Workspace file length:', len(ws_bytes), 'SHA256:', hashlib.sha256(ws_bytes).hexdigest())
    print('Files identical:', ws_bytes == content)
except Exception as e:
    print('Error checking server:', e)
