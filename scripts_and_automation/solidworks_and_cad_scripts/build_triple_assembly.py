import os
import json
import base64

def build():
    sim_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator"
    js_dir = os.path.join(sim_dir, "js")
    
    lift_src = r"C:/Users/user/.gemini/antigravity/brain/d33cdfe9-3d93-4bad-be86-c338a8ef7c3f/.user_uploaded/media_1793519356559_969d70d2.glb"
    base_src = r"C:/Users/user/.gemini/antigravity/brain/d33cdfe9-3d93-4bad-be86-c338a8ef7c3f/.user_uploaded/media_1793469056660_d2145f0b.glb"

    with open(os.path.join(js_dir, "three.min.js"), "r", encoding="utf-8") as f:
        three_js = f.read()
    with open(os.path.join(js_dir, "OrbitControls.js"), "r", encoding="utf-8") as f:
        orbit_controls = f.read()
    with open(os.path.join(js_dir, "GLTFLoader.js"), "r", encoding="utf-8") as f:
        gltf_loader = f.read()

    with open(lift_src, "rb") as f:
        lift_b64 = base64.b64encode(f.read()).decode("ascii")
    with open(base_src, "rb") as f:
        base_b64 = base64.b64encode(f.read()).decode("ascii")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Space Elevator CAD Complete Simulation</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
    body {{ background-color: #030508; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; overflow: hidden; }}
    #canvas-container {{ width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; }}
    
    /* Aerospace Telemetry HUD */
    #hud {{
      position: absolute; top: 20px; left: 20px; width: 420px;
      background: rgba(8, 14, 24, 0.92); backdrop-filter: blur(14px);
      border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px;
      padding: 16px 20px; box-shadow: 0 16px 48px rgba(0, 0, 0, 0.85);
      pointer-events: auto; z-index: 10;
    }}
    .hud-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid rgba(56, 189, 248, 0.25); padding-bottom: 8px; }}
    .hud-title {{ font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 1.5px; }}
    .hud-badge {{ font-size: 10px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); padding: 3px 8px; border-radius: 4px; font-weight: 600; font-family: monospace; }}
    
    .telemetry-row {{ display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px; align-items: center; }}
    .telemetry-label {{ color: #94a3b8; }}
    .telemetry-val {{ font-weight: 600; color: #f8fafc; font-feature-settings: "tnum"; font-family: "SF Mono", Consolas, Monaco, monospace; }}
    .highlight-geo {{ color: #4ade80; font-weight: 700; }}
    .highlight-alert {{ color: #f87171; font-weight: 700; }}
    .highlight-gold {{ color: #fbbf24; font-weight: 700; }}
    
    /* Mission Control Panel */
    #controls-panel {{
      position: absolute; bottom: 20px; left: 20px; width: 420px;
      background: rgba(8, 14, 24, 0.92); backdrop-filter: blur(14px);
      border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px;
      padding: 16px 20px; box-shadow: 0 16px 48px rgba(0, 0, 0, 0.85);
      z-index: 10;
    }}
    .panel-title {{ font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .btn-group {{ display: flex; gap: 8px; margin-bottom: 10px; }}
    button {{
      flex: 1; padding: 9px 10px; background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8; border-radius: 4px;
      font-size: 11px; font-weight: 600; cursor: pointer; text-transform: uppercase;
      letter-spacing: 0.5px; transition: all 0.2s ease;
    }}
    button:hover {{ background: #38bdf8; color: #030712; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }}
    button.active {{ background: #0284c7; color: #ffffff; border-color: #38bdf8; box-shadow: 0 0 14px rgba(2, 132, 199, 0.6); }}
    button#btn-brake.active {{ background: #dc2626; border-color: #ef4444; color: #ffffff; box-shadow: 0 0 14px rgba(220, 38, 38, 0.6); }}
    
    .slider-container {{ margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(56, 189, 248, 0.2); }}
    .slider-label {{ font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between; }}
    input[type=range] {{ width: 100%; margin-top: 6px; accent-color: #38bdf8; cursor: pointer; }}

    /* Altitude Profile Bar */
    #profile-container {{
      position: absolute; right: 24px; top: 24px; bottom: 24px; width: 68px;
      background: rgba(8, 14, 24, 0.85); backdrop-filter: blur(8px);
      border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 6px;
      display: flex; flex-direction: column; align-items: center;
      padding: 16px 0; z-index: 10;
    }}
    #profile-track {{ position: relative; width: 6px; height: 100%; background: #1e293b; border-radius: 3px; cursor: pointer; }}
    #profile-marker {{
      position: absolute; left: -6px; width: 18px; height: 8px;
      background: #38bdf8; border-radius: 4px; box-shadow: 0 0 14px #38bdf8;
      transform: translateY(50%); transition: bottom 0.05s linear;
    }}
    .profile-node {{
      position: absolute; left: -4px; width: 14px; height: 3px;
      background: #64748b; border-radius: 1px;
    }}
    .profile-tag {{
      position: absolute; font-size: 9px; color: #94a3b8; right: 18px;
      white-space: nowrap; transform: translateY(50%); font-family: monospace;
    }}

    /* Model Loading Indicator */
    #loader-overlay {{
      position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(3, 5, 8, 0.94); display: flex; flex-direction: column;
      justify-content: center; align-items: center; z-index: 100;
      transition: opacity 0.4s ease;
    }}
    .spinner {{
      width: 48px; height: 48px; border: 3px solid rgba(56, 189, 248, 0.2);
      border-top-color: #38bdf8; border-radius: 50%;
      animation: spin 1s linear infinite; margin-bottom: 16px;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .loader-text {{ font-size: 14px; color: #38bdf8; font-weight: 600; letter-spacing: 1px; font-family: monospace; }}
  </style>

  <!-- Embedded Three.js, Controls & GLTFLoader -->
  <script>{three_js}</script>
  <script>{orbit_controls}</script>
  <script>{gltf_loader}</script>
  <script src="day1_space_elevator_data.js"></script>
</head>
<body>
  <div id="loader-overlay">
    <div class="spinner"></div>
    <div class="loader-text" id="loader-msg">ATTACHING UPPER SPACE STATION & LIFT TO TETHER...</div>
  </div>

  <div id="canvas-container"></div>

  <!-- Real-Time Aerospace Telemetry HUD -->
  <div id="hud">
    <div class="hud-header">
      <span class="hud-title">Space Elevator Lift Simulation</span>
      <span class="hud-badge" id="badge-status">ASCENDING</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Mission Elapsed Time</span>
      <span class="telemetry-val" id="val-time">00d 00h 00m</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Climber Altitude h(t)</span>
      <span class="telemetry-val highlight-gold" id="val-altitude">35,786.00 km</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Radial Velocity v_r</span>
      <span class="telemetry-val" id="val-velocity">450.0 km/h</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Effective Net Gravity g_eff</span>
      <span class="telemetry-val" id="val-geff">0.0000 m/s²</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Newtonian Gravity g(r)</span>
      <span class="telemetry-val" id="val-g">0.2242 m/s²</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Centrifugal Outward a_c</span>
      <span class="telemetry-val" id="val-ac">0.2242 m/s²</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Axial Cable Tension T(r)</span>
      <span class="telemetry-val" id="val-tension">582.40 kN</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Coriolis Libration Force</span>
      <span class="telemetry-val highlight-alert" id="val-coriolis">364.61 N</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Hyperbolic Energy C3</span>
      <span class="telemetry-val" id="val-c3">-0.05 km²/s²</span>
    </div>
    <div class="telemetry-row">
      <span class="telemetry-label">Orbital Regime</span>
      <span class="telemetry-val highlight-geo" id="val-regime">★ GEOSTATIONARY ZERO-G (35,786 km) ★</span>
    </div>
  </div>

  <!-- Mission Control Center -->
  <div id="controls-panel">
    <div class="panel-title">Tether Climber Drive System</div>
    <div class="btn-group">
      <button id="btn-ascend" class="active">▲ Ascend</button>
      <button id="btn-descend">▼ Descend</button>
      <button id="btn-brake">■ Brake / Hold</button>
    </div>
    <div class="panel-title">Camera Guidance Locks</div>
    <div class="btn-group">
      <button id="cam-climber" class="active">Climber Lift</button>
      <button id="cam-base">Earth Port</button>
      <button id="cam-geo">Upper Station</button>
      <button id="cam-full">Full System</button>
    </div>
    <div class="slider-container">
      <div class="slider-label">
        <span>Simulation Warp Speed</span>
        <span id="slider-val" style="color:#38bdf8; font-weight:700;">100x</span>
      </div>
      <input type="range" id="time-slider" min="1" max="1000" value="100">
    </div>
  </div>

  <!-- Vertical Visual Altitude Tracker -->
  <div id="profile-container">
    <div id="profile-track">
      <div class="profile-node" style="bottom: 0%;"></div>
      <div class="profile-tag" style="bottom: 0%;">0 km (Earth Port)</div>
      
      <div class="profile-node" style="bottom: 35.786%;"></div>
      <div class="profile-tag" style="bottom: 35.786%;">35,786 km (GEO)</div>
      
      <div class="profile-node" style="bottom: 100%;"></div>
      <div class="profile-tag" style="bottom: 100%;">100,000 km (Apex)</div>
      
      <div id="profile-marker" style="bottom: 35.786%;"></div>
    </div>
  </div>

  <script>
    const SKETCHFAB_LIFT_B64 = "{lift_b64}";
    const SKETCHFAB_BASE_B64 = "{base_b64}";

    function base64ToArrayBuffer(base64) {{
      const binary_string = window.atob(base64);
      const len = binary_string.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {{
        bytes[i] = binary_string.charCodeAt(i);
      }}
      return bytes.buffer;
    }}

    // =========================================================================
    // PHYSICAL CONSTANTS (EARTH EQUATORIAL ECEF FRAME)
    // =========================================================================
    const MU = 3.986004418e14;          // Standard gravitational parameter [m^3/s^2]
    const R_E = 6378137.0;              // Earth equatorial radius [m]
    const OMEGA = 7.2921159e-5;         // Earth sidereal rotation [rad/s]
    const R_GEO = Math.pow(MU / Math.pow(OMEGA, 2), 1/3); // 42,164.17 km
    const H_GEO = R_GEO - R_E;          // 35,786 km
    const H_APEX = 100000000.0;         // 100,000 km
    const M_CLIMBER = 20000.0;          // 20 metric tons [kg]
    const SIGMA_WORK = 65.0e9;          // 65 GPa working stress
    const RHO = 2260.0;                 // Graphene density [kg/m^3]
    const L_C = SIGMA_WORK / (RHO * 9.798); // Characteristic length: 2,935.4 km

    // Scaled Simulation 3D Spatial Units
    const BASE_Y = 0.0;
    const GEO_Y = 220.0;
    const APEX_Y = 400.0;
    const ALT_TO_SCENE = APEX_Y / (H_APEX / 1000.0);

    // Initial Climber Position at Middle of Rope (GEO ~35,786 km)
    let climbAltitudeKm = 35786.0;
    let climbDirection = 1; // 1 = Up, -1 = Down, 0 = Hold
    let nominalSpeedKmh = 450.0; // 450 km/h baseline velocity
    let timeScale = 100;
    let cameraMode = 'climber';
    let simElapsedSec = 0;

    // =========================================================================
    // THREE.JS SCENE SETUP
    // =========================================================================
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x030508, 0.0008);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 8000);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, powerPreference: "high-performance" }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.3;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;

    // Lighting Setup
    const sunLight = new THREE.DirectionalLight(0xffffff, 2.8);
    sunLight.position.set(300, 250, 300);
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0x38bdf8, 1.2);
    fillLight.position.set(-200, -80, -200);
    scene.add(fillLight);

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    scene.add(ambientLight);

    // Starfield Background
    const starGeo = new THREE.BufferGeometry();
    const starCount = 3500;
    const starPos = new Float32Array(starCount * 3);
    for(let i = 0; i < starCount * 3; i += 3) {{
      starPos[i] = (Math.random() - 0.5) * 4000;
      starPos[i+1] = (Math.random() - 0.5) * 4000;
      starPos[i+2] = (Math.random() - 0.5) * 4000;
    }}
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
    scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({{ color: 0xffffff, size: 1.6, transparent: true, opacity: 0.85 }})));

    // Earth Ocean Sphere at Sea Level
    const earthRadius = 900;
    const earthGeo = new THREE.SphereGeometry(earthRadius, 64, 32);
    const earthMat = new THREE.MeshStandardMaterial({{ color: 0x075985, roughness: 0.6, metalness: 0.2 }});
    const earthMesh = new THREE.Mesh(earthGeo, earthMat);
    earthMesh.position.set(0, -earthRadius, 0);
    scene.add(earthMesh);

    // Atmosphere Haze
    const atmoGeo = new THREE.SphereGeometry(earthRadius + 14, 64, 32);
    const atmoMat = new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.16, side: THREE.BackSide }});
    const atmoMesh = new THREE.Mesh(atmoGeo, atmoMat);
    atmoMesh.position.set(0, -earthRadius, 0);
    scene.add(atmoMesh);

    // Continuous Physical Graphene Tether Ribbon from Earth (Y=0) to Apex (Y=400)
    const tetherCurve = new THREE.LineCurve3(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, APEX_Y, 0));
    const tetherGeo = new THREE.TubeGeometry(tetherCurve, 100, 0.25, 8, false);
    const tetherMat = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, emissive: 0x0284c7, roughness: 0.2, metalness: 0.95 }});
    scene.add(new THREE.Mesh(tetherGeo, tetherMat));

    // Dynamic Moving Climber Node (Mounts the DM Space Lift in middle of rope)
    const climberNode = new THREE.Group();
    scene.add(climberNode);

    // Active beacon on the moving lift
    const beacon = new THREE.PointLight(0x38bdf8, 3.5, 45);
    beacon.position.set(0, 2.0, 0);
    climberNode.add(beacon);

    // =========================================================================
    // LOAD 3 AUTHENTIC SKETCHFAB CAD ASSETS:
    // 1) Base Platform ON GROUND (Y = 0, Upright anchor)
    // 2) Lift Climber IN MIDDLE OF ROPE (Smooth travelling along tether)
    // 3) Upper Space Station AT TIP / APEX OF ROPE (day1_space_elevator.glb)
    // =========================================================================
    const gltfLoader = new THREE.GLTFLoader();
    let loadedModels = 0;
    const totalModels = 3;
    function checkLoaded() {{
      loadedModels++;
      if (loadedModels >= totalModels) {{
        const overlay = document.getElementById('loader-overlay');
        overlay.style.opacity = '0';
        setTimeout(() => overlay.style.display = 'none', 300);
      }}
    }}

    // 1. Earth Port Base Station CAD ON GROUND (Upright at Y = 0)
    const baseBuffer = base64ToArrayBuffer(SKETCHFAB_BASE_B64);
    let baseStationModel = null;
    gltfLoader.parse(baseBuffer, '', (gltf) => {{
      baseStationModel = gltf.scene;
      baseStationModel.traverse((child) => {{
        if (child.isMesh) child.material.side = THREE.DoubleSide;
      }});

      baseStationModel.rotation.set(0, 0, 0);
      const box = new THREE.Box3().setFromObject(baseStationModel);
      const size = new THREE.Vector3();
      box.getSize(size);

      const targetHeight = 400.0;
      const scaleFactor = targetHeight / (size.y || 1000.0);
      baseStationModel.scale.set(scaleFactor, scaleFactor, scaleFactor);
      baseStationModel.position.set(0, 0, 0);
      scene.add(baseStationModel);
      console.log('1. Earth Port Base Station anchored ON GROUND at Y=0!');
      checkLoaded();
    }}, (err) => console.error('Error loading base station:', err));

    // 2. DM Space Lift CAD IN MIDDLE OF ROPE (Climber)
    const liftBuffer = base64ToArrayBuffer(SKETCHFAB_LIFT_B64);
    gltfLoader.parse(liftBuffer, '', (gltf) => {{
      const liftModel = gltf.scene;
      liftModel.traverse((child) => {{
        if (child.isMesh) child.material.side = THREE.DoubleSide;
      }});

      const box = new THREE.Box3().setFromObject(liftModel);
      const center = new THREE.Vector3();
      box.getCenter(center);
      const size = new THREE.Vector3();
      box.getSize(size);

      liftModel.position.x = -center.x;
      liftModel.position.y = -center.y;
      liftModel.position.z = -center.z;

      const targetClimberHeight = 16.0;
      const liftScale = targetClimberHeight / (size.y || 1.0);
      
      const liftWrapper = new THREE.Group();
      liftWrapper.scale.set(liftScale, liftScale, liftScale);
      liftWrapper.add(liftModel);

      climberNode.add(liftWrapper);
      console.log('2. DM Space Lift mounted in sky on the tether rope!');
      checkLoaded();
    }}, (err) => console.error('Error loading lift:', err));

    // 3. Upper Space Station CAD AT TIP OF ROPE (day1_space_elevator.glb)
    function mountUpperStation(gltf) {{
      const stationModel = gltf.scene;
      stationModel.traverse((child) => {{
        if (child.isMesh) child.material.side = THREE.DoubleSide;
      }});

      const box = new THREE.Box3().setFromObject(stationModel);
      const center = new THREE.Vector3();
      box.getCenter(center);
      const size = new THREE.Vector3();
      box.getSize(size);

      stationModel.position.x = -center.x;
      stationModel.position.y = -center.y;
      stationModel.position.z = -center.z;

      // Scale station to fit as the orbital apex counterweight complex
      const targetHeight = 45.0;
      const stationScale = targetHeight / (size.y || 4000.0);

      const stationWrapper = new THREE.Group();
      stationWrapper.scale.set(stationScale, stationScale, stationScale);
      stationWrapper.add(stationModel);

      // Mount at the top tip of the rope (Y = APEX_Y = 400)
      stationWrapper.position.set(0, APEX_Y, 0);
      scene.add(stationWrapper);
      console.log('3. Upper Space Station mounted at TIP OF ROPE (Y=' + APEX_Y + ')!');
      checkLoaded();
    }}

    // Load Upper Station: Try memory buffer first (if present), else load file
    if (window.DAY1_SPACE_ELEVATOR_B64) {{
      const upperBuffer = base64ToArrayBuffer(window.DAY1_SPACE_ELEVATOR_B64);
      gltfLoader.parse(upperBuffer, '', mountUpperStation, (err) => console.error('Error parsing upper station buffer:', err));
    }} else {{
      gltfLoader.load('day1_space_elevator.glb', mountUpperStation, null, (err) => {{
        console.error('Error loading day1_space_elevator.glb:', err);
        checkLoaded();
      }});
    }}

    // Initial Camera Target Position (Looking at lift at middle of rope)
    const initialSceneY = climbAltitudeKm * ALT_TO_SCENE;
    climberNode.position.set(0, initialSceneY, 0);
    camera.position.set(0, initialSceneY + 12, 38);
    controls.target.set(0, initialSceneY + 2, 0);

    // =========================================================================
    // FIRST-PRINCIPLES AEROSPACE PHYSICS COMPUTATION
    // =========================================================================
    function computePhysics(altitudeKm, climbSpeedKmh) {{
      const altM = altitudeKm * 1000.0;
      const r = R_E + altM;
      const vRadialMs = (climbSpeedKmh * 1000.0) / 3600.0;

      // Newtonian Gravity
      const g = MU / Math.pow(r, 2);

      // Centrifugal Acceleration
      const a_c = Math.pow(OMEGA, 2) * r;

      // Net Effective Gravity
      const g_eff = g - a_c;

      // Transverse Coriolis Libration Force
      const f_coriolis = 2.0 * M_CLIMBER * OMEGA * vRadialMs;

      // Pearson Exponential Cable Tension Law
      const phi = (R_E / L_C) * (1.0 + 0.5 * Math.pow(R_E / R_GEO, 3) - (R_E / r) - 0.5 * (r / R_GEO) * Math.pow(R_E / R_GEO, 2));
      const A_base = (1.25 * M_CLIMBER * (9.798 - Math.pow(OMEGA, 2) * R_E)) / SIGMA_WORK;
      const A_r = A_base * Math.exp(phi);
      const tensionN = A_r * SIGMA_WORK;

      // Hyperbolic Excess Orbital Injection Energy C3 = v_tangential^2 - v_escape^2
      const v_tan = OMEGA * r;
      const v_esc = Math.sqrt((2.0 * MU) / r);
      const c3 = (Math.pow(v_tan, 2) - Math.pow(v_esc, 2)) / 1e6;

      // Orbital Altitude Regime
      let regime = 'Troposphere / Sea Level';
      if(altitudeKm > 100 && altitudeKm <= 2000) regime = 'Low Earth Orbit (LEO)';
      else if(altitudeKm > 2000 && altitudeKm < 35500) regime = 'Medium Earth Orbit (MEO)';
      else if(Math.abs(altitudeKm - 35786) <= 400) regime = '★ GEOSTATIONARY ZERO-G (35,786 km) ★';
      else if(altitudeKm >= 36000 && altitudeKm < 99000) regime = 'Super-GEO (Centrifugal Dominance)';
      else if(altitudeKm >= 99000) regime = 'Apex Counterweight (Interplanetary Sling)';

      return {{ g, a_c, g_eff, f_coriolis, tensionN, c3, regime }};
    }}

    // =========================================================================
    // UI & CONTROLS INTERACTION
    // =========================================================================
    const btnAscend = document.getElementById('btn-ascend');
    const btnDescend = document.getElementById('btn-descend');
    const btnBrake = document.getElementById('btn-brake');
    const badgeStatus = document.getElementById('badge-status');

    btnAscend.addEventListener('click', () => {{
      climbDirection = 1;
      updateDriveState('ASCENDING', btnAscend);
    }});
    btnDescend.addEventListener('click', () => {{
      climbDirection = -1;
      updateDriveState('DESCENDING', btnDescend);
    }});
    btnBrake.addEventListener('click', () => {{
      climbDirection = 0;
      updateDriveState('HOLD / BRAKE', btnBrake);
    }});

    function updateDriveState(label, activeBtn) {{
      document.querySelectorAll('#controls-panel .btn-group:first-of-type button').forEach(b => b.classList.remove('active'));
      activeBtn.classList.add('active');
      badgeStatus.innerText = label;
    }}

    // Camera Guidance Locks
    document.getElementById('cam-climber').addEventListener('click', (e) => setCamera('climber', e.target));
    document.getElementById('cam-base').addEventListener('click', (e) => setCamera('base', e.target));
    document.getElementById('cam-geo').addEventListener('click', (e) => setCamera('geo', e.target));
    document.getElementById('cam-full').addEventListener('click', (e) => setCamera('full', e.target));

    function setCamera(mode, targetBtn) {{
      cameraMode = mode;
      document.querySelectorAll('#controls-panel .btn-group:nth-of-type(2) button').forEach(b => b.classList.remove('active'));
      targetBtn.classList.add('active');

      if(mode === 'base') {{
        controls.target.set(0, 10, 0);
        camera.position.set(0, 30, 60);
      }} else if(mode === 'geo') {{
        controls.target.set(0, APEX_Y, 0);
        camera.position.set(0, APEX_Y + 25, 75);
      }} else if(mode === 'full') {{
        controls.target.set(0, 200, 0);
        camera.position.set(0, 250, 520);
      }}
    }}

    // Warp Speed Slider
    const timeSlider = document.getElementById('time-slider');
    const sliderVal = document.getElementById('slider-val');
    timeSlider.addEventListener('input', (e) => {{
      timeScale = parseFloat(e.target.value);
      sliderVal.innerText = timeScale + 'x';
    }});

    // Altitude Bar Click Navigation
    document.getElementById('profile-track').addEventListener('click', (e) => {{
      const rect = e.currentTarget.getBoundingClientRect();
      const clickY = e.clientY - rect.top;
      const frac = 1.0 - (clickY / rect.height);
      climbAltitudeKm = Math.max(0, Math.min(100000, frac * 100000.0));
    }});

    // DOM Telemetry Elements
    const elTime = document.getElementById('val-time');
    const elAlt = document.getElementById('val-altitude');
    const elVel = document.getElementById('val-velocity');
    const elGeff = document.getElementById('val-geff');
    const elG = document.getElementById('val-g');
    const elAc = document.getElementById('val-ac');
    const elTension = document.getElementById('val-tension');
    const elCoriolis = document.getElementById('val-coriolis');
    const elC3 = document.getElementById('val-c3');
    const elRegime = document.getElementById('val-regime');
    const elMarker = document.getElementById('profile-marker');

    // =========================================================================
    // DYNAMIC ANIMATION & SMOOTH TRAVEL LOOP
    // =========================================================================
    let lastTime = performance.now();

    function animate(currentTime) {{
      requestAnimationFrame(animate);

      const deltaSec = Math.min((currentTime - lastTime) / 1000.0, 0.1);
      lastTime = currentTime;

      // Integrate Smooth Climber Motion along the rope
      if(climbDirection !== 0) {{
        const deltaHours = (deltaSec * timeScale) / 3600.0;
        climbAltitudeKm += climbDirection * nominalSpeedKmh * deltaHours;

        if(climbAltitudeKm >= 100000.0) {{
          climbAltitudeKm = 100000.0;
          climbDirection = 0;
          updateDriveState('AT APEX', btnBrake);
        }} else if(climbAltitudeKm <= 0.0) {{
          climbAltitudeKm = 0.0;
          climbDirection = 0;
          updateDriveState('AT EARTH PORT', btnBrake);
        }}
      }}

      simElapsedSec += deltaSec * timeScale;

      // Smoothly update climber 3D position along the tether rope
      const sceneY = climbAltitudeKm * ALT_TO_SCENE;
      climberNode.position.set(0, sceneY, 0);

      // Compute Aerospace Physics Telemetry
      const currentSpeed = climbDirection * nominalSpeedKmh;
      const p = computePhysics(climbAltitudeKm, currentSpeed);

      // Update HUD Values
      const days = Math.floor(simElapsedSec / 86400);
      const hours = Math.floor((simElapsedSec % 86400) / 3600);
      const mins = Math.floor((simElapsedSec % 3600) / 60);
      elTime.innerText = `${{String(days).padStart(2,'0')}}d ${{String(hours).padStart(2,'0')}}h ${{String(mins).padStart(2,'0')}}m`;
      elAlt.innerText = `${{climbAltitudeKm.toFixed(2)}} km`;
      elVel.innerText = `${{Math.abs(currentSpeed).toFixed(1)}} km/h`;
      elGeff.innerText = `${{p.g_eff.toFixed(4)}} m/s²`;
      elG.innerText = `${{p.g.toFixed(4)}} m/s²`;
      elAc.innerText = `${{p.a_c.toFixed(4)}} m/s²`;
      elTension.innerText = `${{(p.tensionN / 1000.0).toFixed(2)}} kN`;
      elCoriolis.innerText = `${{Math.abs(p.f_coriolis).toFixed(2)}} N`;
      elC3.innerText = `${{p.c3.toFixed(2)}} km²/s²`;
      elRegime.innerText = p.regime;

      // Update Visual Altitude Marker
      const pct = (climbAltitudeKm / 100000.0) * 100.0;
      elMarker.style.bottom = `${{pct}}%`;

      // Camera Follow Mode (Tracks the climber lift smoothly in the sky)
      if(cameraMode === 'climber') {{
        const targetPos = new THREE.Vector3(0, sceneY + 2.0, 0);
        controls.target.lerp(targetPos, 0.1);
        camera.position.y += (targetPos.y + 10.0 - camera.position.y) * 0.1;
      }}

      controls.update();
      renderer.render(scene, camera);
    }}

    requestAnimationFrame(animate);

    // Responsive Resize Handler
    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});
  </script>
</body>
</html>
"""

    out_paths = [
        r"E:\Downloads\index.html",
        os.path.join(sim_dir, "index.html"),
        r"C:\Users\user\.gemini\antigravity\brain\d33cdfe9-3d93-4bad-be86-c338a8ef7c3f\index.html"
    ]

    for p in out_paths:
        with open(p, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generated: {p} ({len(html_content):,} bytes)")

if __name__ == "__main__":
    build()
