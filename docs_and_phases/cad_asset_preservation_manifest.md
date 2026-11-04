# Space Elevator CAD Asset Preservation Manifest & Scene Hierarchy Registry
## Absolute Rule: Existing CAD Assets are Permanent Project Assets

**Document ID:** `docs/cad_asset_preservation_manifest.md`  
**Date:** 2 November 2026  
**Status:** Certified & Locked  
**Governing Directive:** Master Development Directive V2.0  

---

### 1. Master CAD Inventory & Provenance

| Component Assignment | Asset File Name / Source Path | Size (Bytes) | Meshes | Materials | Node Root Structure | Transformation & Scale Policy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Terrestrial Skyscraper Base** | `international_space_elevator.glb`<br>`media_1793469056660_d2145f0b.glb` | 1,448,136 | 1 | 1 | `Sketchfab_model` &rarr; `ISEV.fbx` &rarr; `RootNode` &rarr; `ISEV` | Ground anchor at $Y=0$, scaled to crown the architectural skyscraper foundation. |
| **2. Mobile Cargo Climber Capsule** | `dm_space_day_1_-_space_elevator_(1).glb`<br>`media_1793530091601_5342d98b.glb` | 307,572 | 34 | 6 | `Sketchfab_model` &rarr; `pCylinder2` &rarr; `polySurface1` | Triple-ring guide chassis, travels along tether between $0\text{ km}$ and $100,000\text{ km}$. |
| **3. Apex Orbital Station / Counterweight** | `day1_space_elevator.glb` | 34,184,616 | 21 | 5 | `Sketchfab_model` &rarr; `root` &rarr; `GLTF_SceneRootNode` &rarr; `Section_0` | Apex counterweight tip mounted at $Y = 350.0$ ($100,000\text{ km}$). |
| **4. Carbon Nanotube Tether Ribbon** | Procedural CatmullRom / Variable Taper Ribbon | Dynamic | 1 | 1 | Catmull-Rom Spline Curve connecting ground collar to apex docking port | 100-segment continuous ribbon deformed dynamically by Coriolis libration. |

---

### 2. Three.js Scene Node Hierarchy Map

```
Scene (Root)
 ├── AmbientLight (0xffffff, intensity: 0.6)
 ├── DirectionalLight (Sun Light, 0xffffff, intensity: 1.8)
 ├── EarthGroup
 │    ├── EarthMesh (R = 100.0, NASA Blue Marble Satellite Texture + Bump Map)
 │    └── AtmosphereMesh (R = 101.8, Inverted back-side glow)
 └── ElevatorAssembly (Pinned to Earth surface normal vector N)
      ├── BaseAnchorGroup (Y = 0)
      │    ├── SkyscraperFoundation (Tiered hexagonal bedrock plinth + 4 buttresses)
      │    ├── MagneticTensionCollar (Summit anchor ring)
      │    └── CAD_BaseMesh (international_space_elevator.glb, crowned atop spire)
      ├── TetherMesh (CatmullRom continuous ribbon 0 to 350 units)
      ├── ClimberNode (Translates along tether based on integrated altitude h(t))
      │    ├── ClimberBeaconLight (Cyan point light)
      │    └── CAD_ClimberMesh (dm_space_day_1_-_space_elevator_(1).glb, triple rings)
      └── UpperStationGroup (Y = 350.0 / 100,000 km apex)
           ├── CAD_ApexStationMesh (day1_space_elevator.glb)
           └── InterplanetaryEjectionVector (Hyperbolic trajectory marker)
```

---

### 3. Preservation & Quality Protection Rules
1. **Zero Replacement:** No CAD file will be deleted, swapped, or substituted with generic primitives or procedural boxes.
2. **Deterministic Scaling:** All model bounding boxes are centered on their true mechanical pivots.
3. **Traceable State:** All 100 telemetry channels, live graphs, and UI modules read from the exact kinematic and physical states of these Three.js nodes.
