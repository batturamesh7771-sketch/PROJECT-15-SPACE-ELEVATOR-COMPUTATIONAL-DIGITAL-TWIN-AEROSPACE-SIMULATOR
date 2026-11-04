import os, re, shutil

sim_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator"
idx_path = os.path.join(sim_dir, "index.html")
dash_js_path = os.path.join(sim_dir, "js", "dashboard_ui.js")

with open(idx_path, "r", encoding="utf-8") as f:
    orig_html = f.read()

with open(dash_js_path, "r", encoding="utf-8") as f:
    dash_code = f.read()

# Extract injectStyles() and buildDOM() content from dashboard_ui.js to embed directly into index.html
# Find the CSS in dashboard_ui.js
css_start = dash_code.find('const css = `')
if css_start != -1:
    css_start += len('const css = `')
    css_end = dash_code.find('`;', css_start)
    dash_css = dash_code[css_start:css_end]
else:
    dash_css = ""

# Find the HTML in buildDOM()
dom_start = dash_code.find('overlay.innerHTML = `')
if dom_start != -1:
    dom_start += len('overlay.innerHTML = `')
    dom_end = dash_code.find('`;', dom_start)
    dash_dom = dash_code[dom_start:dom_end]
else:
    dash_dom = ""

print(f"Extracted Dashboard CSS length: {len(dash_css)}")
print(f"Extracted Dashboard DOM length: {len(dash_dom)}")
