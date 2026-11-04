import os, shutil

sim_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator"
idx_path = os.path.join(sim_dir, "index.html")

with open(idx_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Clean up duplicate scripts in <head>
# Ensure exact set of scripts
head_start = html.find("<head>")
head_end = html.find("</head>")

# In <head>, link css/dashboard.css
css_link = '  <link rel="stylesheet" href="css/dashboard.css">\n</head>'
html = html.replace("</head>", css_link)

# Clean up any duplicated scripts
target_scripts = """  <script src="day1_space_elevator_data.js"></script>
  <script src="js/physics_engine.js"></script>
  <script src="js/materials_environment.js"></script>
  <script src="js/orbital_missions.js"></script>
  <script src="js/dashboard_ui.js"></script>"""

# Replace all script inclusions with the single clean block
# Find from day1_space_elevator_data.js to </head>
s_idx = html.find('<script src="day1_space_elevator_data.js"></script>')
e_idx = html.find('<link rel="stylesheet" href="css/dashboard.css">')
html = html[:s_idx] + target_scripts + "\n" + html[e_idx:]

# 2. In <body>, remove the old UI elements:
# <div id="search-box-container">...</div>
# <div id="hud">...</div>
# <div id="graphs-container">...</div>
# <div id="controls-panel">...</div>
# <div id="profile-container">...</div>
# <div id="hint">...</div>

old_elements = [
    html.find('<div id="search-box-container">'),
    html.find('<!-- Real-Time Telemetry HUD -->'),
    html.find('<!-- Dual Real-Time Canvas Graph Panels -->'),
    html.find('<!-- Mission Control Center -->'),
    html.find('<!-- Vertical Visual Altitude Tracker -->'),
    html.find('<div id="hint">')
]

# Find start of search-box-container and end of hint
start_old = html.find('<div id="search-box-container">')
end_hint = html.find('</div>', html.find('<div id="hint">')) + len('</div>')

print(f"Removing old DOM from index {start_old} to {end_hint}")
html = html[:start_old] + '<div id="canvas-container"></div>\n' + html[end_hint:]

# Also remove old styles inside <style>
# From #search-box-container to end of #hint
style_start = html.find("/* Top Google Maps Places Search Bar */")
if style_start == -1:
    style_start = html.find("#search-box-container {")
style_end = html.find("</style>")

clean_style = """    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body { background-color: #010409; color: #f0f6fc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; overflow: hidden; height: 100vh; }
    #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }

    /* Loading Screen */
    #loader-overlay {
      position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
      background: #020617; z-index: 9999; display: flex; flex-direction: column;
      align-items: center; justify-content: center; transition: opacity 0.4s ease;
    }
    .spinner {
      width: 50px; height: 50px; border: 3px solid rgba(56, 189, 248, 0.2);
      border-top-color: #38bdf8; border-radius: 50%; animation: spin 1s linear infinite;
      margin-bottom: 20px;
    }
    .loader-text { color: #38bdf8; font-family: monospace; font-size: 13px; letter-spacing: 2px; }
    @keyframes spin { to { transform: rotate(360deg); } }
  """

s_start = html.find("<style>") + len("<style>\n")
s_end = html.find("</style>")
html = html[:s_start] + clean_style + html[s_end:]

with open(idx_path, "w", encoding="utf-8") as f:
    f.write(html)

# Also sync to E:\Downloads\index.html
shutil.copy2(idx_path, r"E:\Downloads\index.html")
print("Cleaned index.html and synced to E:\\Downloads\\index.html!")
