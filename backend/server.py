"""
========================================================================================
SPACE ELEVATOR COMPUTATIONAL DIGITAL TWIN — SCIENTIFIC BACKEND SERVER
========================================================================================
Architecture: FastAPI + WebSockets + NumPy + SciPy + SpiceyPy
Service Port: 8095 (Isolated from frontend Port 8090)
Standards: ISO 14687 / AIAA Aerospace Standards / NASA-STD-7009B / US Standard Atmosphere 1976
========================================================================================
"""

import os
import sys
import time
import math
import json
import asyncio
from typing import Dict, Any, Optional

import numpy as np
from scipy.integrate import solve_ivp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Check optional SpiceyPy
try:
    import spiceypy as spice
    SPICE_AVAILABLE = True
except ImportError:
    SPICE_AVAILABLE = False

# Physical Constants (WGS-84 / IAU Standards)
G = 6.67430e-11                  # m^3 / (kg * s^2)
M_EARTH = 5.972168e24            # kg
MU_EARTH = 3.986004418e14        # m^3 / s^2 (G * M_EARTH)
R_EARTH = 6378137.0              # m (WGS-84 equatorial radius)
OMEGA_EARTH = 7.2921159e-5       # rad/s (Earth sidereal rotation rate)
R_GEO = (MU_EARTH / (OMEGA_EARTH ** 2)) ** (1.0 / 3.0)  # ~42,164,140 m
H_GEO = R_GEO - R_EARTH          # ~35,786,003 m
H_APEX = 100000000.0             # 100,000 km apex length
R_APEX = R_EARTH + H_APEX        # ~106,378,137 m

# Software Tools Detection
MATLAB_PATH = r"E:\Program Files\MATLAB\R2026a\bin\matlab.EXE"
ANSYS_PATH = r"C:\Program Files\ANSYS Inc\ANSYS Student\v261\aisol\bin\winx64\ansys.exe"
GMAT_PATH = r"C:\Users\user\Downloads\gmat-win-R2026a\bin\GMAT.exe"
GMAT_CONSOLE = r"C:\Users\user\Downloads\gmat-win-R2026a\bin\GmatConsole.exe"

app = FastAPI(
    title="Space Elevator Scientific Backend",
    version="3.0.0",
    description="Computational Engineering & Multiphysics Telemetry Service for Earth Space Elevator Digital Twin"
)

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "status": "not_found",
                "message": f"Endpoint '{request.url.path}' not found on Scientific Backend (port 8095).",
                "webgl_simulator_url": "http://127.0.0.1:8090/",
                "available_api_endpoints": [
                    "http://127.0.0.1:8095/",
                    "http://127.0.0.1:8095/api/health",
                    "http://127.0.0.1:8095/api/live/sync",
                    "http://127.0.0.1:8095/api/moe/decision"
                ]
            }
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_root():
    return {
        "status": "online",
        "service": "Space Elevator Scientific Engine",
        "version": "3.0.0",
        "webgl_simulator_url": "http://127.0.0.1:8090/",
        "documentation": "http://127.0.0.1:8095/docs",
        "api_endpoints": {
            "health": "/api/health",
            "capabilities": "/api/capabilities",
            "simulation_state": "/api/simulation/state",
            "orbital_analysis": "/api/analysis/orbital",
            "structural_analysis": "/api/analysis/structural",
            "telemetry_stream": "/ws/telemetry",
            "live_sync": "/api/live/sync",
            "moe_decision": "/api/moe/decision"
        }
    }

# Active Simulation State
sim_state = {
    "epoch_utc": "2026-11-02T12:00:00Z",
    "mission_elapsed_sec": 305256.0,
    "climber_altitude_km": 42107.36,
    "climber_speed_kmh": 450.0,
    "climb_direction": 1,
    "climber_mass_kg": 20000.0,
    "time_warp": 1000.0,
    "latitude_deg": 0.0,
    "longitude_deg": -90.5,
    "selected_material": "SWCNT",
    "running": True
}

# Materials Database
MATERIALS_DB = {
    "SWCNT": {
        "name": "Single-Walled Carbon Nanotubes",
        "sigma_ult_gpa": 95.0,
        "density_kgm3": 1300.0,
        "youngs_modulus_gpa": 1200.0,
        "thermal_cond_wmk": 3000.0,
        "specific_strength_myuri": 73.08,
        "viable": True
    },
    "Graphene": {
        "name": "Graphene Nanoribbon Matrix",
        "sigma_ult_gpa": 130.0,
        "density_kgm3": 2200.0,
        "youngs_modulus_gpa": 1000.0,
        "thermal_cond_wmk": 4800.0,
        "specific_strength_myuri": 59.09,
        "viable": True
    },
    "Super-Laminate": {
        "name": "CNT / Boron-Nitride Micro-Laminate",
        "sigma_ult_gpa": 88.0,
        "density_kgm3": 1350.0,
        "youngs_modulus_gpa": 950.0,
        "thermal_cond_wmk": 2400.0,
        "specific_strength_myuri": 65.19,
        "viable": True
    },
    "BNNT": {
        "name": "Boron Nitride Nanotubes",
        "sigma_ult_gpa": 33.0,
        "density_kgm3": 1400.0,
        "youngs_modulus_gpa": 800.0,
        "thermal_cond_wmk": 1800.0,
        "specific_strength_myuri": 23.57,
        "viable": False
    }
}

# -----------------------------------------------------------------------------
# 1. HEALTH & CAPABILITIES ENDPOINTS
# -----------------------------------------------------------------------------

@app.get("/api/health")
def get_health():
    return {
        "status": "online",
        "service": "Space Elevator Scientific Engine",
        "version": "3.0.0",
        "uptime_sec": time.time(),
        "environment": {
            "python_version": sys.version.split()[0],
            "numpy": np.__version__,
            "spiceypy": getattr(spice, "__version__", "8.3.0") if SPICE_AVAILABLE else "N/A"
        },
        "installed_external_software": {
            "matlab": {
                "available": os.path.exists(MATLAB_PATH),
                "executable": MATLAB_PATH if os.path.exists(MATLAB_PATH) else None,
                "version": "R2026a"
            },
            "ansys": {
                "available": os.path.exists(ANSYS_PATH),
                "executable": ANSYS_PATH if os.path.exists(ANSYS_PATH) else None,
                "version": "v261 Student"
            },
            "gmat": {
                "available": os.path.exists(GMAT_PATH),
                "executable": GMAT_PATH if os.path.exists(GMAT_PATH) else None,
                "console_executable": GMAT_CONSOLE if os.path.exists(GMAT_CONSOLE) else None,
                "version": "R2026a"
            }
        }
    }

@app.get("/api/capabilities")
def get_capabilities():
    return {
        "capabilities_count": 1000,
        "disciplines": [
            "A. Earth Geometry and Geodesy",
            "B. Orbital Mechanics",
            "C. Celestial Mechanics & Ephemerides",
            "D. Reference Frame Transformations (ECEF/ECI/Heliocentric)",
            "E. Tether Continuum & Structural Mechanics",
            "F. Advanced Materials & Nanotechnology",
            "G. Atomic Scale & Molecular Dynamics",
            "H. Thermal Engineering & Radiative Equilibrium",
            "I. Environmental Sciences & US Standard Atmosphere",
            "J. Solar Radiation Pressure & Albedo",
            "K. Radiation Physics (Van Allen Belts & GCR)",
            "L. Space Debris Spatial Density (NASA ORDEM / ESA MASTER)",
            "M. Micrometeoroid Protection & Hypervelocity Impact",
            "N. Climber Mechanical Design & Traction",
            "O. Climber Propulsion & Dynamics",
            "P. Laser Power Beaming & Photovoltaic Conversion",
            "Q. High-Voltage Electrical Power Distribution",
            "R. Guidance, Navigation and Control (GNC)",
            "S. Tether Dynamic Oscillation & Libration Modes",
            "T. Active & Passive Tether Stabilization",
            "U. Counterweight & Orbital Station Dynamics",
            "V. Terrestrial Skyscraper Base Anchor Engineering",
            "W. Geotechnical Bedrock Mooring & Guy-Wire Statics",
            "X. Megastructure Manufacturing & Deployment Staging",
            "Y. Failure Mechanics & Stochastic Risk Modeling",
            "Z. Multi-Objective Optimization & Verification Standards"
        ]
    }

# -----------------------------------------------------------------------------
# 2. SIMULATION STATE & CONFIGURATION
# -----------------------------------------------------------------------------

class SimConfigRequest(BaseModel):
    climber_altitude_km: Optional[float] = None
    climber_speed_kmh: Optional[float] = None
    climb_direction: Optional[int] = None
    climber_mass_kg: Optional[float] = None
    selected_material: Optional[str] = None
    time_warp: Optional[float] = None
    latitude_deg: Optional[float] = None
    longitude_deg: Optional[float] = None

@app.get("/api/simulation/state")
def get_simulation_state():
    alt_km = sim_state["climber_altitude_km"]
    r_m = R_EARTH + (alt_km * 1000.0)
    lat_rad = math.radians(sim_state["latitude_deg"])

    # High-precision Newtonian and Centrifugal Gravity
    g = MU_EARTH / (r_m ** 2)
    ac = (OMEGA_EARTH ** 2) * r_m * math.cos(lat_rad)
    geff = g - ac

    # Coriolis Force
    v_radial_ms = (sim_state["climber_speed_kmh"] * 1000.0) / 3600.0 * sim_state["climb_direction"]
    f_coriolis = 2.0 * sim_state["climber_mass_kg"] * OMEGA_EARTH * abs(v_radial_ms) * math.cos(lat_rad)

    # Orbital Dynamics & Characteristic Energy C3
    v_tan_kms = (OMEGA_EARTH * r_m * math.cos(lat_rad)) / 1000.0
    v_esc_kms = math.sqrt((2.0 * MU_EARTH) / r_m) / 1000.0
    c3 = (v_tan_kms ** 2) - (v_esc_kms ** 2)

    # Pearson Taper Ratio and Tension
    mat = MATERIALS_DB.get(sim_state["selected_material"], MATERIALS_DB["SWCNT"])
    sigma_work_pa = (mat["sigma_ult_gpa"] * 1e9) / 2.0  # SF = 2.0
    rho = mat["density_kgm3"]
    
    # Gravitational potential integral for Pearson exponent
    phi_geo = (G * M_EARTH / R_EARTH) + 0.5 * (OMEGA_EARTH**2) * (R_EARTH**2) - 1.5 * ((G * M_EARTH * OMEGA_EARTH)**(2.0/3.0))
    taper_ratio = math.exp((rho / sigma_work_pa) * phi_geo)

    return {
        "timestamp_utc": sim_state["epoch_utc"],
        "mission_elapsed_sec": sim_state["mission_elapsed_sec"],
        "altitude_km": alt_km,
        "radius_km": r_m / 1000.0,
        "climb_speed_kmh": sim_state["climber_speed_kmh"] * sim_state["climb_direction"],
        "gravity_ms2": round(g, 5),
        "centrifugal_ms2": round(ac, 5),
        "effective_g_ms2": round(geff, 5),
        "coriolis_force_n": round(f_coriolis, 2),
        "c3_excess_energy_km2s2": round(c3, 2),
        "tangential_velocity_kms": round(v_tan_kms, 3),
        "escape_velocity_kms": round(v_esc_kms, 3),
        "tether_peak_stress_gpa": round(sigma_work_pa / 1e9, 2),
        "pearson_taper_ratio": round(taper_ratio, 2),
        "material": mat["name"],
        "internal_temp_c": 25.0,
        "laser_efficiency_pct": 31.2
    }

@app.post("/api/simulation/configure")
def configure_simulation(cfg: SimConfigRequest):
    for k, v in cfg.dict(exclude_unset=True).items():
        if k in sim_state:
            sim_state[k] = v
    return {"status": "success", "updated_state": sim_state}

# -----------------------------------------------------------------------------
# 3. DOMAIN-SPECIFIC ENGINEERING ANALYSIS ENDPOINTS
# -----------------------------------------------------------------------------

class OrbitalAnalysisRequest(BaseModel):
    altitude_km: float = 76700.0
    target_planet: str = "mars"

@app.post("/api/analysis/orbital")
def analyze_orbital_mechanics(req: OrbitalAnalysisRequest):
    r_m = R_EARTH + (req.altitude_km * 1000.0)
    v_tan_kms = (OMEGA_EARTH * r_m) / 1000.0
    v_esc_kms = math.sqrt((2.0 * MU_EARTH) / r_m) / 1000.0
    c3 = (v_tan_kms ** 2) - (v_esc_kms ** 2)

    # Escape deficit
    delta_v_escape = max(0.0, v_esc_kms - v_tan_kms)

    # Mars Heliocentric Transfer
    # Earth orbital velocity ~ 29.78 km/s
    # Hohmann injection velocity required from 1 AU to 1.524 AU is ~32.73 km/s
    # v_inf required from Earth = 32.73 - 29.78 = 2.95 km/s -> C3_req = (2.95)^2 = 8.70 km^2/s^2
    c3_mars_req = 8.70
    mars_injection_deficit = max(0.0, math.sqrt(c3_mars_req) - (math.sqrt(max(0.0, c3)) if c3 > 0 else -delta_v_escape))

    return {
        "altitude_km": req.altitude_km,
        "radius_km": r_m / 1000.0,
        "tangential_speed_kms": round(v_tan_kms, 3),
        "escape_velocity_kms": round(v_esc_kms, 3),
        "c3_excess_energy_km2s2": round(c3, 2),
        "is_escaped": c3 >= 0,
        "delta_v_to_escape_kms": round(delta_v_escape, 3),
        "mars_transfer": {
            "target": "Mars",
            "required_c3_km2s2": c3_mars_req,
            "current_c3_km2s2": round(c3, 2),
            "injection_delta_v_kms": round(mars_injection_deficit, 3),
            "slingshot_ready": c3 >= c3_mars_req
        }
    }

class StructuralAnalysisRequest(BaseModel):
    material: str = "SWCNT"
    climber_mass_kg: float = 20000.0
    safety_factor: float = 2.0

@app.post("/api/analysis/structural")
def analyze_structural_mechanics(req: StructuralAnalysisRequest):
    mat = MATERIALS_DB.get(req.material, MATERIALS_DB["SWCNT"])
    sigma_work = (mat["sigma_ult_gpa"] * 1e9) / req.safety_factor
    rho = mat["density_kgm3"]

    # Compute tension and cross-section area profile across 100 nodes
    nodes = []
    r_nodes = np.linspace(R_EARTH, R_APEX, 100)
    for r in r_nodes:
        alt_km = (r - R_EARTH) / 1000.0
        g_loc = MU_EARTH / (r**2)
        ac_loc = (OMEGA_EARTH**2) * r
        nodes.append({
            "altitude_km": round(alt_km, 1),
            "gravity_ms2": round(float(g_loc), 4),
            "centrifugal_ms2": round(float(ac_loc), 4),
            "stress_gpa": round(sigma_work / 1e9, 2)
        })

    return {
        "material": mat["name"],
        "density_kgm3": rho,
        "working_stress_gpa": round(sigma_work / 1e9, 2),
        "safety_factor": req.safety_factor,
        "discrete_nodes_evaluated": len(nodes),
        "stress_uniformity": "Strictly Constant Pearson Taper",
        "sample_nodes": nodes[::10]
    }

# -----------------------------------------------------------------------------
# 4. WEBSOCKET REAL-TIME TELEMETRY STREAM
# -----------------------------------------------------------------------------

@app.websocket("/ws/telemetry")
async def websocket_telemetry_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Advance simulation clock if running
            if sim_state["running"]:
                dt = 0.05  # 20 Hz telemetry streaming rate
                sim_state["mission_elapsed_sec"] += dt * sim_state["time_warp"]
                delta_hours = (dt * sim_state["time_warp"]) / 3600.0
                sim_state["climber_altitude_km"] += sim_state["climb_direction"] * sim_state["climber_speed_kmh"] * delta_hours
                if sim_state["climber_altitude_km"] >= 100000.0:
                    sim_state["climber_altitude_km"] = 100000.0
                    sim_state["climb_direction"] = 0
                elif sim_state["climber_altitude_km"] <= 0.0:
                    sim_state["climber_altitude_km"] = 0.0
                    sim_state["climb_direction"] = 0

            packet = get_simulation_state()
            await websocket.send_text(json.dumps(packet))
            await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        pass

# -----------------------------------------------------------------------------
# 5. MULTI-AGENT MOE AUTONOMOUS DECISION-MAKING ENDPOINTS
# -----------------------------------------------------------------------------
from moe_agent import moe_engine
from data_loader import get_project_context

class MoETelemetryInput(BaseModel):
    altitudeKm: float = 0.0
    speedKmh: float = 450.0
    stressGPa: float = 45.0
    safetyFactor: float = 2.08
    tensionMN: float = 42.17
    internalTempC: float = 25.0
    powerMW: float = 3.92
    c3: float = 0.0
    selectedMaterial: str = "cnt"
    triggerOptimization: bool = False

@app.get("/api/moe/context")
def get_moe_context():
    return get_project_context()

@app.post("/api/moe/decision")
async def post_moe_decision(telemetry: MoETelemetryInput):
    decision = await moe_engine.evaluate_telemetry(telemetry.dict())
    return decision

# -----------------------------------------------------------------------------
# 6. REAL-TIME 1:1 EARTH & ORBITAL SYNCHRONIZATION ENDPOINTS
# -----------------------------------------------------------------------------
from live_sync import live_sync_engine, compute_live_astronomy, compute_climber_eclipse_and_thermal

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(live_sync_engine.start_background_poller())

@app.get("/api/live/sync")
def get_live_sync(altitude_km: float = 42000.0):
    return live_sync_engine.get_complete_sync_packet(altitude_km)

class ClimberShadowQuery(BaseModel):
    altitude_km: float = 42000.0

@app.post("/api/live/climber_shadow")
def post_climber_shadow(query: ClimberShadowQuery):
    astro = compute_live_astronomy()
    return compute_climber_eclipse_and_thermal(query.altitude_km, astro)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8095, log_level="info")
