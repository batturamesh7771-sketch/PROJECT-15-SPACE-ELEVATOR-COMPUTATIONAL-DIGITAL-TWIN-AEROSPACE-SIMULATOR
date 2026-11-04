import os

index_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect CSS for old elements: #hud, #graphs-container, #controls-panel, #profile-container, #search-box-container
print('Contains #hud in style:', '#hud {' in html or '#hud{' in html)
print('Contains #graphs-container in style:', '#graphs-container {' in html)
print('Contains #controls-panel in style:', '#controls-panel {' in html)
print('Contains #search-box-container in style:', '#search-box-container {' in html)
print('Contains #profile-container in style:', '#profile-container {' in html)
