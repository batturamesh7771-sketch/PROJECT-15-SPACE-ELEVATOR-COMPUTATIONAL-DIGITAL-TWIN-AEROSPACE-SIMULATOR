import os

src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"

with open(src_js, "r", encoding="utf-8") as f:
    content = f.read()

# Let's inspect updateTelemetry function start and replace it with full backend coupling
target_func_start = "  function updateTelemetry(data) {"
target_func_end = "    // Redraw Canvases"

replacement_func = """  function updateTelemetry(data) {
    if (!data) return;

    if (data.altitudeKm !== undefined) state.climbAltitudeKm = data.altitudeKm;
    if (data.nominalSpeedKmh !== undefined) state.nominalSpeedKmh = data.nominalSpeedKmh;
    if (data.climbDirection !== undefined) state.climbDirection = data.climbDirection;
    if (data.simElapsedSec !== undefined) state.simElapsedSec = data.simElapsedSec;
    if (data.latitude !== undefined) state.latitude = data.latitude;
    if (data.longitude !== undefined) state.longitude = data.longitude;

    const altKm = state.climbAltitudeKm;
    const speedKmh = state.climbDirection * state.nominalSpeedKmh;
    const vMs = (speedKmh * 1000.0) / 3600.0;
    const latDeg = state.latitude;
    const lonDeg = state.longitude;

    // =========================================================================
    // 1. REAL-TIME COUPLING TO BACKEND PHYSICS ENGINE (120+ CHANNELS)
    // =========================================================================
    let phys = null;
    if (window.SpaceElevatorPhysics && typeof window.SpaceElevatorPhysics.computeState === 'function') {
      try {
        phys = window.SpaceElevatorPhysics.computeState(altKm, speedKmh, latDeg, lonDeg, 20000.0);
      } catch (err) {
        console.warn('SpaceElevatorPhysics.computeState error:', err);
      }
    }

    // =========================================================================
    // 2. REAL-TIME COUPLING TO BACKEND MATERIALS & ENVIRONMENT ENGINE
    // =========================================================================
    let env = null;
    let health = null;
    if (window.MaterialsEnvironment) {
      if (typeof window.MaterialsEnvironment.getEnvironmentAtAltitude === 'function') {
        try {
          env = window.MaterialsEnvironment.getEnvironmentAtAltitude(altKm);
        } catch (err) {
          console.warn('MaterialsEnvironment.getEnvironmentAtAltitude error:', err);
        }
      }
      if (typeof window.MaterialsEnvironment.evaluateTetherHealth === 'function') {
        try {
          health = window.MaterialsEnvironment.evaluateTetherHealth({
            altitudeKm: altKm,
            selectedMaterial: state.selectedMaterial || 'cnt',
            simElapsedSec: state.simElapsedSec
          });
        } catch (err) {}
      }
    }

    // =========================================================================
    // 3. REAL-TIME COUPLING TO BACKEND ORBITAL MECHANICS ENGINE
    // =========================================================================
    let orb = null;
    let marsTransfer = null;
    if (window.OrbitalMissions) {
      if (typeof window.OrbitalMissions.calculateReleaseState === 'function') {
        try {
          orb = window.OrbitalMissions.calculateReleaseState(altKm);
        } catch (err) {
          console.warn('OrbitalMissions.calculateReleaseState error:', err);
        }
      }
      if (typeof window.OrbitalMissions.calculateHeliocentricTransfer === 'function') {
        try {
          marsTransfer = window.OrbitalMissions.calculateHeliocentricTransfer('mars', altKm);
        } catch (err) {}
      }
    }

    // Fallbacks if standalone/disconnected
    const r = R_E + (altKm * 1000.0);
    const g = phys ? phys.gravity.inward_gravity_ms2 : (MU / Math.pow(r, 2));
    const ac = phys ? phys.gravity.centrifugal_accel_ms2 : (Math.pow(OMEGA, 2) * r * Math.cos(latDeg * Math.PI / 180.0));
    const geff = phys ? phys.gravity.effective_g_ms2 : (g - ac);
    const coriolisF = phys ? phys.coriolis.coriolis_force_n : Math.abs(2.0 * 20000.0 * OMEGA * vMs * Math.cos(latDeg * Math.PI / 180.0));
    const c3 = orb ? orb.c3_km2s2 : (phys ? phys.orbital.c3_excess_energy_km2s2 : ((Math.pow(OMEGA * r, 2) - (2.0 * MU / r)) / 1e6));
    const tensionMN = phys ? (phys.tether.cable_tension_n / 1e6) : (10.0 + 82.0 * Math.exp(-Math.pow((altKm/100000.0)-0.35786, 2) / 0.12));
    const actualStressGPa = phys ? phys.tether.peak_stress_gpa : 38.1;
    const sf = phys ? phys.tether.safety_factor.toFixed(2) : (95.0 / actualStressGPa).toFixed(2);
    const powerMW = phys ? phys.power.electrical_power_mw : Math.max(0.12, (20000.0 * Math.max(0, geff) * Math.abs(vMs)) / 0.875 / 1e6);
    const energyGWh = phys ? phys.power.cumulative_energy_gwh : (9.84 + (state.simElapsedSec / 3600.0) * (powerMW / 1000.0));

    // Update Telemetry Card DOM
    const tAlt = document.getElementById('se-t-alt');
    if (tAlt) tAlt.innerText = `${altKm.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} km`;

    const tSpd = document.getElementById('se-t-spd');
    if (tSpd) tSpd.innerText = `${Math.abs(speedKmh).toFixed(2)} km/h`;

    const days = Math.floor(state.simElapsedSec / 86400);
    const hours = Math.floor((state.simElapsedSec % 86400) / 3600);
    const mins = Math.floor((state.simElapsedSec % 3600) / 60);
    const secs = Math.floor(state.simElapsedSec % 60);
    const metStr = `${days}d ${String(hours).padStart(2,'0')}h ${String(mins).padStart(2,'0')}m ${String(secs).padStart(2,'0')}s`;

    const tMet = document.getElementById('se-t-met');
    if (tMet) tMet.innerText = metStr;
    const metDisplay = document.getElementById('se-met-display');
    if (metDisplay) metDisplay.innerText = metStr;

    const tC3 = document.getElementById('se-t-c3');
    if (tC3) tC3.innerText = `${c3.toFixed(2)} km²/s²`;

    const tGrav = document.getElementById('se-t-grav');
    if (tGrav) tGrav.innerText = `${g.toFixed(4)} m/s²`;

    const tCent = document.getElementById('se-t-cent');
    if (tCent) tCent.innerText = `${ac.toFixed(4)} m/s²`;

    const tGeff = document.getElementById('se-t-geff');
    if (tGeff) tGeff.innerText = `${geff.toFixed(4)} m/s²`;

    const tCoriolis = document.getElementById('se-t-coriolis');
    if (tCoriolis) tCoriolis.innerText = `${coriolisF.toFixed(2)} N`;

    const tTens = document.getElementById('se-t-tens');
    if (tTens) tTens.innerText = `${tensionMN.toFixed(2)} MN`;

    const tStress = document.getElementById('se-t-stress');
    if (tStress) tStress.innerText = `${actualStressGPa.toFixed(1)} GPa`;

    const tSf = document.getElementById('se-t-sf');
    if (tSf) tSf.innerText = sf;

    const tPower = document.getElementById('se-t-power');
    if (tPower) tPower.innerText = `${Math.max(0.12, powerMW).toFixed(2)} MW`;

    const tEnergy = document.getElementById('se-t-energy');
    if (tEnergy) tEnergy.innerText = `${energyGWh.toFixed(2)} GWh`;

    // Deck Card 2: Tether Health Monitor
    const dSf = document.getElementById('se-deck-sf');
    if (dSf) dSf.innerText = sf;

    const dStress = document.getElementById('se-deck-stress');
    if (dStress) dStress.innerText = `${actualStressGPa.toFixed(1)} GPa`;

    const dHealthPct = document.getElementById('se-health-pct');
    if (dHealthPct && health) {
      dHealthPct.innerText = `${health.healthPct.toFixed(1)}%`;
    }

    const dMass = document.getElementById('se-deck-mass');
    if (dMass) {
      const massVal = (phys && phys.tether.total_tether_mass_kg) ? (phys.tether.total_tether_mass_kg / 1e9).toFixed(2) : (health && health.totalMassMt ? health.totalMassMt.toFixed(2) : '5.21');
      dMass.innerText = `${massVal} Mt`;
    }

    const dTaper = document.getElementById('se-deck-taper');
    if (dTaper) {
      const taperVal = (phys && phys.tether.pearson_taper_ratio) ? phys.tether.pearson_taper_ratio.toFixed(1) : (health && health.taperRatio ? health.taperRatio.toFixed(1) : '12.7');
      dTaper.innerText = `${taperVal}`;
    }

    // Deck Card 3: Live Orbital & Mission Analysis
    const dOrbEscape = document.getElementById('se-orb-escape-val');
    if (dOrbEscape) {
      if (orb && orb.isEscaped) {
        dOrbEscape.innerText = '0.00 km/s (Escaped)';
        dOrbEscape.style.color = '#10b981';
      } else if (orb && orb.deltaVToEscape_kms !== undefined) {
        dOrbEscape.innerText = `${orb.deltaVToEscape_kms.toFixed(2)} km/s`;
        dOrbEscape.style.color = '#38bdf8';
      }
    }

    const dOrbMars = document.getElementById('se-orb-mars-val');
    if (dOrbMars) {
      if (marsTransfer && marsTransfer.injectionDeltaVKms !== undefined) {
        dOrbMars.innerText = `${marsTransfer.injectionDeltaVKms.toFixed(2)} km/s`;
      } else if (altKm >= 100000.0) {
        dOrbMars.innerText = '0.00 km/s (Slingshot Ready)';
      }
    }

    const dOrbC3 = document.getElementById('se-orb-c3-val');
    if (dOrbC3) {
      dOrbC3.innerText = `${c3.toFixed(2)} km²/s²`;
      dOrbC3.style.color = c3 >= 0 ? '#10b981' : '#f59e0b';
    }

    // Deck Card 4: Live Space Environment & Risk
    const dEnvSolar = document.getElementById('se-env-solar-val');
    if (dEnvSolar && env) {
      dEnvSolar.innerText = `${Math.round(env.solarFlux_Wm2)} W/m²`;
    }

    const dEnvDebris = document.getElementById('se-env-debris-val');
    if (dEnvDebris && env) {
      dEnvDebris.innerText = `${env.debrisFlux_per_m2_yr.toExponential(1)} /m²/yr`;
    }

    const dEnvTemp = document.getElementById('se-env-temp-val');
    if (dEnvTemp && env) {
      const tVal = Math.round(env.equilibriumTemp_C);
      dEnvTemp.innerText = `${tVal >= 0 ? '+' : ''}${tVal} °C`;
    }

    const dEnvRad = document.getElementById('se-env-rad-val');
    if (dEnvRad && env) {
      const doseVal = env.radiationDose_mSv_h !== undefined ? env.radiationDose_mSv_h : (env.radiationDose_mSv_yr / 8760.0);
      dEnvRad.innerText = `${doseVal.toFixed(3)} mSv/h`;
    }

    const dRiskBadge = document.getElementById('se-risk-badge');
    if (dRiskBadge && env) {
      if (env.riskLevel === 'Critical') {
        dRiskBadge.innerText = '● CRITICAL HAZARD: Debris / Belts';
        dRiskBadge.style.color = '#ef4444';
        dRiskBadge.style.borderColor = '#ef4444';
        dRiskBadge.style.background = 'rgba(239, 68, 68, 0.2)';
      } else if (env.riskLevel === 'Severe') {
        dRiskBadge.innerText = '● HIGH HAZARD: Proton Belt';
        dRiskBadge.style.color = '#f59e0b';
        dRiskBadge.style.borderColor = '#f59e0b';
        dRiskBadge.style.background = 'rgba(245, 158, 11, 0.2)';
      } else {
        dRiskBadge.innerText = `● ${env.riskLevel || 'Nominal'} Risk`;
        dRiskBadge.style.color = '#10b981';
        dRiskBadge.style.borderColor = '#10b981';
        dRiskBadge.style.background = 'rgba(16, 185, 129, 0.15)';
      }
    }

    // Redraw Canvases"""

start_pos = content.find(target_func_start)
end_pos = content.find(target_func_end)

if start_pos != -1 and end_pos != -1:
    content = content[:start_pos] + replacement_func + content[end_pos + len("    // Redraw Canvases"):]
    print("Replaced updateTelemetry with full real-time backend coupling!")
else:
    print("Error: Could not locate updateTelemetry boundaries")

with open(src_js, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved dashboard_ui.js")
