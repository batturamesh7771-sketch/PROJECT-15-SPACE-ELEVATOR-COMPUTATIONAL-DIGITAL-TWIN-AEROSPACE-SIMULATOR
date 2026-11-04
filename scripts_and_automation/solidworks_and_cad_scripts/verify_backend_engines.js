const fs = require('fs');

// Load modules in Node
const physCode = fs.readFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\WebGL_Simulator\\js\\physics_engine.js', 'utf8');
const matCode = fs.readFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\WebGL_Simulator\\js\\materials_environment.js', 'utf8');
const orbCode = fs.readFileSync('C:\\Users\\user\\Desktop\\Space_Elevator_CAD_Phase1\\WebGL_Simulator\\js\\orbital_missions.js', 'utf8');

const window = {};
eval(physCode);
eval(matCode);
eval(orbCode);

console.log('Modules loaded successfully:');
console.log('SpaceElevatorPhysics available:', typeof window.SpaceElevatorPhysics);
console.log('MaterialsEnvironment available:', typeof window.MaterialsEnvironment);
console.log('OrbitalMissions available:', typeof window.OrbitalMissions);

console.log('\n--- Altitude 0 km (Ground Anchor) ---');
const p0 = window.SpaceElevatorPhysics.computeState(0, 450, 0, 0, 20000);
const e0 = window.MaterialsEnvironment.getEnvironmentAtAltitude(0);
const o0 = window.OrbitalMissions.calculateReleaseState(0);
console.log('Gravity:', p0.gravity.inward_gravity_ms2, 'Centrifugal:', p0.gravity.centrifugal_accel_ms2, 'Effective G:', p0.gravity.effective_g_ms2);
console.log('Coriolis Force:', p0.coriolis.coriolis_force_n, 'N');
console.log('Environment:', e0.riskLevel, 'Debris:', e0.debrisFlux_per_m2_yr, 'Temp:', e0.equilibriumTemp_C);
console.log('Orbital C3:', o0.c3_km2s2, 'DeltaV to Escape:', o0.deltaVToEscape_kms);

console.log('\n--- Altitude 35,786 km (GEO) ---');
const pGeo = window.SpaceElevatorPhysics.computeState(35786, 450, 0, 0, 20000);
const eGeo = window.MaterialsEnvironment.getEnvironmentAtAltitude(35786);
const oGeo = window.OrbitalMissions.calculateReleaseState(35786);
console.log('Gravity:', pGeo.gravity.inward_gravity_ms2, 'Centrifugal:', pGeo.gravity.centrifugal_accel_ms2, 'Effective G:', pGeo.gravity.effective_g_ms2);
console.log('Peak Stress:', pGeo.tether.peak_stress_gpa, 'GPa | Tension:', (pGeo.tether.cable_tension_n/1e6).toFixed(2), 'MN | Safety Factor:', pGeo.tether.safety_factor);
console.log('Environment:', eGeo.riskLevel, 'Radiation:', eGeo.radiationDose_mSv_h, 'mSv/h | Temp:', eGeo.equilibriumTemp_C);
console.log('Orbital C3:', oGeo.c3_km2s2, 'DeltaV to Escape:', oGeo.deltaVToEscape_kms);

console.log('\n--- Altitude 100,000 km (Apex Counterweight) ---');
const pApex = window.SpaceElevatorPhysics.computeState(100000, 450, 0, 0, 20000);
const eApex = window.MaterialsEnvironment.getEnvironmentAtAltitude(100000);
const oApex = window.OrbitalMissions.calculateReleaseState(100000);
console.log('Centrifugal Dominance Effective G:', pApex.gravity.effective_g_ms2, 'm/s2 (Upward outward acceleration)');
console.log('Apex Release Velocity:', pApex.kinematics.tangential_speed_kms, 'km/s | Escape Status:', oApex.isEscaped);
console.log('Hyperbolic Excess Energy C3:', oApex.c3_km2s2, 'km2/s2');
