/**
 * =========================================================================================
 * SPACE ELEVATOR COMPUTATIONAL DIGITAL TWIN: MATHEMATICAL PHYSICS ENGINE
 * =========================================================================================
 * 
 * High-Precision Orbital Mechanics, Aerodynamics, Pearson-Aravind Taper Dynamics,
 * Coriolis Deflections, Laser Power Beaming, and Non-Equatorial Shear Mechanics.
 * 
 * Document Reference: docs/phase1_physics_verification.md
 * Standards: US Standard Atmosphere 1976, IAU/IUGG Planetary Geodetic Constants (SI Units)
 * 
 * Exported namespace: window.SpaceElevatorPhysics (Browser) & module.exports (Node.js)
 * =========================================================================================
 */

(function (root, factory) {
  'use strict';
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.SpaceElevatorPhysics = factory();
  }
})(typeof self !== 'undefined' ? self : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
  'use strict';

  // =======================================================================================
  // 1. FUNDAMENTAL PHYSICAL & PLANETARY CONSTANTS (SI Units)
  // =======================================================================================
  const CONSTANTS = {
    // Standard Gravitational Parameter of Earth (m^3/s^2) [IAU/WGS84]
    MU: 3.986004418e14,

    // Earth Mean Equatorial Radius (m) [WGS84]
    R_E: 6378137.0,

    // Earth Sidereal Angular Rotation Rate (rad/s) [IERS Standard: 86,164.0905 s period]
    OMEGA: 7.2921159e-5,

    // Geostationary Orbital Radius: r_geo = (mu / omega^2)^(1/3) = 42,164,169.46 m
    R_GEO: Math.cbrt(3.986004418e14 / (7.2921159e-5 * 7.2921159e-5)), // 42,164,169.46186 m

    // Geostationary Altitude above Equatorial Surface: h_geo = r_geo - R_e = 35,786,032.46 m
    H_GEO: Math.cbrt(3.986004418e14 / (7.2921159e-5 * 7.2921159e-5)) - 6378137.0, // 35,786.032 km

    // Nominal Standard Surface Gravity (m/s^2) [ISO 80000-3]
    G_STANDARD: 9.80665,

    // Nominal Equatorial Surface Inward Gravity: g0 = mu / R_e^2 = 9.798285 m/s^2
    G0: 9.798285479,

    // Nominal Surface Gravity constant used for characteristic length definition (m/s^2)
    G0_CHAR: 9.798,

    // Apex Counterweight Baseline Altitude (m) [100,000 km]
    APEX_ALTITUDE: 100000000.0,

    // Tether Material Specifications: Carbon Nanotube (CNT) Macro-Yarn
    MATERIAL_NAME: 'Carbon Nanotube (CNT) Macro-Yarn',
    RHO_MAT: 1300.0,            // Volumetric mass density (kg/m^3)
    SIGMA_WORK: 50.0e9,         // Operational design working stress: 50.0 GPa (Pa)
    SIGMA_ULT: 100.0e9,         // Ultimate tensile failure stress: 100.0 GPa (Pa)
    DESIGN_SF: 2.0,             // Required structural design safety factor

    // Characteristic Length: L_c = sigma_work / (rho_mat * g0) = 3,925,413.35 m = 3925.4 km
    L_C: 50.0e9 / (1300.0 * 9.798),

    // Baseline Reference Tether Cross-Sectional Area at Earth surface (m^2) [1.0 cm^2 = 100 mm^2]
    TETHER_BASE_AREA: 1.0e-4,

    // Climber Physical Baseline Defaults
    DEFAULT_CLIMBER_MASS: 20000.0,      // Total climber mass: 20 metric tons (kg)
    DEFAULT_PAYLOAD_MASS: 14000.0,      // Payload mass: 14 metric tons (kg)
    DEFAULT_CLIMB_SPEED: 125.0,         // Nominal vertical cruising speed: 125 m/s = 450 km/h
    DEFAULT_MAX_ACCEL: 0.50,            // Passenger comfort acceleration limit (m/s^2)
    DEFAULT_CD: 0.42,                   // Climber aerodynamic drag coefficient (subsonic/transonic)
    DEFAULT_FRONTAL_AREA: 12.5,         // Climber frontal aerodynamic area (m^2)

    // Propulsion & Beamed Energy Efficiencies
    ETA_DRIVE: 0.94,                    // Climber mechanical motor & pinch-roller efficiency (94%)
    ETA_PV: 0.52,                       // Monochromatic tuned GaAs PV receiver efficiency (52%)
    ETA_ATM_SURFACE: 0.85,              // Clear-sky atmospheric laser transmission at sea level (85%)
    ATM_SCALE_HEIGHT: 8500.0,           // Optical atmospheric attenuation scale height (m)
    ETA_REGEN: 0.85,                    // Regenerative braking generator recovery efficiency (85%)

    // Specific Gas Constant for Dry Air (J / (kg * K))
    R_SPECIFIC_AIR: 287.05,
    GAMMA_AIR: 1.40                     // Ratio of specific heats for dry air
  };

  // =======================================================================================
  // 2. GRAVITATIONAL & CENTRIFUGAL ACCELERATION SUITE
  // =======================================================================================

  /**
   * Calculates inward Newtonian gravitational acceleration at radial distance r from Earth center.
   * @param {number} r Radial geocentric distance in meters (r >= R_e).
   * @returns {number} Inward gravity g(r) in m/s^2.
   */
  function gravity(r) {
    if (r <= 0) return 0;
    return CONSTANTS.MU / (r * r);
  }

  /**
   * Calculates outward centrifugal acceleration due to Earth sidereal rotation.
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} Outward centrifugal acceleration a_c(r) in m/s^2.
   */
  function centrifugal(r) {
    if (r <= 0) return 0;
    return CONSTANTS.OMEGA * CONSTANTS.OMEGA * r;
  }

  /**
   * Calculates effective net gravity in the co-rotating frame:
   * g_eff(r) = g(r) - a_c(r)
   * Positive value = net inward pull toward Earth.
   * Zero value = perfect equilibrium (EXACTLY 0.0000 m/s^2 at GEO).
   * Negative value = net outward centrifugal pull toward space.
   * 
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} Effective gravity g_eff(r) in m/s^2.
   */
  function effectiveGravity(r) {
    if (r <= 0) return 0;
    // High-precision zero snap at GEO equilibrium radius (within 0.1 meter tolerance)
    if (Math.abs(r - CONSTANTS.R_GEO) < 0.1) {
      return 0.0;
    }
    const g_in = gravity(r);
    const a_out = centrifugal(r);
    const diff = g_in - a_out;
    // Suppress IEEE-754 epsilon noise near zero
    if (Math.abs(diff) < 1.0e-14) {
      return 0.0;
    }
    return diff;
  }

  /**
   * Calculates co-rotational tangential speed at radial distance r.
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} Tangential velocity v_tan in m/s.
   */
  function tangentialSpeed(r) {
    if (r <= 0) return 0;
    return CONSTANTS.OMEGA * r;
  }

  /**
   * Calculates parabolic escape velocity at radial distance r.
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} Escape velocity v_esc in m/s.
   */
  function escapeVelocity(r) {
    if (r <= 0) return 0;
    return Math.sqrt(2.0 * CONSTANTS.MU / r);
  }

  /**
   * Calculates circular orbital speed at radial distance r.
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} Circular orbital speed v_circ in m/s.
   */
  function circularOrbitalVelocity(r) {
    if (r <= 0) return 0;
    return Math.sqrt(CONSTANTS.MU / r);
  }

  /**
   * Calculates hyperbolic excess energy C3 for release from the elevator at radial distance r.
   * C3(r) = v_tan(r)^2 - v_esc(r)^2 [km^2/s^2]
   * Negative value = bound elliptical or suborbital release.
   * Zero value = parabolic escape.
   * Positive value = hyperbolic escape trajectory (e.g. +52.68 km^2/s^2 at 100,000 km altitude).
   * 
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} C3 hyperbolic excess energy in km^2/s^2.
   */
  function hyperbolicExcessEnergy(r) {
    if (r <= 0) return 0;
    const v_tan = tangentialSpeed(r); // m/s
    const v_esc = escapeVelocity(r);  // m/s
    const c3_mps2 = (v_tan * v_tan) - (v_esc * v_esc); // m^2/s^2
    return c3_mps2 * 1.0e-6; // convert to km^2/s^2
  }

  // =======================================================================================
  // 3. US STANDARD ATMOSPHERE (1976) & AERODYNAMIC DRAG
  // =======================================================================================

  /**
   * Evaluates atmospheric properties (Temperature, Pressure, Density) based on US Standard Atmosphere 1976.
   * Continuous and validated from sea level (0 m) to outer vacuum (> 100 km).
   * 
   * @param {number} altitude Geometric altitude in meters above sea level.
   * @returns {Object} { temperature: K, pressure: Pa, density: kg/m^3, speedOfSound: m/s }
   */
  function atmosphere(altitude) {
    const h = Math.max(0.0, altitude);

    // Deep space vacuum above 100 km (Kármán line / outer atmosphere limit)
    if (h >= 100000.0) {
      return {
        temperature: 0.0,
        pressure: 0.0,
        density: 0.0,
        speedOfSound: 0.0
      };
    }

    let T = 288.15; // K
    let P = 101325.0; // Pa

    if (h <= 11000.0) {
      // Troposphere: linear temperature lapse rate (-6.5 K/km)
      T = 288.15 - 0.0065 * h;
      P = 101325.0 * Math.pow(T / 288.15, 5.25588);
    } else if (h <= 25000.0) {
      // Tropopause and Lower Stratosphere: isothermal at 216.65 K
      T = 216.65;
      P = 22632.0 * Math.exp(-0.0001577 * (h - 11000.0));
    } else if (h <= 47000.0) {
      // Stratosphere (Layer 2): positive lapse rate (+2.8 K/km)
      const P25 = 22632.0 * Math.exp(-0.0001577 * 14000.0); // P at 25 km
      T = 216.65 + 0.0028 * (h - 25000.0);
      P = P25 * Math.pow(T / 216.65, -12.20114);
    } else if (h <= 51000.0) {
      // Stratopause: isothermal at 278.25 K
      const P25 = 22632.0 * Math.exp(-0.0001577 * 14000.0);
      const T47 = 216.65 + 0.0028 * 22000.0;
      const P47 = P25 * Math.pow(T47 / 216.65, -12.20114);
      T = 278.25;
      P = P47 * Math.exp(-0.0001222 * (h - 47000.0));
    } else if (h <= 71000.0) {
      // Mesosphere (Layer 4): negative lapse rate (-2.8 K/km)
      const P25 = 22632.0 * Math.exp(-0.0001577 * 14000.0);
      const T47 = 216.65 + 0.0028 * 22000.0;
      const P47 = P25 * Math.pow(T47 / 216.65, -12.20114);
      const P51 = P47 * Math.exp(-0.0001222 * 4000.0);
      T = 278.25 - 0.0028 * (h - 51000.0);
      P = P51 * Math.pow(T / 278.25, 12.20114);
    } else {
      // Upper Mesosphere (71 km - 100 km): smoothly decays to exosphere vacuum
      const P25 = 22632.0 * Math.exp(-0.0001577 * 14000.0);
      const T47 = 216.65 + 0.0028 * 22000.0;
      const P47 = P25 * Math.pow(T47 / 216.65, -12.20114);
      const P51 = P47 * Math.exp(-0.0001222 * 4000.0);
      const T71 = 278.25 - 0.0028 * 20000.0;
      const P71 = P51 * Math.pow(T71 / 278.25, 12.20114);
      T = Math.max(180.0, T71 - 0.0020 * (h - 71000.0));
      P = P71 * Math.exp(-0.000147 * (h - 71000.0));
    }

    // Ideal gas law: rho = P / (R_specific * T)
    const rho = P / (CONSTANTS.R_SPECIFIC_AIR * T);
    const speedOfSound = Math.sqrt(CONSTANTS.GAMMA_AIR * CONSTANTS.R_SPECIFIC_AIR * T);

    return {
      temperature: T,
      pressure: P,
      density: rho,
      speedOfSound: speedOfSound
    };
  }

  /**
   * Calculates dynamic pressure q = 0.5 * rho * v^2.
   * @param {number} altitude Altitude in meters.
   * @param {number} velocity Velocity in m/s.
   * @returns {number} Dynamic pressure in Pascals (Pa).
   */
  function dynamicPressure(altitude, velocity) {
    const atmo = atmosphere(altitude);
    return 0.5 * atmo.density * velocity * velocity;
  }

  /**
   * Calculates aerodynamic drag force on climber body:
   * F_drag = q * C_d * A_frontal
   * @param {number} altitude Altitude in meters.
   * @param {number} velocity Velocity in m/s.
   * @param {number} [cd] Drag coefficient (default: 0.42).
   * @param {number} [frontalArea] Frontal area in m^2 (default: 12.5 m^2).
   * @returns {number} Aerodynamic drag force in Newtons (N).
   */
  function dragForce(altitude, velocity, cd = CONSTANTS.DEFAULT_CD, frontalArea = CONSTANTS.DEFAULT_FRONTAL_AREA) {
    const q = dynamicPressure(altitude, velocity);
    return q * cd * frontalArea;
  }

  // =======================================================================================
  // 4. CARBON NANOTUBE PEARSON-ARAVIND EXPONENTIAL TAPER & STRESS
  // =======================================================================================

  /**
   * Evaluates the Pearson-Aravind constant-stress area taper ratio:
   * A(r) / A_base = exp[ (rho_mat / sigma_work) * ( mu*(1/R_e - 1/r) - 0.5*omega^2*(r^2 - R_e^2) ) ]
   * 
   * Reaches maximum value of ~3.5219 at GEO (r_geo = 42,164.17 km) and smoothly tapers
   * to ~2.1127 at the 100,000 km counterweight apex.
   * 
   * @param {number} r Radial geocentric distance in meters.
   * @returns {number} Cross-sectional area taper ratio (dimensionless).
   */
  function taperRatio(r) {
    if (r <= CONSTANTS.R_E) return 1.0;
    const termGrav = CONSTANTS.MU * (1.0 / CONSTANTS.R_E - 1.0 / r);
    const termCent = 0.5 * CONSTANTS.OMEGA * CONSTANTS.OMEGA * (r * r - CONSTANTS.R_E * CONSTANTS.R_E);
    const exponent = (CONSTANTS.RHO_MAT / CONSTANTS.SIGMA_WORK) * (termGrav - termCent);
    return Math.exp(exponent);
  }

  /**
   * Computes the physical cross-sectional area of the tether ribbon at radial distance r.
   * @param {number} r Radial geocentric distance in meters.
   * @param {number} [baseArea] Base area at Earth surface in m^2 (default: 1.0e-4 m^2).
   * @returns {number} Cross-sectional area A(r) in m^2.
   */
  function taperArea(r, baseArea = CONSTANTS.TETHER_BASE_AREA) {
    return baseArea * taperRatio(r);
  }

  /**
   * Computes total dynamic axial tension, axial stress, and structural safety factor
   * at radial distance r accounting for tether static pre-tension and climber dynamic loads.
   * 
   * @param {number} r Radial geocentric distance in meters.
   * @param {number} [climberMass] Climber mass in kg (default: 20,000 kg).
   * @param {number} [climberAccel] Vertical acceleration in m/s^2 (default: 0.0).
   * @param {number} [vClimb] Climbing speed in m/s (default: 125.0 m/s).
   * @param {number} [baseArea] Base tether cross-section in m^2 (default: 1.0e-4 m^2).
   * @returns {Object} Structural stress metrics: { area, staticTension, climberLoad, totalTension, axialStress, safetyFactor }
   */
  function dynamicStress(
    r,
    climberMass = CONSTANTS.DEFAULT_CLIMBER_MASS,
    climberAccel = 0.0,
    vClimb = CONSTANTS.DEFAULT_CLIMB_SPEED,
    baseArea = CONSTANTS.TETHER_BASE_AREA
  ) {
    const area = taperArea(r, baseArea);
    // Baseline static tension carried by constant-stress ribbon: T_static = sigma_work * A(r)
    const staticTension = CONSTANTS.SIGMA_WORK * area;

    // Climber net reaction force transferred onto tether:
    // Below GEO, climber effective weight hangs downward (increasing tether tension above it).
    // Above GEO, centrifugal pull acts outward (relieving tension on lower sections, or adding tension to anchor).
    const alt = Math.max(0.0, r - CONSTANTS.R_E);
    const g_eff = effectiveGravity(r);
    const f_drag = dragForce(alt, vClimb);
    
    // Total dynamic vertical load of the climber:
    // F_load = M * g_eff + F_drag + M * a
    const climberLoad = climberMass * Math.max(0.0, g_eff) + f_drag + climberMass * Math.max(0.0, climberAccel);

    const totalTension = staticTension + climberLoad;
    const axialStress = totalTension / area; // Pascals (Pa)
    const safetyFactor = CONSTANTS.SIGMA_ULT / Math.max(1.0, axialStress);

    return {
      area: area,
      staticTension: staticTension,
      climberLoad: climberLoad,
      totalTension: totalTension,
      axialStress: axialStress,
      safetyFactor: safetyFactor
    };
  }

  // =======================================================================================
  // 5. CORIOLIS DYNAMICS & TRANSVERSE DEFLECTION
  // =======================================================================================

  /**
   * Calculates Coriolis force, acceleration, and dynamic lag angle for a moving climber.
   * Equation: F_coriolis = 2 * M_climber * omega * v_climb
   * Incline Lag: tan(theta_lag) = F_coriolis / (M_climber * g_eff)
   * 
   * When ascending (v > 0), Coriolis force points Westward (opposing Earth rotation).
   * When descending (v < 0), Coriolis force points Eastward (assisting rotation).
   * 
   * @param {number} r Radial geocentric distance in meters.
   * @param {number} [climberMass] Climber mass in kg.
   * @param {number} [vClimb] Climbing vertical velocity in m/s.
   * @returns {Object} Coriolis metrics: { accel, force, direction, lagAngleRad, lagAngleDeg, tetherDeflectionDeg }
   */
  function coriolisDynamics(r, climberMass = CONSTANTS.DEFAULT_CLIMBER_MASS, vClimb = CONSTANTS.DEFAULT_CLIMB_SPEED) {
    const a_coriolis = 2.0 * CONSTANTS.OMEGA * Math.abs(vClimb);
    const f_coriolis = 2.0 * climberMass * CONSTANTS.OMEGA * vClimb;

    let direction = 'Neutral (Stationary)';
    if (vClimb > 0.001) {
      direction = 'Westward (Lagging)';
    } else if (vClimb < -0.001) {
      direction = 'Eastward (Leading)';
    }

    const g_eff = effectiveGravity(r);
    const absGeff = Math.abs(g_eff);

    // Climber body lag angle relative to local vertical:
    // tan(theta_lag) = F_coriolis / (M * |g_eff|)
    // Regularized against zero at GEO microgravity
    const effectiveDenominator = climberMass * Math.max(0.001, absGeff);
    const lagAngleRad = Math.atan2(Math.abs(f_coriolis), effectiveDenominator);
    const lagAngleDeg = lagAngleRad * (180.0 / Math.PI);

    // Tether structural inclination angle: restoring force comes from tether axial tension T(r)
    const stress = dynamicStress(r, climberMass, 0.0, vClimb);
    const tetherDeflectionRad = Math.atan2(Math.abs(f_coriolis), Math.max(1.0, stress.totalTension));
    const tetherDeflectionDeg = tetherDeflectionRad * (180.0 / Math.PI);

    // Estimated lateral steady-state deflection distance along circular arc
    const lateralDisplacement = r * tetherDeflectionRad;

    return {
      accel: a_coriolis,
      force: f_coriolis,
      direction: direction,
      lagAngleRad: lagAngleRad,
      lagAngleDeg: lagAngleDeg,
      tetherDeflectionRad: tetherDeflectionRad,
      tetherDeflectionDeg: tetherDeflectionDeg,
      lateralDisplacement: lateralDisplacement
    };
  }

  // =======================================================================================
  // 6. POWER BEAMING & PROPULSION DRIVETRAIN
  // =======================================================================================

  /**
   * Computes climber propulsion thrust, mechanical power, and ground laser beaming requirements.
   * 
   * Governing Equations:
   * Thrust: F_thrust = M_climber * max(0, g_eff) + F_drag + M_climber * (dv/dt)
   * Mechanical Power: P_mech = F_thrust * v_climb
   * Laser Beamed Power: P_laser = P_mech / (eta_drive * eta_PV * eta_atm)
   * Regenerative braking when descending below GEO or decelerating.
   * 
   * @param {number} altitude Climber altitude above Earth surface in meters.
   * @param {number} [velocity] Vertical climb velocity in m/s.
   * @param {number} [accel] Kinematic acceleration in m/s^2.
   * @param {number} [climberMass] Total climber mass in kg.
   * @param {Object} [options] Drivetrain efficiency overrides.
   * @returns {Object} Complete power and propulsion telemetry.
   */
  function climberPower(
    altitude,
    velocity = CONSTANTS.DEFAULT_CLIMB_SPEED,
    accel = 0.0,
    climberMass = CONSTANTS.DEFAULT_CLIMBER_MASS,
    options = {}
  ) {
    const r = CONSTANTS.R_E + Math.max(0.0, altitude);
    const g_eff = effectiveGravity(r);
    const f_drag = dragForce(altitude, velocity, options.cd, options.frontalArea);

    // Efficiencies
    const eta_drive = options.etaDrive ?? CONSTANTS.ETA_DRIVE;
    const eta_pv = options.etaPV ?? CONSTANTS.ETA_PV;
    
    // Atmospheric optical transmission increases exponentially with altitude up to 100% in vacuum
    const eta_atm_surface = options.etaAtmSurface ?? CONSTANTS.ETA_ATM_SURFACE;
    const eta_atm = 1.0 - (1.0 - eta_atm_surface) * Math.exp(-altitude / CONSTANTS.ATM_SCALE_HEIGHT);
    const eta_system_total = eta_drive * eta_pv * eta_atm;

    let f_thrust = 0.0;
    let p_mech = 0.0;
    let p_laser = 0.0;
    let p_regen = 0.0;
    let climberStatus = 'Hovering / Docked';

    if (velocity > 0.001) {
      climberStatus = 'Ascending';
      // Upward ascent:
      // Below GEO (g_eff > 0): must overcome gravity + drag + inertial acceleration
      // Above GEO (g_eff < 0): centrifugal outward pull helps ascent!
      if (g_eff >= 0.0) {
        f_thrust = climberMass * g_eff + f_drag + climberMass * Math.max(0.0, accel);
        p_mech = f_thrust * velocity;
        p_laser = p_mech / Math.max(0.01, eta_system_total);
      } else {
        // Beyond GEO: net outward gravity is pulling the climber outward
        const netPull = -g_eff; // outward acceleration (m/s^2)
        const netOutwardForce = climberMass * netPull - f_drag;
        if (accel > netPull) {
          // Accelerating faster than natural centrifugal pull
          f_thrust = climberMass * (accel - netPull) + f_drag;
          p_mech = f_thrust * velocity;
          p_laser = p_mech / Math.max(0.01, eta_system_total);
        } else {
          // Centrifugal force drives climber; pinch-rollers apply regenerative braking to maintain cruise speed
          const f_brake = Math.max(0.0, climberMass * (netPull - accel) - f_drag);
          p_regen = f_brake * velocity * eta_drive * CONSTANTS.ETA_REGEN;
          f_thrust = 0.0;
          p_mech = 0.0;
          p_laser = 0.0;
        }
      }
    } else if (velocity < -0.001) {
      climberStatus = 'Descending';
      const absV = Math.abs(velocity);
      if (g_eff > 0.0) {
        // Below GEO descent: gravity pulls down, pinch rollers brake regeneratively
        const f_brake = Math.max(0.0, climberMass * g_eff - f_drag + climberMass * Math.max(0.0, -accel));
        p_regen = f_brake * absV * eta_drive * CONSTANTS.ETA_REGEN;
        f_thrust = 0.0;
        p_mech = 0.0;
        p_laser = 0.0;
      } else {
        // Above GEO descent: pulling inward against outward centrifugal force requires positive drive power!
        f_thrust = climberMass * Math.abs(g_eff) + f_drag + climberMass * Math.max(0.0, -accel);
        p_mech = f_thrust * absV;
        p_laser = p_mech / Math.max(0.01, eta_system_total);
      }
    } else {
      // Station-keeping / hovering
      if (g_eff > 0.0) {
        f_thrust = climberMass * g_eff;
        p_mech = 0.0;
        p_laser = 0.0;
      }
    }

    return {
      thrustForceN: f_thrust,
      thrustForceKN: f_thrust / 1000.0,
      mechanicalPowerW: p_mech,
      mechanicalPowerKW: p_mech / 1000.0,
      mechanicalPowerMW: p_mech / 1.0e6,
      laserBeamPowerW: p_laser,
      laserBeamPowerMW: p_laser / 1.0e6,
      regenPowerKW: p_regen / 1000.0,
      etaDrive: eta_drive,
      etaPV: eta_pv,
      etaAtm: eta_atm,
      etaSystemTotal: eta_system_total,
      climberStatus: climberStatus,
      dragForceN: f_drag,
      climberWeightN: climberMass * g_eff
    };
  }

  // =======================================================================================
  // 7. NON-EQUATORIAL ARBITRARY LATITUDE SHEAR DYNAMICS
  // =======================================================================================

  /**
   * Evaluates the non-equatorial lateral equilibrium incline angle and lateral shear forces.
   * Governing Equation:
   * tan(psi) = [omega^2 * r * sin(phi) * cos(phi)] / [g(r) - omega^2 * r * cos(phi)^2]
   * Lateral shear force: F_shear = T_base * sin(psi)
   * 
   * When anchor latitude phi = 0 (Equatorial Baseline): psi = 0.000 deg, F_shear = 0.0 N.
   * When anchor latitude phi != 0: creates strong equatorward tilt and dangerous lateral shear.
   * 
   * @param {number} latitudeDeg Geodetic latitude of anchor platform in degrees.
   * @param {number} [altitudeMeters] Altitude in meters (default: 0 = Earth surface).
   * @param {number} [baseArea] Tether base cross-section in m^2.
   * @returns {Object} Non-equatorial shear telemetry: { psiRad, psiDeg, shearForceN, shearForceKN, axialForceN, shearToTensionRatio, status }
   */
  function nonEquatorialShear(latitudeDeg, altitudeMeters = 0.0, baseArea = CONSTANTS.TETHER_BASE_AREA) {
    const phi = latitudeDeg * (Math.PI / 180.0);
    const r = CONSTANTS.R_E + Math.max(0.0, altitudeMeters);

    // If perfectly equatorial:
    if (Math.abs(latitudeDeg) < 1.0e-5) {
      const t_base = CONSTANTS.SIGMA_WORK * baseArea;
      return {
        latitudeDeg: 0.0,
        psiRad: 0.0,
        psiDeg: 0.0,
        shearForceN: 0.0,
        shearForceKN: 0.0,
        shearForceMN: 0.0,
        axialForceN: t_base,
        shearToTensionRatio: 0.0,
        warningFlag: false,
        status: 'Stable Equatorial Baseline (Zero Lateral Shear)'
      };
    }

    const sinPhi = Math.sin(phi);
    const cosPhi = Math.cos(phi);
    const g_r = gravity(r);
    const omega2_r = CONSTANTS.OMEGA * CONSTANTS.OMEGA * r;

    // Numerator: lateral equatorward centrifugal component
    const numerator = omega2_r * sinPhi * cosPhi;
    // Denominator: radial inward net acceleration
    const denominator = g_r - omega2_r * cosPhi * cosPhi;

    const tanPsi = numerator / Math.max(1.0e-6, denominator);
    const psiRad = Math.atan(tanPsi);
    const psiDeg = psiRad * (180.0 / Math.PI);

    const t_base = CONSTANTS.SIGMA_WORK * baseArea;
    const f_shear = t_base * Math.sin(psiRad);
    const f_axial = t_base * Math.cos(psiRad);

    let status = 'Warning: Non-Equatorial Tilt';
    if (Math.abs(psiDeg) > 5.0) {
      status = 'CRITICAL: Severe Off-Axis Lateral Shear Failure Mode';
    }

    return {
      latitudeDeg: latitudeDeg,
      psiRad: psiRad,
      psiDeg: psiDeg,
      shearForceN: f_shear,
      shearForceKN: f_shear / 1000.0,
      shearForceMN: f_shear / 1.0e6,
      axialForceN: f_axial,
      shearToTensionRatio: tanPsi,
      warningFlag: true,
      status: status
    };
  }

  // =======================================================================================
  // 8. ORBITAL RELEASE PARAMETERS & EQUATORIAL TRAJECTORY
  // =======================================================================================

  /**
   * Computes Keplerian orbital parameters for a payload released horizontally from the elevator.
   * @param {number} r Radial geocentric distance in meters.
   * @returns {Object} Keplerian orbit parameters.
   */
  function orbitalParameters(r) {
    const v_tan = tangentialSpeed(r);
    const v_circ = circularOrbitalVelocity(r);
    const v_esc = escapeVelocity(r);
    const c3 = hyperbolicExcessEnergy(r);

    // Specific orbital energy: epsilon = 0.5 * v^2 - mu / r
    const specificEnergy = 0.5 * v_tan * v_tan - CONSTANTS.MU / r; // J/kg

    // Semi-major axis: a = -mu / (2 * epsilon)
    let a_orbit = -CONSTANTS.MU / (2.0 * specificEnergy); // m

    // For horizontal equatorial tangential release:
    // Angular momentum: h_spec = r * v_tan
    const h_spec = r * v_tan;
    // Eccentricity: e = sqrt(1 + 2 * epsilon * h^2 / mu^2) = |r * v_tan^2 / mu - 1|
    const e = Math.abs((r * v_tan * v_tan) / CONSTANTS.MU - 1.0);

    let perigeeRadius = 0.0;
    let apogeeRadius = 0.0;
    let periodHours = 0.0;
    let orbitType = 'Suborbital';

    if (c3 > 0.0) {
      orbitType = 'Hyperbolic Interplanetary Escape';
      perigeeRadius = r;
      apogeeRadius = Infinity;
      periodHours = null;
    } else if (Math.abs(c3) < 0.01) {
      orbitType = 'Parabolic Escape';
      perigeeRadius = r;
      apogeeRadius = Infinity;
      periodHours = null;
    } else if (Math.abs(r - CONSTANTS.R_GEO) < 1000.0) {
      orbitType = 'Circular GEO Orbit';
      perigeeRadius = r;
      apogeeRadius = r;
      periodHours = (2.0 * Math.PI / CONSTANTS.OMEGA) / 3600.0; // 23.934 hours
    } else if (v_tan > v_circ) {
      orbitType = 'Elliptical Transfer Orbit (Perigee at Release)';
      perigeeRadius = r;
      apogeeRadius = a_orbit * (1.0 + e);
      periodHours = (2.0 * Math.PI * Math.sqrt(Math.pow(a_orbit, 3) / CONSTANTS.MU)) / 3600.0;
    } else {
      orbitType = 'Suborbital / Reentry Trajectory (Apogee at Release)';
      apogeeRadius = r;
      perigeeRadius = a_orbit * (1.0 - e);
      periodHours = (2.0 * Math.PI * Math.sqrt(Math.pow(Math.max(1.0, a_orbit), 3) / CONSTANTS.MU)) / 3600.0;
    }

    const deltaVToEscape = Math.max(0.0, v_esc - v_tan);

    return {
      specificEnergyMJ: specificEnergy * 1.0e-6,
      semiMajorAxisKM: a_orbit * 1.0e-3,
      eccentricity: e,
      perigeeAltitudeKM: Math.max(0.0, perigeeRadius - CONSTANTS.R_E) * 1.0e-3,
      apogeeAltitudeKM: (apogeeRadius === Infinity) ? Infinity : Math.max(0.0, apogeeRadius - CONSTANTS.R_E) * 1.0e-3,
      periodHours: periodHours,
      orbitType: orbitType,
      deltaVToEscapeMPS: deltaVToEscape
    };
  }

  // =======================================================================================
  // 9. 4TH-ORDER RUNGE-KUTTA (RK4) KINEMATICS INTEGRATOR
  // =======================================================================================

  /**
   * Advances the climber state [altitude, velocity] across a time interval dt using
   * a 4th-order Runge-Kutta numerical integration scheme.
   * 
   * Ensures strict kinematic consistency: velocity = dh / dt_sim.
   * Includes smooth acceleration rate limiting towards target speed.
   * 
   * @param {number} currentAlt Altitude in meters (>= 0).
   * @param {number} currentVel Current climb velocity in m/s.
   * @param {number} targetSpeed Commanded target cruising speed in m/s.
   * @param {number} dt Numerical integration time step in seconds (e.g. 0.05 to 1.0 s).
   * @param {number} [mass] Climber mass in kg (default: 20,000 kg).
   * @param {Object} [options] Integration parameters { maxAccel, accelTimeConstant }.
   * @returns {Object} { altitude: number, velocity: number, acceleration: number, dt: number }
   */
  function integrateKinematics(
    currentAlt,
    currentVel,
    targetSpeed,
    dt,
    mass = CONSTANTS.DEFAULT_CLIMBER_MASS,
    options = {}
  ) {
    const maxAccel = options.maxAccel ?? CONSTANTS.DEFAULT_MAX_ACCEL; // m/s^2
    const tau = options.accelTimeConstant ?? 1.0; // seconds

    // Derivative evaluation function: [dh/dt, dv/dt]
    function derivatives(h, v) {
      const clampedV = v;
      // Commanded acceleration targeting desired cruise speed
      const rawA = (targetSpeed - clampedV) / tau;
      const a = Math.max(-maxAccel, Math.min(maxAccel, rawA));
      return { dh: clampedV, dv: a };
    }

    // Stage 1 (k1)
    const k1 = derivatives(currentAlt, currentVel);

    // Stage 2 (k2)
    const h2 = currentAlt + 0.5 * dt * k1.dh;
    const v2 = currentVel + 0.5 * dt * k1.dv;
    const k2 = derivatives(h2, v2);

    // Stage 3 (k3)
    const h3 = currentAlt + 0.5 * dt * k2.dh;
    const v3 = currentVel + 0.5 * dt * k2.dv;
    const k3 = derivatives(h3, v3);

    // Stage 4 (k4)
    const h4 = currentAlt + dt * k3.dh;
    const v4 = currentVel + dt * k3.dv;
    const k4 = derivatives(h4, v4);

    // Weighted RK4 step: y_{n+1} = y_n + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
    const deltaH = (dt / 6.0) * (k1.dh + 2.0 * k2.dh + 2.0 * k3.dh + k4.dh);
    const deltaV = (dt / 6.0) * (k1.dv + 2.0 * k2.dv + 2.0 * k3.dv + k4.dv);

    const nextAlt = Math.max(0.0, currentAlt + deltaH);
    const nextVel = currentVel + deltaV;
    const effAccel = (k1.dv + 2.0 * k2.dv + 2.0 * k3.dv + k4.dv) / 6.0;

    return {
      altitude: nextAlt,
      velocity: nextVel,
      acceleration: effAccel,
      dt: dt
    };
  }

  // =======================================================================================
  // 10. COMPUTE STATE: COMPLETE 100+ TELEMETRY CHANNELS ENGINE
  // =======================================================================================

  /**
   * Computes the complete instantaneous physical state of the space elevator system,
   * returning 120+ verified telemetry channels categorized into logical aerospace subsystems
   * and indexed by unique string identifiers in .channels.
   * 
   * @param {number} altitudeMeters Climber altitude above Earth equatorial surface (m).
   * @param {number} [velocityMs] Climbing speed along tether in m/s (default: 125 m/s = 450 km/h).
   * @param {number} [latitudeDeg] Anchor geodetic latitude in degrees (default: 0.0 deg).
   * @param {number} [climberMassKg] Climber total mass in kg (default: 20,000 kg).
   * @param {Object} [options] Simulation and physical overrides.
   * @returns {Object} Comprehensive telemetry state tree with channels dictionary.
   */
  function computeState(
    altitudeMeters = 0.0,
    velocityMs = CONSTANTS.DEFAULT_CLIMB_SPEED,
    latitudeDeg = 0.0,
    climberMassKg = CONSTANTS.DEFAULT_CLIMBER_MASS,
    options = {}
  ) {
    const h = Math.max(0.0, altitudeMeters);
    const r = CONSTANTS.R_E + h;
    const v = velocityMs;
    const mass = climberMassKg;
    const accel = options.accelerationMs2 ?? 0.0;
    const baseArea = options.tetherBaseArea ?? CONSTANTS.TETHER_BASE_AREA;
    const payloadMass = options.payloadMassKg ?? CONSTANTS.DEFAULT_PAYLOAD_MASS;
    const metSeconds = options.metSeconds ?? (v > 0 ? h / v : 0.0);

    // 1. Gravity & Accelerations
    const g_grav = gravity(r);
    const a_cent = centrifugal(r);
    const g_eff = effectiveGravity(r);
    const g_eff_g = g_eff / CONSTANTS.G_STANDARD;
    const isAtGeo = Math.abs(h - CONSTANTS.H_GEO) < 1.0;
    const netDirection = isAtGeo ? 'Neutral (Zero-G)' : (g_eff > 0 ? 'Earth-ward (Inward)' : 'Space-ward (Outward)');

    // 2. Velocities
    const v_tan = tangentialSpeed(r);
    const v_circ = circularOrbitalVelocity(r);
    const v_esc = escapeVelocity(r);
    const c3 = hyperbolicExcessEnergy(r);

    // 3. Atmosphere & Aerodynamics
    const atmo = atmosphere(h);
    const q_dyn = 0.5 * atmo.density * v * v;
    const cd = options.cd ?? CONSTANTS.DEFAULT_CD;
    const frontalArea = options.frontalArea ?? CONSTANTS.DEFAULT_FRONTAL_AREA;
    const f_drag = q_dyn * cd * frontalArea;
    const dragPowerW = f_drag * Math.abs(v);
    const mach = (atmo.speedOfSound > 0) ? Math.abs(v) / atmo.speedOfSound : 0.0;

    let aeroRegime = 'Deep Space Vacuum';
    if (h < 11000.0) aeroRegime = 'Tropospheric Continuum';
    else if (h < 25000.0) aeroRegime = 'Stratospheric Continuum';
    else if (h < 50000.0) aeroRegime = 'Upper Stratosphere';
    else if (h < 85000.0) aeroRegime = 'Mesospheric Slip Flow';
    else if (h <= 100000.0) aeroRegime = 'Transition / Free Molecular';

    // 4. Tether Material & Taper
    const tRatio = taperRatio(r);
    const localArea = taperArea(r, baseArea);
    const equivRadiusMm = Math.sqrt(localArea / Math.PI) * 1000.0;

    // 5. Stress, Tension & Safety Factors
    const stressData = dynamicStress(r, mass, accel, v, baseArea);
    const marginOfSafety = (stressData.safetyFactor / CONSTANTS.DESIGN_SF) - 1.0;

    // 6. Coriolis Dynamics
    const coriolisData = coriolisDynamics(r, mass, v);

    // 7. Power Beaming & Climber Mechanics
    const powerData = climberPower(h, v, accel, mass, options);

    // 8. Non-Equatorial Shear
    const shearData = nonEquatorialShear(latitudeDeg, h, baseArea);

    // 9. Orbital Release Trajectory
    const orbitalData = orbitalParameters(r);

    // 10. Mission Energy & Operations
    // Gravitational potential energy relative to surface: U = -mu*m/r - (-mu*m/R_e) = mu*m*(1/R_e - 1/r)
    const potentialEnergyJ = CONSTANTS.MU * mass * (1.0 / CONSTANTS.R_E - 1.0 / r);
    const kineticEnergyJ = 0.5 * mass * (v * v + v_tan * v_tan);
    const totalEnergyGJ = (potentialEnergyJ + kineticEnergyJ) * 1.0e-9;
    const remainingToGeoM = Math.max(0.0, CONSTANTS.H_GEO - h);
    const transitTimeToGeoHours = (v > 0) ? (remainingToGeoM / v) / 3600.0 : Infinity;
    const remainingToApexM = Math.max(0.0, CONSTANTS.APEX_ALTITUDE - h);
    const transitTimeToApexHours = (v > 0) ? (remainingToApexM / v) / 3600.0 : Infinity;
    const co2SavingsTons = (h / CONSTANTS.H_GEO) * (mass / 1000.0) * 15.2; // approx rocket emissions factor

    // Structured Categories
    const position = {
      altitude_m: h,
      altitude_km: h * 1.0e-3,
      radius_m: r,
      radius_km: r * 1.0e-3,
      fraction_to_geo: h / CONSTANTS.H_GEO,
      fraction_to_apex: h / CONSTANTS.APEX_ALTITUDE,
      latitude_deg: latitudeDeg,
      latitude_rad: latitudeDeg * (Math.PI / 180.0),
      longitude_deg: options.longitudeDeg ?? 0.0,
      zenith_angle_deg: Math.abs(shearData.psiDeg)
    };

    const gravity_telemetry = {
      g_grav_mps2: g_grav,
      a_centrifugal_mps2: a_cent,
      g_eff_mps2: g_eff,
      g_eff_g: g_eff_g,
      g_grav_ratio_surface: g_grav / CONSTANTS.G0,
      a_centrifugal_ratio_surface: a_cent / CONSTANTS.G0,
      net_acceleration_vector_mag: Math.abs(g_eff),
      net_acceleration_direction: netDirection,
      geo_equilibrium_offset_m: r - CONSTANTS.R_GEO,
      tidal_acceleration_gradient_mps2_m: (2.0 * CONSTANTS.MU / Math.pow(r, 3)) + (CONSTANTS.OMEGA * CONSTANTS.OMEGA)
    };

    const kinematics = {
      v_climb_mps: v,
      v_climb_kmh: v * 3.6,
      v_tan_mps: v_tan,
      v_tan_kms: v_tan * 1.0e-3,
      v_circ_mps: v_circ,
      v_circ_kms: v_circ * 1.0e-3,
      v_esc_mps: v_esc,
      v_esc_kms: v_esc * 1.0e-3,
      mach_number: mach,
      speed_of_sound_mps: atmo.speedOfSound
    };

    const orbital = {
      c3_energy_km2_s2: c3,
      c3_energy_m2_s2: c3 * 1.0e6,
      specific_orbital_energy_mj_kg: orbitalData.specificEnergyMJ,
      release_orbit_semi_major_axis_km: orbitalData.semiMajorAxisKM,
      release_orbit_eccentricity: orbitalData.eccentricity,
      release_orbit_perigee_altitude_km: orbitalData.perigeeAltitudeKM,
      release_orbit_apogee_altitude_km: orbitalData.apogeeAltitudeKM,
      release_orbit_period_hours: orbitalData.periodHours,
      release_orbit_type: orbitalData.orbitType,
      delta_v_to_escape_mps: orbitalData.deltaVToEscapeMPS
    };

    const atmosphere_telemetry = {
      temperature_k: atmo.temperature,
      temperature_c: atmo.temperature > 0 ? (atmo.temperature - 273.15) : -273.15,
      pressure_pa: atmo.pressure,
      pressure_atm: atmo.pressure / 101325.0,
      density_kg_m3: atmo.density,
      density_ratio_sea_level: atmo.density / 1.2250,
      dynamic_pressure_pa: q_dyn,
      atmospheric_scale_height_m: CONSTANTS.ATM_SCALE_HEIGHT,
      mean_free_path_m: (atmo.pressure > 0) ? (66.0e-9 * (101325.0 / atmo.pressure) * (atmo.temperature / 288.15)) : Infinity,
      aerodynamic_regime: aeroRegime
    };

    const aerodynamics = {
      cd_drag_coefficient: cd,
      frontal_area_m2: frontalArea,
      drag_force_n: f_drag,
      drag_force_kn: f_drag * 1.0e-3,
      drag_power_w: dragPowerW,
      drag_power_kw: dragPowerW * 1.0e-3,
      reynolds_number: (atmo.density > 0) ? (atmo.density * Math.abs(v) * Math.sqrt(frontalArea) / 1.81e-5) : 0.0,
      knudsen_number: (atmo.pressure > 0) ? ((66.0e-9 * (101325.0 / atmo.pressure) * (atmo.temperature / 288.15)) / Math.sqrt(frontalArea)) : Infinity
    };

    const tether = {
      material_name: CONSTANTS.MATERIAL_NAME,
      material_density_kg_m3: CONSTANTS.RHO_MAT,
      sigma_work_pa: CONSTANTS.SIGMA_WORK,
      sigma_work_gpa: CONSTANTS.SIGMA_WORK * 1.0e-9,
      sigma_ult_pa: CONSTANTS.SIGMA_ULT,
      sigma_ult_gpa: CONSTANTS.SIGMA_ULT * 1.0e-9,
      char_length_km: CONSTANTS.L_C * 1.0e-3,
      taper_ratio: tRatio,
      tether_area_m2: localArea,
      tether_area_mm2: localArea * 1.0e6,
      tether_radius_equivalent_mm: equivRadiusMm
    };

    const stress = {
      tether_static_tension_n: stressData.staticTension,
      tether_static_tension_mn: stressData.staticTension * 1.0e-6,
      climber_dynamic_load_n: stressData.climberLoad,
      total_tension_n: stressData.totalTension,
      total_tension_kn: stressData.totalTension * 1.0e-3,
      total_tension_mn: stressData.totalTension * 1.0e-6,
      axial_stress_pa: stressData.axialStress,
      axial_stress_gpa: stressData.axialStress * 1.0e-9,
      safety_factor: stressData.safetyFactor,
      margin_of_safety: marginOfSafety
    };

    const coriolis = {
      coriolis_accel_mps2: coriolisData.accel,
      coriolis_force_n: coriolisData.force,
      coriolis_force_kn: coriolisData.force * 1.0e-3,
      coriolis_direction: coriolisData.direction,
      coriolis_lag_angle_rad: coriolisData.lagAngleRad,
      coriolis_lag_angle_deg: coriolisData.lagAngleDeg,
      tether_deflection_angle_deg: coriolisData.tetherDeflectionDeg,
      tether_lateral_displacement_m: coriolisData.lateralDisplacement,
      coriolis_restoring_force_n: Math.abs(coriolisData.force),
      coriolis_torque_nm: Math.abs(coriolisData.force) * r
    };

    const power = {
      climber_mass_kg: mass,
      climber_weight_n: powerData.climberWeightN,
      climber_acceleration_mps2: accel,
      inertial_force_n: mass * accel,
      thrust_force_n: powerData.thrustForceN,
      thrust_force_kn: powerData.thrustForceKN,
      mechanical_power_w: powerData.mechanicalPowerW,
      mechanical_power_kw: powerData.mechanicalPowerKW,
      mechanical_power_mw: powerData.mechanicalPowerMW,
      regen_power_kw: powerData.regenPowerKW,
      eta_drive: powerData.etaDrive,
      eta_pv: powerData.etaPV,
      eta_atm: powerData.etaAtm,
      eta_system_total: powerData.etaSystemTotal,
      laser_beam_power_w: powerData.laserBeamPowerW,
      laser_beam_power_mw: powerData.laserBeamPowerMW,
      climber_status: powerData.climberStatus
    };

    const non_equatorial = {
      anchor_latitude_deg: shearData.latitudeDeg,
      incline_angle_psi_rad: shearData.psiRad,
      incline_angle_psi_deg: shearData.psiDeg,
      lateral_shear_force_n: shearData.shearForceN,
      lateral_shear_force_kn: shearData.shearForceKN,
      axial_anchor_force_n: shearData.axialForceN,
      shear_to_tension_ratio: shearData.shearToTensionRatio,
      shear_warning_flag: shearData.warningFlag,
      shear_stability_status: shearData.status
    };

    const mission = {
      potential_energy_gj: potentialEnergyJ * 1.0e-9,
      kinetic_energy_gj: kineticEnergyJ * 1.0e-9,
      total_mechanical_energy_gj: totalEnergyGJ,
      transit_time_to_geo_hours: transitTimeToGeoHours,
      transit_time_to_apex_hours: transitTimeToApexHours,
      cumulative_energy_consumed_mwh: (powerData.laserBeamPowerMW * (metSeconds / 3600.0)),
      payload_fraction: payloadMass / mass,
      co2_savings_vs_rocket_tons: co2SavingsTons,
      mission_elapsed_time_s: metSeconds,
      telemetry_timestamp_iso: new Date().toISOString()
    };

    // Dictionary of all 120+ flat channels with metadata
    const channels = {};
    const registerChannel = (id, value, unit, category, description) => {
      channels[id] = { id, value, unit, category, description };
    };

    // Category 1: Position
    registerChannel('altitude_m', position.altitude_m, 'm', 'Position', 'Radial altitude above Earth equatorial surface');
    registerChannel('altitude_km', position.altitude_km, 'km', 'Position', 'Climber altitude in kilometers');
    registerChannel('radius_m', position.radius_m, 'm', 'Position', 'Geocentric distance from Earth center');
    registerChannel('radius_km', position.radius_km, 'km', 'Position', 'Geocentric distance in kilometers');
    registerChannel('fraction_to_geo', position.fraction_to_geo, 'ratio', 'Position', 'Fraction of climb completed to GEO (35,786 km)');
    registerChannel('fraction_to_apex', position.fraction_to_apex, 'ratio', 'Position', 'Fraction of climb completed to Apex Counterweight');
    registerChannel('latitude_deg', position.latitude_deg, 'deg', 'Position', 'Tether anchor geodetic latitude');
    registerChannel('latitude_rad', position.latitude_rad, 'rad', 'Position', 'Tether anchor latitude in radians');
    registerChannel('longitude_deg', position.longitude_deg, 'deg', 'Position', 'Equatorial anchor sub-satellite longitude');
    registerChannel('zenith_angle_deg', position.zenith_angle_deg, 'deg', 'Position', 'Off-vertical zenith inclination angle');

    // Category 2: Gravitation & Acceleration
    registerChannel('g_grav_mps2', gravity_telemetry.g_grav_mps2, 'm/s^2', 'Gravitation', 'Inward Newtonian gravitational acceleration');
    registerChannel('a_centrifugal_mps2', gravity_telemetry.a_centrifugal_mps2, 'm/s^2', 'Gravitation', 'Outward co-rotational centrifugal acceleration');
    registerChannel('g_eff_mps2', gravity_telemetry.g_eff_mps2, 'm/s^2', 'Gravitation', 'Effective net gravity (g - a_c, exactly 0.0000 at GEO)');
    registerChannel('g_eff_g', gravity_telemetry.g_eff_g, 'G', 'Gravitation', 'Effective net gravity in Earth standard G-units');
    registerChannel('g_grav_ratio_surface', gravity_telemetry.g_grav_ratio_surface, 'ratio', 'Gravitation', 'Ratio of local gravity to sea-level gravity');
    registerChannel('a_centrifugal_ratio_surface', gravity_telemetry.a_centrifugal_ratio_surface, 'ratio', 'Gravitation', 'Ratio of centrifugal acceleration to surface gravity');
    registerChannel('net_acceleration_vector_mag', gravity_telemetry.net_acceleration_vector_mag, 'm/s^2', 'Gravitation', 'Scalar magnitude of net acceleration');
    registerChannel('net_acceleration_direction', gravity_telemetry.net_acceleration_direction, 'string', 'Gravitation', 'Direction of net acceleration vector');
    registerChannel('geo_equilibrium_offset_m', gravity_telemetry.geo_equilibrium_offset_m, 'm', 'Gravitation', 'Radial offset distance from exact GEO equilibrium');
    registerChannel('tidal_acceleration_gradient_mps2_m', gravity_telemetry.tidal_acceleration_gradient_mps2_m, 's^-2', 'Gravitation', 'Tidal gravitational gradient tensor component');

    // Category 3: Kinematics & Velocities
    registerChannel('v_climb_mps', kinematics.v_climb_mps, 'm/s', 'Kinematics', 'Vertical climbing velocity along tether');
    registerChannel('v_climb_kmh', kinematics.v_climb_kmh, 'km/h', 'Kinematics', 'Climbing speed in kilometers per hour');
    registerChannel('v_tan_mps', kinematics.v_tan_mps, 'm/s', 'Kinematics', 'Tangential orbital velocity from Earth rotation');
    registerChannel('v_tan_kms', kinematics.v_tan_kms, 'km/s', 'Kinematics', 'Tangential speed in km/s');
    registerChannel('v_circ_mps', kinematics.v_circ_mps, 'm/s', 'Kinematics', 'Local circular orbital speed');
    registerChannel('v_circ_kms', kinematics.v_circ_kms, 'km/s', 'Kinematics', 'Circular orbital speed in km/s');
    registerChannel('v_esc_mps', kinematics.v_esc_mps, 'm/s', 'Kinematics', 'Local parabolic escape velocity');
    registerChannel('v_esc_kms', kinematics.v_esc_kms, 'km/s', 'Kinematics', 'Escape velocity in km/s');
    registerChannel('mach_number', kinematics.mach_number, 'Mach', 'Kinematics', 'Aerodynamic Mach number relative to atmosphere');
    registerChannel('speed_of_sound_mps', kinematics.speed_of_sound_mps, 'm/s', 'Kinematics', 'Local speed of sound');

    // Category 4: Orbital Mechanics & Release
    registerChannel('c3_energy_km2_s2', orbital.c3_energy_km2_s2, 'km^2/s^2', 'Orbital', 'Hyperbolic excess energy C3 (v_tan^2 - v_esc^2)');
    registerChannel('c3_energy_m2_s2', orbital.c3_energy_m2_s2, 'm^2/s^2', 'Orbital', 'Hyperbolic excess energy in m^2/s^2');
    registerChannel('specific_orbital_energy_mj_kg', orbital.specific_orbital_energy_mj_kg, 'MJ/kg', 'Orbital', 'Specific orbital mechanical energy if released');
    registerChannel('release_orbit_semi_major_axis_km', orbital.release_orbit_semi_major_axis_km, 'km', 'Orbital', 'Semi-major axis of tangential release orbit');
    registerChannel('release_orbit_eccentricity', orbital.release_orbit_eccentricity, 'dimensionless', 'Orbital', 'Orbital eccentricity of equatorial release orbit');
    registerChannel('release_orbit_perigee_altitude_km', orbital.release_orbit_perigee_altitude_km, 'km', 'Orbital', 'Perigee altitude of release orbit');
    registerChannel('release_orbit_apogee_altitude_km', orbital.release_orbit_apogee_altitude_km, 'km', 'Orbital', 'Apogee altitude of release orbit');
    registerChannel('release_orbit_period_hours', orbital.release_orbit_period_hours, 'hours', 'Orbital', 'Orbital period for closed orbits');
    registerChannel('release_orbit_type', orbital.release_orbit_type, 'string', 'Orbital', 'Classification of release orbital trajectory');
    registerChannel('delta_v_to_escape_mps', orbital.delta_v_to_escape_mps, 'm/s', 'Orbital', 'Impulsive delta-v required to achieve escape velocity');

    // Category 5: Atmosphere
    registerChannel('temperature_k', atmosphere_telemetry.temperature_k, 'K', 'Atmosphere', 'Static air temperature (US Standard 1976)');
    registerChannel('temperature_c', atmosphere_telemetry.temperature_c, 'deg C', 'Atmosphere', 'Static air temperature in Celsius');
    registerChannel('pressure_pa', atmosphere_telemetry.pressure_pa, 'Pa', 'Atmosphere', 'Static barometric air pressure');
    registerChannel('pressure_atm', atmosphere_telemetry.pressure_atm, 'atm', 'Atmosphere', 'Barometric pressure in standard atmospheres');
    registerChannel('density_kg_m3', atmosphere_telemetry.density_kg_m3, 'kg/m^3', 'Atmosphere', 'Atmospheric mass density');
    registerChannel('density_ratio_sea_level', atmosphere_telemetry.density_ratio_sea_level, 'ratio', 'Atmosphere', 'Density ratio to standard sea level');
    registerChannel('dynamic_pressure_pa', atmosphere_telemetry.dynamic_pressure_pa, 'Pa', 'Atmosphere', 'Dynamic pressure q = 0.5 * rho * v^2');
    registerChannel('atmospheric_scale_height_m', atmosphere_telemetry.atmospheric_scale_height_m, 'm', 'Atmosphere', 'Optical attenuation scale height');
    registerChannel('mean_free_path_m', atmosphere_telemetry.mean_free_path_m, 'm', 'Atmosphere', 'Mean free path of air molecules');
    registerChannel('aerodynamic_regime', atmosphere_telemetry.aerodynamic_regime, 'string', 'Atmosphere', 'Atmospheric gas-dynamic flow regime');

    // Category 6: Aerodynamic Loads & Drag
    registerChannel('cd_drag_coefficient', aerodynamics.cd_drag_coefficient, 'dimensionless', 'Aerodynamics', 'Climber aerodynamic drag coefficient');
    registerChannel('frontal_area_m2', aerodynamics.frontal_area_m2, 'm^2', 'Aerodynamics', 'Climber frontal aerodynamic area');
    registerChannel('drag_force_n', aerodynamics.drag_force_n, 'N', 'Aerodynamics', 'Aerodynamic drag force resisting ascent');
    registerChannel('drag_force_kn', aerodynamics.drag_force_kn, 'kN', 'Aerodynamics', 'Drag force in kilonewtons');
    registerChannel('drag_power_w', aerodynamics.drag_power_w, 'W', 'Aerodynamics', 'Rate of energy dissipation by drag');
    registerChannel('drag_power_kw', aerodynamics.drag_power_kw, 'kW', 'Aerodynamics', 'Drag power dissipation in kilowatts');
    registerChannel('reynolds_number', aerodynamics.reynolds_number, 'dimensionless', 'Aerodynamics', 'Flow Reynolds number');
    registerChannel('knudsen_number', aerodynamics.knudsen_number, 'dimensionless', 'Aerodynamics', 'Flow Knudsen number');

    // Category 7: Tether Material & Taper
    registerChannel('material_name', tether.material_name, 'string', 'Tether', 'Structural tether material classification');
    registerChannel('material_density_kg_m3', tether.material_density_kg_m3, 'kg/m^3', 'Tether', 'Material volumetric mass density');
    registerChannel('sigma_work_pa', tether.sigma_work_pa, 'Pa', 'Tether', 'Design working tensile stress');
    registerChannel('sigma_work_gpa', tether.sigma_work_gpa, 'GPa', 'Tether', 'Design working stress in GPa');
    registerChannel('sigma_ult_pa', tether.sigma_ult_pa, 'Pa', 'Tether', 'Material ultimate tensile strength');
    registerChannel('sigma_ult_gpa', tether.sigma_ult_gpa, 'GPa', 'Tether', 'Material ultimate strength in GPa');
    registerChannel('char_length_km', tether.char_length_km, 'km', 'Tether', 'Characteristic breaking length L_c = sigma / (rho * g0)');
    registerChannel('taper_ratio', tether.taper_ratio, 'ratio', 'Tether', 'Pearson-Aravind area taper ratio A(r) / A_base');
    registerChannel('tether_area_m2', tether.tether_area_m2, 'm^2', 'Tether', 'Local tether cross-sectional area');
    registerChannel('tether_area_mm2', tether.tether_area_mm2, 'mm^2', 'Tether', 'Tether cross-sectional area in mm^2');
    registerChannel('tether_radius_equivalent_mm', tether.tether_radius_equivalent_mm, 'mm', 'Tether', 'Equivalent circular cylinder radius in mm');

    // Category 8: Structural Stress & Safety
    registerChannel('tether_static_tension_n', stress.tether_static_tension_n, 'N', 'Stress', 'Static equilibrium tension carried by tether');
    registerChannel('tether_static_tension_mn', stress.tether_static_tension_mn, 'MN', 'Stress', 'Static tether tension in Meganewtons');
    registerChannel('climber_dynamic_load_n', stress.climber_dynamic_load_n, 'N', 'Stress', 'Dynamic load imposed by climber on tether');
    registerChannel('total_tension_n', stress.total_tension_n, 'N', 'Stress', 'Total dynamic structural tension T(r)');
    registerChannel('total_tension_kn', stress.total_tension_kn, 'kN', 'Stress', 'Total dynamic tension in kilonewtons');
    registerChannel('total_tension_mn', stress.total_tension_mn, 'MN', 'Stress', 'Total dynamic tension in Meganewtons');
    registerChannel('axial_stress_pa', stress.axial_stress_pa, 'Pa', 'Stress', 'Realized axial tensile stress sigma(r)');
    registerChannel('axial_stress_gpa', stress.axial_stress_gpa, 'GPa', 'Stress', 'Realized axial stress in GPa');
    registerChannel('safety_factor', stress.safety_factor, 'ratio', 'Stress', 'Structural safety factor SF = sigma_ult / sigma');
    registerChannel('margin_of_safety', stress.margin_of_safety, 'ratio', 'Stress', 'Margin of safety MS = SF / SF_design - 1');

    // Category 9: Coriolis Dynamics
    registerChannel('coriolis_accel_mps2', coriolis.coriolis_accel_mps2, 'm/s^2', 'Coriolis', 'Transverse Coriolis acceleration magnitude 2*omega*v');
    registerChannel('coriolis_force_n', coriolis.coriolis_force_n, 'N', 'Coriolis', 'Transverse Coriolis inertial force 2*M*omega*v');
    registerChannel('coriolis_force_kn', coriolis.coriolis_force_kn, 'kN', 'Coriolis', 'Coriolis force in kilonewtons');
    registerChannel('coriolis_direction', coriolis.coriolis_direction, 'string', 'Coriolis', 'Coriolis force transverse orientation');
    registerChannel('coriolis_lag_angle_rad', coriolis.coriolis_lag_angle_rad, 'rad', 'Coriolis', 'Climber dynamic tilt/lag angle');
    registerChannel('coriolis_lag_angle_deg', coriolis.coriolis_lag_angle_deg, 'deg', 'Coriolis', 'Climber lag angle in degrees');
    registerChannel('tether_deflection_angle_deg', coriolis.tether_deflection_angle_deg, 'deg', 'Coriolis', 'Structural tether deflection angle');
    registerChannel('tether_lateral_displacement_m', coriolis.tether_lateral_displacement_m, 'm', 'Coriolis', 'Estimated lateral displacement distance');
    registerChannel('coriolis_restoring_force_n', coriolis.coriolis_restoring_force_n, 'N', 'Coriolis', 'Restoring force component balancing Coriolis');
    registerChannel('coriolis_torque_nm', coriolis.coriolis_torque_nm, 'N*m', 'Coriolis', 'Torque exerted by Coriolis force about Earth center');

    // Category 10: Power & Laser Beaming
    registerChannel('climber_mass_kg', power.climber_mass_kg, 'kg', 'Power', 'Total wet mass of climber vehicle');
    registerChannel('climber_weight_n', power.climber_weight_n, 'N', 'Power', 'Gravitational effective weight M * g_eff');
    registerChannel('climber_acceleration_mps2', power.climber_acceleration_mps2, 'm/s^2', 'Power', 'Commanded vertical acceleration');
    registerChannel('inertial_force_n', power.inertial_force_n, 'N', 'Power', 'Inertial acceleration reaction force M * a');
    registerChannel('thrust_force_n', power.thrust_force_n, 'N', 'Power', 'Climber drive thrust required');
    registerChannel('thrust_force_kn', power.thrust_force_kn, 'kN', 'Power', 'Drive thrust in kilonewtons');
    registerChannel('mechanical_power_w', power.mechanical_power_w, 'W', 'Power', 'Mechanical drive shaft power P = F_thrust * v');
    registerChannel('mechanical_power_kw', power.mechanical_power_kw, 'kW', 'Power', 'Mechanical drive power in kilowatts');
    registerChannel('mechanical_power_mw', power.mechanical_power_mw, 'MW', 'Power', 'Mechanical drive power in Megawatts');
    registerChannel('regen_power_kw', power.regenPowerKW, 'kW', 'Power', 'Regenerative braking electrical power generated');
    registerChannel('eta_drive', power.eta_drive, 'ratio', 'Power', 'Pinch-roller electric drive efficiency');
    registerChannel('eta_pv', power.eta_pv, 'ratio', 'Power', 'GaAs monochromatic PV receiver efficiency');
    registerChannel('eta_atm', power.eta_atm, 'ratio', 'Power', 'Atmospheric optical transmission efficiency');
    registerChannel('eta_system_total', power.eta_system_total, 'ratio', 'Power', 'End-to-end beamed-energy transmission efficiency');
    registerChannel('laser_beam_power_w', power.laser_beam_power_w, 'W', 'Power', 'Ground station laser emitted optical power');
    registerChannel('laser_beam_power_mw', power.laser_beam_power_mw, 'MW', 'Power', 'Laser beam power in Megawatts');
    registerChannel('climber_status', power.climber_status, 'string', 'Power', 'Operational motion and drivetrain mode');

    // Category 11: Non-Equatorial Shear
    registerChannel('anchor_latitude_deg', non_equatorial.anchor_latitude_deg, 'deg', 'Non-Equatorial', 'Anchor platform geodetic latitude');
    registerChannel('incline_angle_psi_rad', non_equatorial.incline_angle_psi_rad, 'rad', 'Non-Equatorial', 'Off-axis equilibrium inclination cone angle psi');
    registerChannel('incline_angle_psi_deg', non_equatorial.incline_angle_psi_deg, 'deg', 'Non-Equatorial', 'Off-axis inclination angle psi in degrees');
    registerChannel('lateral_shear_force_n', non_equatorial.lateral_shear_force_n, 'N', 'Non-Equatorial', 'Equatorward lateral shear force on anchor T*sin(psi)');
    registerChannel('lateral_shear_force_kn', non_equatorial.lateral_shear_force_kn, 'kN', 'Non-Equatorial', 'Lateral shear force in kilonewtons');
    registerChannel('axial_anchor_force_n', non_equatorial.axial_anchor_force_n, 'N', 'Non-Equatorial', 'Vertical holding tension on anchor T*cos(psi)');
    registerChannel('shear_to_tension_ratio', non_equatorial.shear_to_tension_ratio, 'ratio', 'Non-Equatorial', 'Ratio of shear to axial force tan(psi)');
    registerChannel('shear_warning_flag', non_equatorial.shear_warning_flag, 'boolean', 'Non-Equatorial', 'Off-axis lateral shear hazard alert flag');
    registerChannel('shear_stability_status', non_equatorial.shear_stability_status, 'string', 'Non-Equatorial', 'Structural stability status assessment');

    // Category 12: Mission Energy & Operations
    registerChannel('potential_energy_gj', mission.potential_energy_gj, 'GJ', 'Mission', 'Gravitational potential energy relative to surface');
    registerChannel('kinetic_energy_gj', mission.kinetic_energy_gj, 'GJ', 'Mission', 'Kinetic energy (climbing + orbital tangential)');
    registerChannel('total_mechanical_energy_gj', mission.total_mechanical_energy_gj, 'GJ', 'Mission', 'Total mechanical energy of climber vehicle');
    registerChannel('transit_time_to_geo_hours', mission.transit_time_to_geo_hours, 'hours', 'Mission', 'Remaining climb transit time to GEO at current speed');
    registerChannel('transit_time_to_apex_hours', mission.transit_time_to_apex_hours, 'hours', 'Mission', 'Remaining climb transit time to Apex at current speed');
    registerChannel('cumulative_energy_consumed_mwh', mission.cumulative_energy_consumed_mwh, 'MWh', 'Mission', 'Estimated cumulative electrical energy consumed');
    registerChannel('payload_fraction', mission.payload_fraction, 'ratio', 'Mission', 'Ratio of payload mass to total climber mass');
    registerChannel('co2_savings_vs_rocket_tons', mission.co2_savings_vs_rocket_tons, 'tons CO2', 'Mission', 'Emissions offset vs equivalent rocket launches');
    registerChannel('mission_elapsed_time_s', mission.mission_elapsed_time_s, 's', 'Mission', 'Current Mission Elapsed Time MET');
    registerChannel('telemetry_timestamp_iso', mission.telemetry_timestamp_iso, 'ISO string', 'Mission', 'Timestamp of telemetry computation');

    return {
      // Direct categorized subsystems
      position,
      gravity: gravity_telemetry,
      kinematics,
      orbital,
      atmosphere: atmosphere_telemetry,
      aerodynamics,
      tether,
      stress,
      coriolis,
      power,
      non_equatorial,
      mission,

      // Flat dictionary of all 120+ telemetry channels
      channels,

      // Array format for UI grids / HUD rendering tables
      channelList: Object.values(channels),

      // Helper accessor method: get(channelId)
      get: function (channelId) {
        return channels[channelId] ? channels[channelId].value : undefined;
      }
    };
  }

  // =======================================================================================
  // 11. PUBLIC EXPORT NAMESPACE DEFINITION
  // =======================================================================================
  /**
   * Dynamically switches the active structural tether material and recalibrates all
   * continuous mathematical physical constants (density, working stress, UTS, L_c, cruise speed).
   * @param {string} materialKey ('CNT', 'Graphene', 'Super-Laminate', 'hBN')
   * @returns {Object} Updated CONSTANTS dictionary
   */
  function setMaterial(materialKey) {
    const key = (materialKey || 'cnt').toLowerCase().replace(/[\s_-]/g, '');
    if (key === 'cnt') {
      CONSTANTS.MATERIAL_NAME = 'Carbon Nanotube (CNT) Macro-Yarn';
      CONSTANTS.RHO_MAT = 1300.0;
      CONSTANTS.SIGMA_WORK = 47.5e9;
      CONSTANTS.SIGMA_ULT = 95.0e9;
      CONSTANTS.DESIGN_SF = 2.0;
      CONSTANTS.DEFAULT_CLIMB_SPEED = 125.0; // 450 km/h
      CONSTANTS.L_C = 47.5e9 / (1300.0 * 9.798);
    } else if (key === 'graphene') {
      CONSTANTS.MATERIAL_NAME = 'Monolayer Graphene Ribbon Array';
      CONSTANTS.RHO_MAT = 2200.0;
      CONSTANTS.SIGMA_WORK = 65.0e9;
      CONSTANTS.SIGMA_ULT = 130.0e9;
      CONSTANTS.DESIGN_SF = 2.0;
      CONSTANTS.DEFAULT_CLIMB_SPEED = 180.55; // 650 km/h
      CONSTANTS.L_C = 65.0e9 / (2200.0 * 9.798);
    } else if (key === 'superlaminate') {
      CONSTANTS.MATERIAL_NAME = 'Super-Laminate (CNT/PMR-15 Composite)';
      CONSTANTS.RHO_MAT = 1800.0;
      CONSTANTS.SIGMA_WORK = 37.5e9;
      CONSTANTS.SIGMA_ULT = 75.0e9;
      CONSTANTS.DESIGN_SF = 2.0;
      CONSTANTS.DEFAULT_CLIMB_SPEED = 88.89; // 320 km/h
      CONSTANTS.L_C = 37.5e9 / (1800.0 * 9.798);
    } else if (key === 'hbn') {
      CONSTANTS.MATERIAL_NAME = 'Hexagonal Boron Nitride (White Graphene)';
      CONSTANTS.RHO_MAT = 2100.0;
      CONSTANTS.SIGMA_WORK = 26.0e9;
      CONSTANTS.SIGMA_ULT = 65.0e9;
      CONSTANTS.DESIGN_SF = 2.5;
      CONSTANTS.DEFAULT_CLIMB_SPEED = 50.0; // 180 km/h limited
      CONSTANTS.L_C = 26.0e9 / (2100.0 * 9.798);
    }
    return CONSTANTS;
  }

  function getActiveMaterial() {
    return {
      name: CONSTANTS.MATERIAL_NAME,
      densityKgM3: CONSTANTS.RHO_MAT,
      workingStressGPa: CONSTANTS.SIGMA_WORK / 1e9,
      ultimateStrengthGPa: CONSTANTS.SIGMA_ULT / 1e9,
      charLengthKm: CONSTANTS.L_C / 1000.0,
      cruiseSpeedKmh: CONSTANTS.DEFAULT_CLIMB_SPEED * 3.6
    };
  }

  const SpaceElevatorPhysics = {
    CONSTANTS,
    setMaterial,
    getActiveMaterial,
    gravity,
    centrifugal,
    effectiveGravity,
    tangentialSpeed,
    escapeVelocity,
    circularOrbitalVelocity,
    hyperbolicExcessEnergy,
    atmosphere,
    dynamicPressure,
    dragForce,
    taperRatio,
    taperArea,
    dynamicStress,
    coriolisDynamics,
    climberPower,
    nonEquatorialShear,
    orbitalParameters,
    integrateKinematics,
    computeState
  };

  return SpaceElevatorPhysics;
});
