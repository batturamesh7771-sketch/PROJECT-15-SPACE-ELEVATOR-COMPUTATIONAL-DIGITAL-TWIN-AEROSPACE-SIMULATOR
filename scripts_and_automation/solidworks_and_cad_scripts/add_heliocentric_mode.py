import os
import shutil

src_html = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"
dst_html = r"E:\Downloads\index.html"

# 1. Update dashboard_ui.js to include the Heliocentric View Mode tile
with open(src_js, "r", encoding="utf-8") as f:
    js_text = f.read()

old_tiles = """          <div class="se-view-tile active" data-mode="full">
            ${ICONS.full}<span>Full System</span>
          </div>
        </div>"""

new_tiles = """          <div class="se-view-tile active" data-mode="full">
            ${ICONS.full}<span>Full System</span>
          </div>
          <div class="se-view-tile" data-mode="helio" style="grid-column: span 2;">
            ${ICONS.solar}<span>Heliocentric Orbit View (Sun & Earth Orbit)</span>
          </div>
        </div>"""

if old_tiles in js_text:
    js_text = js_text.replace(old_tiles, new_tiles, 1)
    print("Added Heliocentric View Mode tile to dashboard_ui.js")
else:
    print("Notice: old_tiles pattern not found directly, checking regex")
    import re
    js_text = re.sub(
        r'<div class="se-view-tile[^"]*" data-mode="full">[\s\S]*?<span>Full System</span>[\s\S]*?</div>\s*</div>',
        new_tiles,
        js_text,
        count=1
    )
    print("Replaced tiles via regex")

with open(src_js, "w", encoding="utf-8") as f:
    f.write(js_text)
print("Saved dashboard_ui.js")

# 2. Update index.html to create the Sun mesh, Earth orbit path, and Heliocentric camera logic
with open(src_html, "r", encoding="utf-8") as f:
    html_text = f.read()

# Add Sun and Heliocentric Orbit Group
target_starfield = "scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 1.5, transparent: true, opacity: 0.85 })));"

sun_and_orbit_code = """scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 1.5, transparent: true, opacity: 0.85 })));

    // =========================================================================
    // HELIOCENTRIC SOLAR SYSTEM & EARTH ORBIT REVOLUTION ENGINE (MODE 2)
    // =========================================================================
    const HELIO_ORBIT_RADIUS = 1600.0; // Scaled visual 1 AU for viewport clarity
    const EARTH_AXIAL_TILT_RAD = 23.43928 * (Math.PI / 180.0); // 23.44 deg obliquity

    // 1. Central Glowing Sun Mesh (Heliocentric Origin 0, 0, 0)
    const sunGroup = new THREE.Group();
    const sunGeo = new THREE.SphereGeometry(75.0, 32, 32);
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
    const sunMesh = new THREE.Mesh(sunGeo, sunMat);
    sunGroup.add(sunMesh);

    // Sun Corona Glow
    const coronaGeo = new THREE.SphereGeometry(95.0, 32, 32);
    const coronaMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.35 });
    sunGroup.add(new THREE.Mesh(coronaGeo, coronaMat));

    // Heliocentric Point Light from Sun
    const helioSunLight = new THREE.PointLight(0xfffbeb, 3.2, 8000, 0.4);
    sunGroup.add(helioSunLight);
    sunGroup.position.set(0, 0, 0);
    sunGroup.visible = false; // Toggled in Heliocentric Mode
    scene.add(sunGroup);

    // 2. Earth Orbital Ellipse Path (Keplerian e = 0.0167)
    const orbitPoints = [];
    const orbitSegments = 256;
    for (let i = 0; i <= orbitSegments; i++) {
      const th = (i / orbitSegments) * Math.PI * 2;
      const r = HELIO_ORBIT_RADIUS * (1.0 - 0.0167 * Math.cos(th));
      orbitPoints.push(new THREE.Vector3(r * Math.cos(th), 0, r * Math.sin(th)));
    }
    const orbitPathGeo = new THREE.BufferGeometry().setFromPoints(orbitPoints);
    const orbitPathMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.45 });
    const earthOrbitLine = new THREE.Line(orbitPathGeo, orbitPathMat);
    earthOrbitLine.visible = false;
    scene.add(earthOrbitLine);

    // Parent group to handle Earth heliocentric orbital position and axial tilt
    let helioAnomaly = 0.0;"""

if target_starfield in html_text:
    html_text = html_text.replace(target_starfield, sun_and_orbit_code, 1)
    print("Added Sun and Earth Orbit Path to index.html")

# Update setCam in index.html to handle mode === 'helio'
target_setcam = "function setCam(mode) {\n      cameraMode = mode;\n      const worldPos = new THREE.Vector3();"
replacement_setcam = """function setCam(mode) {
      cameraMode = mode;
      const worldPos = new THREE.Vector3();

      if (mode === 'helio') {
        sunGroup.visible = true;
        earthOrbitLine.visible = true;
        controls.target.copy(earthGroup.position);
        camera.position.set(earthGroup.position.x + 350, 450, earthGroup.position.z + 850);
        return;
      } else {
        sunGroup.visible = false;
        earthOrbitLine.visible = false;
        if (cameraMode !== 'helio') {
          earthGroup.position.set(0, 0, 0);
        }
      }"""

if target_setcam in html_text:
    html_text = html_text.replace(target_setcam, replacement_setcam, 1)
    print("Added mode === 'helio' handling in setCam")

# Update animate loop to advance Earth along its heliocentric orbit when in helio mode or advancing time
target_animate_rot = "      // Continuous Earth rotation at sidereal rate\n      earthGroup.rotation.y += (OMEGA * dt * (timeScale / 100.0));"
replacement_animate_rot = """      // Continuous Earth rotation at sidereal rate
      earthGroup.rotation.y += (OMEGA * dt * (timeScale / 100.0));

      // Heliocentric Orbital Revolution around the Sun (365.256 Days Period)
      const SEC_PER_SIDEREAL_YEAR = 31558149.76;
      helioAnomaly += ((dt * timeScale) / SEC_PER_SIDEREAL_YEAR) * (Math.PI * 2);
      if (cameraMode === 'helio') {
        const rHelio = HELIO_ORBIT_RADIUS * (1.0 - 0.0167 * Math.cos(helioAnomaly));
        earthGroup.position.set(rHelio * Math.cos(helioAnomaly), 0, rHelio * Math.sin(helioAnomaly));
        earthGroup.rotation.z = EARTH_AXIAL_TILT_RAD; // 23.44 deg axial obliquity
        controls.target.lerp(earthGroup.position, 0.05);
      } else {
        earthGroup.position.set(0, 0, 0);
        earthGroup.rotation.z = 0;
      }"""

if target_animate_rot in html_text:
    html_text = html_text.replace(target_animate_rot, replacement_animate_rot, 1)
    print("Added Heliocentric Earth orbital revolution to animate loop")

with open(src_html, "w", encoding="utf-8") as f:
    f.write(html_text)
print("Saved index.html")

# Synchronize E:\Downloads\index.html
if os.path.exists(os.path.dirname(dst_html)):
    shutil.copyfile(src_html, dst_html)
    print("Synchronized to E:\\Downloads\\index.html")
