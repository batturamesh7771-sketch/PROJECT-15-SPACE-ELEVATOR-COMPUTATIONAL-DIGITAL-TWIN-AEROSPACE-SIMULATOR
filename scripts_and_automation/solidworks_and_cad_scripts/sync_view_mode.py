import os
import shutil

src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"

with open(src_js, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update activeViewMode initial state to 'full'
content = content.replace("activeViewMode: 'climber',", "activeViewMode: 'full',", 1)

# 2. Update view tiles active class in HTML template
content = content.replace('<div class="se-view-tile active" data-mode="climber">', '<div class="se-view-tile" data-mode="climber">', 1)
content = content.replace('<div class="se-view-tile" data-mode="full">', '<div class="se-view-tile active" data-mode="full">', 1)

with open(src_js, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated activeViewMode to 'full' in dashboard_ui.js")
