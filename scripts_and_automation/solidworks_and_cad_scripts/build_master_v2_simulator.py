import os, base64

def generate_v2():
    sim_dir = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator'
    js_dir = os.path.join(sim_dir, 'js')

    with open(os.path.join(js_dir, 'three.min.js'), 'r', encoding='utf-8') as f:
        three_js = f.read()
    with open(os.path.join(js_dir, 'OrbitControls.js'), 'r', encoding='utf-8') as f:
        orbit_controls = f.read()
    with open(os.path.join(js_dir, 'GLTFLoader.js'), 'r', encoding='utf-8') as f:
        gltf_loader = f.read()

    lift_src = r'C:/Users/user/.gemini/antigravity/brain/d33cdfe9-3d93-4bad-be86-c338a8ef7c3f/.user_uploaded/media_1793530091601_5342d98b.glb'
    base_src = r'C:/Users/user/.gemini/antigravity/brain/d33cdfe9-3d93-4bad-be86-c338a8ef7c3f/.user_uploaded/media_1793469056660_d2145f0b.glb'

    with open(lift_src, 'rb') as f:
        lift_b64 = base64.b64encode(f.read()).decode('ascii')
    with open(base_src, 'rb') as f:
        base_b64 = base64.b64encode(f.read()).decode('ascii')

    # Read base textures if available
    tex_dir = os.path.join(sim_dir, 'textures')
    earth_tex = 'textures/earth_blue_marble.jpg' if os.path.exists(os.path.join(tex_dir, 'earth_blue_marble.jpg')) else ''

    print('Ready to assemble master V2 HTML')

if __name__ == '__main__':
    generate_v2()
