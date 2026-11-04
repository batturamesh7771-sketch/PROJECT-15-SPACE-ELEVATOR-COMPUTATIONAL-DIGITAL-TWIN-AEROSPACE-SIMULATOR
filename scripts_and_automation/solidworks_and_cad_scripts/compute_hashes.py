import os, hashlib

files_to_hash = [
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\day1_space_elevator.glb',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\day1_space_elevator_data.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\physics_engine.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\materials_environment.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\orbital_missions.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js',
    r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\css\dashboard.css'
]

# Check models folder too
models_dir = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\models'
if os.path.exists(models_dir):
    for f in os.listdir(models_dir):
        files_to_hash.append(os.path.join(models_dir, f))

# Check Phase 1 root
phase1_root = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1'
for f in os.listdir(phase1_root):
    if f.endswith('.glb') or f.endswith('.gltf') or f.endswith('.step') or f.endswith('.stl'):
        files_to_hash.append(os.path.join(phase1_root, f))

print('=== SHA256 HASH MANIFEST ===')
manifest = []
for fpath in files_to_hash:
    if os.path.exists(fpath) and os.path.isfile(fpath):
        with open(fpath, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        size = os.path.getsize(fpath)
        rel = os.path.basename(fpath)
        print(f'{rel} ({size} bytes): {h}')
        manifest.append({'file': rel, 'path': fpath, 'size': size, 'sha256': h})
