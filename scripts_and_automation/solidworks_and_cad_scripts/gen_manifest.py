import os, hashlib

files_to_hash = [
    r'C:\Users\user\Downloads\international_space_elevator.glb',
    r'C:\Users\user\Downloads\dm_space_day_1_-_space_elevator (1).glb',
    r'C:\Users\user\Downloads\dm_space_day_1_-_space_elevator.glb',
    r'C:\Users\user\Downloads\day1_space_elevator.glb',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\day1_space_elevator.glb',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\day1_space_elevator_data.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\physics_engine.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\materials_environment.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\orbital_missions.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\css\dashboard.css',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\models\Apex_Counterweight_Hub.obj',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\models\Earth_Port_Platform.obj',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\models\GEO_Orbital_Station.obj',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\models\Tether_Climber_20T.obj'
]

lines = ["# Preserved Baseline Engineering & CAD Asset Manifest\n",
         "**Generated:** 2 November 2026\n",
         "**Compliance:** Master Directive V3.0 — Section 1\n\n",
         "| Asset / Source File | Size (Bytes) | SHA-256 Checksum | System Role |\n",
         "| :--- | :--- | :--- | :--- |\n"]

for p in files_to_hash:
    if os.path.exists(p):
        size = os.path.getsize(p)
        name = os.path.basename(p)
        with open(p, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        role = "CAD Model (Protected)" if p.endswith('.glb') or p.endswith('.obj') else "Core Simulation Engine"
        lines.append(f"| `{name}` | {size:,} | `{h}` | {role} |\n")

docs_dir = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\docs'
os.makedirs(docs_dir, exist_ok=True)
manifest_path = os.path.join(docs_dir, 'preserved_baseline_manifest.md')

with open(manifest_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Generated {manifest_path} with {len(files_to_hash)} assets")
