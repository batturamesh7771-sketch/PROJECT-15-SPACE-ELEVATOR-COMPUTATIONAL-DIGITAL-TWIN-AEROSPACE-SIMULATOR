/**
 * Automated Verification & Validation Test Suite for SpaceElevatorPhysics
 * Run with: node Scripts/test_physics_engine.js
 */

const path = require('path');
const SpaceElevatorPhysics = require('../WebGL_Simulator/js/physics_engine.js');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function assert(condition, testName, details = '') {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`  [PASS] ${testName} ${details ? '(' + details + ')' : ''}`);
  } else {
    failedTests++;
    console.error(`  [FAIL] ${testName} ${details ? '(' + details + ')' : ''}`);
  }
}

function assertClose(actual, expected, tolerance, testName) {
  const diff = Math.abs(actual - expected);
  const relDiff = expected !== 0 ? diff / Math.abs(expected) : diff;
  const pass = relDiff <= tolerance || diff <= tolerance;
  assert(pass, testName, `expected: ${expected}, actual: ${actual}, diff: ${diff.toExponential(4)}`);
}

console.log('========================================================================');
console.log('SPACE ELEVATOR PHYSICS ENGINE: NUMERICAL BENCHMARK SUITE');
console.log('========================================================================\n');

// -----------------------------------------------------------------------------
// Test 1: Fundamental Constants
// -----------------------------------------------------------------------------
console.log('Test Suite 1: Fundamental Planetary & Material Constants');
const C = SpaceElevatorPhysics.CONSTANTS;
assertClose(C.MU, 3.986004418e14, 1e-12, 'Gravitational Parameter (MU)');
assertClose(C.R_E, 6378137.0, 1e-12, 'Earth Equatorial Radius (R_e)');
assertClose(C.OMEGA, 7.2921159e-5, 1e-12, 'Sidereal Earth Rotation (OMEGA)');
assertClose(C.RHO_MAT, 1300.0, 1e-12, 'Tether Material Density (rho_mat)');
assertClose(C.SIGMA_WORK, 50.0e9, 1e-12, 'Tether Design Working Stress (sigma_work = 50 GPa)');
assertClose(C.SIGMA_ULT, 100.0e9, 1e-12, 'Tether Ultimate Tensile Strength (sigma_ult = 100 GPa)');
assertClose(C.DESIGN_SF, 2.0, 1e-12, 'Design Safety Factor (SF = 2.0)');
assertClose(C.L_C / 1000.0, 3925.4, 0.001, 'Characteristic Length L_c = 3925.4 km');

// -----------------------------------------------------------------------------
// Test 2: Geostationary Orbit & Equilibrium
// -----------------------------------------------------------------------------
console.log('\nTest Suite 2: Orbital Mechanics & Acceleration suite');
assertClose(C.R_GEO, 42164169.46, 0.0001, 'GEO Radius r_geo = 42,164,169.46 m');
assertClose(C.H_GEO / 1000.0, 35786.03, 0.0001, 'GEO Altitude h_geo = 35,786.03 km');

const g_geo = SpaceElevatorPhysics.gravity(C.R_GEO);
const ac_geo = SpaceElevatorPhysics.centrifugal(C.R_GEO);
assertClose(g_geo, 0.224208, 0.001, 'Inward gravity at GEO = 0.2242 m/s^2');
assertClose(ac_geo, 0.224208, 0.001, 'Outward centrifugal at GEO = 0.2242 m/s^2');

const geff_geo = SpaceElevatorPhysics.effectiveGravity(C.R_GEO);
assert(geff_geo === 0.0, 'Effective net gravity at GEO is EXACTLY 0.0000 m/s^2', `g_eff = ${geff_geo}`);

// -----------------------------------------------------------------------------
// Test 3: Apex Counterweight (100,000 km altitude) & C3 Energy
// -----------------------------------------------------------------------------
console.log('\nTest Suite 3: Apex Counterweight (100,000 km) & Hyperbolic Excess C3');
const r_100k = C.R_E + 100000000.0;
const g_100k = SpaceElevatorPhysics.gravity(r_100k);
const ac_100k = SpaceElevatorPhysics.centrifugal(r_100k);
const geff_100k = SpaceElevatorPhysics.effectiveGravity(r_100k);
const vtan_100k = SpaceElevatorPhysics.tangentialSpeed(r_100k);
const vesc_100k = SpaceElevatorPhysics.escapeVelocity(r_100k);
const c3_100k = SpaceElevatorPhysics.hyperbolicExcessEnergy(r_100k);

assertClose(g_100k, 0.035224, 0.0001, 'Inward gravity at 100,000 km = 0.035224 m/s^2');
assertClose(ac_100k, 0.565665, 0.0001, 'Centrifugal accel at 100,000 km = 0.565665 m/s^2');
assertClose(Math.abs(geff_100k), 0.530442, 0.0001, 'Net outward acceleration at 100,000 km = 0.530442 m/s^2');
assertClose(vtan_100k / 1000.0, 7.757217, 0.0001, 'Tangential speed at 100,000 km = 7.757217 km/s');
assertClose(vesc_100k / 1000.0, 2.737522, 0.0001, 'Escape velocity at 100,000 km = 2.737522 km/s');
assertClose(c3_100k, 52.68, 0.001, 'C3 Hyperbolic Excess Energy at 100,000 km = +52.68 km^2/s^2');

// -----------------------------------------------------------------------------
// Test 4: US Standard Atmosphere 1976 & Aerodynamics
// -----------------------------------------------------------------------------
console.log('\nTest Suite 4: US Standard Atmosphere 1976 & Aerodynamic Drag');
const atmo_sea = SpaceElevatorPhysics.atmosphere(0);
assertClose(atmo_sea.temperature, 288.15, 1e-6, 'Sea Level Temperature T = 288.15 K');
assertClose(atmo_sea.pressure, 101325.0, 1e-6, 'Sea Level Pressure P = 101,325 Pa');
assertClose(atmo_sea.density, 1.2250, 0.001, 'Sea Level Density rho = 1.225 kg/m^3');

const atmo_11k = SpaceElevatorPhysics.atmosphere(11000);
assertClose(atmo_11k.temperature, 216.65, 1e-6, 'Tropopause (11 km) T = 216.65 K');
assertClose(atmo_11k.pressure, 22632.0, 0.001, 'Tropopause (11 km) P = 22,632 Pa');

const atmo_25k = SpaceElevatorPhysics.atmosphere(25000);
assertClose(atmo_25k.temperature, 216.65, 1e-6, 'Lower Stratosphere (25 km) T = 216.65 K');
assert(atmo_25k.pressure < 2500.0 && atmo_25k.pressure > 2400.0, 'Lower Stratosphere (25 km) P ~ 2488 Pa', `P = ${atmo_25k.pressure.toFixed(1)} Pa`);

const atmo_space = SpaceElevatorPhysics.atmosphere(120000);
assert(atmo_space.density === 0.0 && atmo_space.pressure === 0.0, 'Deep space vacuum above 100 km (rho = 0, P = 0)');

const q_sea = SpaceElevatorPhysics.dynamicPressure(0, 125.0);
const drag_sea = SpaceElevatorPhysics.dragForce(0, 125.0, 0.42, 12.5);
assertClose(q_sea, 9570.3, 0.01, 'Sea Level Dynamic Pressure at 125 m/s = 9570.3 Pa');
assertClose(drag_sea / 1000.0, 50.244, 0.01, 'Sea Level Aerodynamic Drag at 125 m/s = 50.24 kN');

// -----------------------------------------------------------------------------
// Test 5: Pearson-Aravind Taper & Dynamic Stress
// -----------------------------------------------------------------------------
console.log('\nTest Suite 5: Pearson-Aravind Exponential Taper & Stress');
const taper_ground = SpaceElevatorPhysics.taperRatio(C.R_E);
assertClose(taper_ground, 1.0000, 1e-6, 'Ground Taper Ratio A(R_e)/A_base = 1.0000');

const taper_geo = SpaceElevatorPhysics.taperRatio(C.R_GEO);
assertClose(taper_geo, 3.5219, 0.001, 'GEO Peak Taper Ratio A(r_geo)/A_base = 3.5219');

const taper_apex = SpaceElevatorPhysics.taperRatio(r_100k);
assertClose(taper_apex, 2.1127, 0.001, '100,000 km Taper Ratio A(apex)/A_base = 2.1127');

const stress_ground = SpaceElevatorPhysics.dynamicStress(C.R_E, 20000.0, 0.0, 125.0);
assert(stress_ground.safetyFactor > 1.8 && stress_ground.safetyFactor <= 2.0, 'Structural Safety Factor in valid nominal design window', `SF = ${stress_ground.safetyFactor.toFixed(3)}`);

// -----------------------------------------------------------------------------
// Test 6: Coriolis Dynamics
// -----------------------------------------------------------------------------
console.log('\nTest Suite 6: Coriolis Dynamics & Deflection');
const coriolis_sea = SpaceElevatorPhysics.coriolisDynamics(C.R_E, 20000.0, 125.0);
assertClose(coriolis_sea.force, 364.61, 0.01, 'Coriolis Force for 20t climber at 125 m/s = 364.61 N');
assert(coriolis_sea.direction.includes('Westward'), 'Coriolis Direction is Westward for ascent');

const coriolis_desc = SpaceElevatorPhysics.coriolisDynamics(C.R_E, 20000.0, -125.0);
assert(coriolis_desc.direction.includes('Eastward'), 'Coriolis Direction is Eastward for descent');

// -----------------------------------------------------------------------------
// Test 7: Laser Power Beaming & Propulsion
// -----------------------------------------------------------------------------
console.log('\nTest Suite 7: Power Beaming & Climber Mechanics');
const power_sea = SpaceElevatorPhysics.climberPower(0, 125.0, 0.0, 20000.0);
assertClose(power_sea.thrustForceKN, 245.53, 0.01, 'Sea-level Thrust Force = 245.53 kN');
assertClose(power_sea.mechanicalPowerMW, 30.69, 0.01, 'Sea-level Mechanical Power = 30.69 MW');
assert(power_sea.laserBeamPowerMW > 70.0 && power_sea.laserBeamPowerMW < 76.0, 'Laser Beam Power at ground station in 70-76 MW range', `P_laser = ${power_sea.laserBeamPowerMW.toFixed(2)} MW`);

const power_geo = SpaceElevatorPhysics.climberPower(C.H_GEO, 125.0, 0.0, 20000.0);
assertClose(power_geo.thrustForceKN, 0.0, 0.001, 'At GEO, required thrust force drops to 0.00 kN');

const power_above_geo = SpaceElevatorPhysics.climberPower(50000000.0, 125.0, 0.0, 20000.0);
assert(power_above_geo.regenPowerKW > 0.0, 'Above GEO cruising generates regenerative braking power', `P_regen = ${power_above_geo.regenPowerKW.toFixed(1)} kW`);

// -----------------------------------------------------------------------------
// Test 8: Non-Equatorial Arbitrary Latitude Shear
// -----------------------------------------------------------------------------
console.log('\nTest Suite 8: Non-Equatorial Arbitrary Latitude Shear');
const shear_eq = SpaceElevatorPhysics.nonEquatorialShear(0.0, 0.0);
assert(shear_eq.psiDeg === 0.0 && shear_eq.shearForceN === 0.0, 'Equatorial baseline (lat = 0 deg) has EXACTLY 0.0 deg incline and 0.0 N shear');

const shear_10deg = SpaceElevatorPhysics.nonEquatorialShear(10.01, 0.0);
assertClose(shear_10deg.psiDeg, 0.0341, 0.001, 'Latitude 10.01 deg off-axis incline angle psi = 0.0341 deg');
assertClose(shear_10deg.shearForceKN, 2.97, 0.02, 'Latitude 10.01 deg surface lateral shear force = 2.97 kN');
assert(shear_10deg.warningFlag === true, 'Latitude 10.01 deg raises shear warning flag');

// -----------------------------------------------------------------------------
// Test 9: 4th-Order Runge-Kutta (RK4) Kinematics Integrator
// -----------------------------------------------------------------------------
console.log('\nTest Suite 9: 4th-Order Runge-Kutta (RK4) Kinematics Integrator');
const rk4_step1 = SpaceElevatorPhysics.integrateKinematics(0.0, 0.0, 125.0, 1.0, 20000.0, { maxAccel: 0.5 });
assertClose(rk4_step1.acceleration, 0.5, 0.01, 'RK4 acceleration at start = 0.5 m/s^2');
assertClose(rk4_step1.velocity, 0.5, 0.01, 'RK4 velocity after 1 second = 0.5 m/s');
assert(rk4_step1.altitude > 0.0, 'RK4 altitude advances positively');

// Integrate for 300 steps (300 seconds) to reach target speed
let simAlt = 0.0;
let simVel = 0.0;
const dt = 1.0;
for (let s = 0; s < 300; s++) {
  const step = SpaceElevatorPhysics.integrateKinematics(simAlt, simVel, 125.0, dt, 20000.0, { maxAccel: 0.5 });
  simAlt = step.altitude;
  simVel = step.velocity;
}
assertClose(simVel, 125.0, 0.001, 'RK4 smoothly reaches and maintains 125.0 m/s cruising speed');
assert(simAlt > 0.0, `Kinematic integration advanced altitude to ${(simAlt / 1000).toFixed(1)} km`);

// -----------------------------------------------------------------------------
// Test 10: Complete computeState Telemetry Channels (100+ channels)
// -----------------------------------------------------------------------------
console.log('\nTest Suite 10: computeState 100+ Telemetry Channels');
const state = SpaceElevatorPhysics.computeState(1000000.0, 125.0, 0.0, 20000.0);
const channelCount = Object.keys(state.channels).length;
console.log(`  Discovered Telemetry Channels: ${channelCount}`);
assert(channelCount >= 100, `Telemetry channels count >= 100 (Actual: ${channelCount})`);

// Verify categories exist
const expectedCategories = ['position', 'gravity', 'kinematics', 'orbital', 'atmosphere', 'aerodynamics', 'tether', 'stress', 'coriolis', 'power', 'non_equatorial', 'mission'];
expectedCategories.forEach(cat => {
  assert(state[cat] !== undefined, `Category '${cat}' is populated`);
});

// Verify direct accessor state.get('c3_energy_km2_s2')
const stateAt100k = SpaceElevatorPhysics.computeState(100000000.0, 125.0, 0.0, 20000.0);
assertClose(stateAt100k.get('c3_energy_km2_s2'), 52.68, 0.001, 'state.get("c3_energy_km2_s2") matches +52.68 km^2/s^2 at 100,000 km');
assertClose(stateAt100k.get('v_tan_kms'), 7.7572, 0.001, 'state.get("v_tan_kms") matches 7.757 km/s at 100,000 km');

// Verify GEO state
const stateAtGeo = SpaceElevatorPhysics.computeState(C.H_GEO, 125.0, 0.0, 20000.0);
assert(stateAtGeo.get('g_eff_mps2') === 0.0, 'state.get("g_eff_mps2") at GEO is EXACTLY 0.0000 m/s^2');

console.log('\n========================================================================');
console.log(`BENCHMARK SUMMARY: ${passedTests} / ${totalTests} TESTS PASSED (${failedTests} FAILED)`);
console.log('========================================================================\n');

if (failedTests > 0) {
  process.exit(1);
} else {
  console.log('STATUS: ALL BENCHMARKS AND EQUATIONS RIGOROUSLY VALIDATED.');
  process.exit(0);
}
