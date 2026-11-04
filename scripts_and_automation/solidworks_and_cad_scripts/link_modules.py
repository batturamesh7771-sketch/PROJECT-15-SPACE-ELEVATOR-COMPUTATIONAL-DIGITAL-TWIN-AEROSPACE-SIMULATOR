import os

sim_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator"
idx_path = os.path.join(sim_dir, "index.html")

with open(idx_path, "r", encoding="utf-8") as f:
    html = f.read()

target = '<script src="day1_space_elevator_data.js"></script>'
replacement = """<script src="day1_space_elevator_data.js"></script>
  <script src="js/physics_engine.js"></script>
  <script src="js/materials_environment.js"></script>
  <script src="js/orbital_missions.js"></script>
  <script src="js/dashboard_ui.js"></script>"""

html = html.replace('<script src="js/orbital_missions.js"></script>', '')
html = html.replace('<script src="js/materials_environment.js"></script>', '')
html = html.replace(target, replacement)

with open(idx_path, "w", encoding="utf-8") as f:
    f.write(html)

# Also copy to E:\Downloads\index.html
e_path = r"E:\Downloads\index.html"
with open(e_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Linked modules and synced E:\\Downloads\\index.html!")
