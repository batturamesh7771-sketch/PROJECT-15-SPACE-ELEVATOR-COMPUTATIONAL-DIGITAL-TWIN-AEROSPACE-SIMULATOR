# EARTH REVOLUTION & CELESTIAL MOTION DESIGN
## SPACE ELEVATOR COMPUTATIONAL DIGITAL TWIN
**Document Identifier:** SIM-SE-2026-REV-001  
**Implementation Target:** Dual-Mode Astrodynamical Engine in WebGL (Port 8090)  

---

### 1. DUAL-MODE VISUALIZATION ENGINE SPECIFICATION

To fulfill both local engineering diagnostics and macroscopic interplanetary mission analysis, the simulator implements two distinct camera and reference frame modes:

#### Mode 1: Earth-Centered Geostationary Co-Rotating View (Default)
- **Primary Purpose:** Engineering inspection of climber transit, tether stress distributions, ground anchor skyscraper docking, and apex station operations.
- **Camera Anchor:** Centered on Earth or tracking the climber vehicle.
- **Reference Frame:** Co-rotating ECEF frame.
- **Visual Features:** High-resolution Earth sphere, atmospheric Rayleigh/Mie scattering shader, 100,000 km segmented tether line with dynamic tension-color gradient, realistic cloud layers, and illuminated ground base skyscraper.

#### Mode 2: Heliocentric Solar System Revolution View (Interplanetary Mode)
- **Primary Purpose:** Visualizing Earth complete orbital revolution around the Sun, Keplerian orbital eccentricity ($e = 0.0167$), axial obliquity (tilt $\epsilon = 23.44^\circ$), and planetary escape departure hyperbolas.
- **Parent Node:** `heliocentricGroup` placed at the scene root.
- **Solar Body:** `sunMesh` with dynamic solar flare corona shaders, placed at $(0, 0, 0)$ heliocentric coordinates.
- **Earth Orbital Path:** Elliptical Keplerian spline with semi-major axis $a = 150.0\text{ units}$, semi-minor axis $b = a \sqrt{1 - e^2}$, oriented in the ecliptic plane.
- **Earth Pivot & Tilt Hierarchy:**
  - `earthPivotGroup` revolves around the Sun at orbital rate $n = 2\pi / 365.256\text{ days}$.
  - `earthAxialGroup` child node rotated by $23.44^\circ$ relative to the ecliptic normal vector.
  - `earthMesh` rotates about its tilted axis at sidereal rate $\Omega = 7.2921159 \times 10^{-5}\text{ rad/s}$.
  - The Space Elevator megastructure remains rigidly connected to the rotating Earth mesh, correctly sweeping through interplanetary space.

---

### 2. SCENE GRAPH CODE ARCHITECTURE

Implemented in `WebGL_Simulator/index.html`:
```javascript
// Mode 2: Heliocentric Solar System Architecture
const heliocentricGroup = new THREE.Group();
scene.add(heliocentricGroup);

// Sun Mesh with radiant glow
const sunGeo = new THREE.SphereGeometry(25, 32, 32);
const sunMat = new THREE.MeshBasicMaterial({ color: 0xffdd44, wireframe: false });
const sunMesh = new THREE.Mesh(sunGeo, sunMat);
heliocentricGroup.add(sunMesh);

// Earth Pivot & Tilt
const earthPivot = new THREE.Group();
heliocentricGroup.add(earthPivot);

const earthAxialGroup = new THREE.Group();
earthAxialGroup.rotation.z = THREE.MathUtils.degToRad(23.44); // 23.44 deg axial obliquity
earthPivot.add(earthAxialGroup);

// Space elevator hierarchy attaches directly to the rotating Earth within earthAxialGroup
earthAxialGroup.add(earthMesh);
earthAxialGroup.add(tetherGroup);
earthAxialGroup.add(skyscraperAnchor);
```
- **Seamless Toggling:** The "Heliocentric Orbit View" mode button toggles camera target, field of view, and clipping planes ($0.1$ to $10,000$ scene units) without tearing down WebGL buffers or losing climber telemetry synchronization.
