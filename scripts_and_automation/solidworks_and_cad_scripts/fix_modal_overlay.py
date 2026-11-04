import os
import shutil

src_css = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\css\dashboard.css"
src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"
src_html = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
dst_html = r"E:\Downloads\index.html"

# 1. Fix CSS modal backdrop
with open(src_css, "r", encoding="utf-8") as f:
    css_content = f.read()

# Make sure .se-modal-backdrop is display: none when not open, and only display: flex when .open
old_modal_css = """.se-modal-backdrop {
        position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(1, 4, 9, 0.82);
        backdrop-filter: blur(10px);
        display: flex; align-items: center; justify-content: center;
        z-index: 100;
        opacity: 0; pointer-events: none; transition: opacity 0.25s ease;
    }
    .se-modal-backdrop.open {
        opacity: 1; pointer-events: auto;
    }"""

new_modal_css = """.se-modal-backdrop {
        position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(1, 4, 9, 0.88);
        backdrop-filter: blur(12px);
        display: none !important;
        align-items: center; justify-content: center;
        z-index: 1000;
        opacity: 0; pointer-events: none !important;
        transition: opacity 0.25s ease;
    }
    .se-modal-backdrop.open {
        display: flex !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }"""

if old_modal_css in css_content:
    css_content = css_content.replace(old_modal_css, new_modal_css, 1)
    print("Replaced modal CSS exactly")
else:
    import re
    css_content = re.sub(
        r'\.se-modal-backdrop\s*\{[^}]*\}\s*\.se-modal-backdrop\.open\s*\{[^}]*\}',
        new_modal_css,
        css_content
    )
    print("Replaced modal CSS via regex")

with open(src_css, "w", encoding="utf-8") as f:
    f.write(css_content)
print("Saved dashboard.css")

# 2. Fix dashboard_ui.js modal backdrop class (remove interactive class)
with open(src_js, "r", encoding="utf-8") as f:
    js_content = f.read()

js_content = js_content.replace(
    '<div id="se-modal-backdrop" class="se-modal-backdrop interactive">',
    '<div id="se-modal-backdrop" class="se-modal-backdrop">',
    1
)

with open(src_js, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Saved dashboard_ui.js modal class fix")
