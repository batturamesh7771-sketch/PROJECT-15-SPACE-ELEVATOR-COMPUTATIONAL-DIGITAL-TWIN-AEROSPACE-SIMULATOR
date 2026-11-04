/**
 * ==============================================================================================
 * SPACE ELEVATOR DIGITAL TWIN - ORBITAL DYNAMICS & INTERPLANETARY LAUNCH OPERATIONS ENGINE
 * ==============================================================================================
 * File: js/orbital_missions.js
 * Author: Lead Orbital Dynamics & Interplanetary Launch Operations Engineer
 *
 * Description:
 *   High-fidelity first-principles orbital mechanics and interplanetary trajectory calculation
 *   engine for equatorial space elevator payload release and interplanetary staging operations.
 *
 * Capabilities:
 *   1. Planetary Escape & Hyperbolic Excess Energy:
 *      - Computes local geocentric radius r, co-rotational tangential velocity v_tan,
 *        circular orbital speed v_circ, gravitational escape velocity v_esc, specific orbital
 *        energy epsilon, and hyperbolic excess energy C3 [km^2/s^2].
 *      - Rigorously classifies orbital flight regimes:
 *          * Sub-orbital Decay / Atmospheric Intersect (h < 35,786 km, r_p < R_e)
 *          * Sub-GEO Elliptical Orbit (apogee at release point, r_p >= R_e)
 *          * Geostationary Circular Zero-G Orbit (h ≈ 35,786 km, C3 < 0, e = 0)
 *          * Super-GEO Elliptical Orbit (h_geo < h < 46,956 km, perigee at release point)
 *          * Parabolic / Hyperbolic Planetary Escape (h >= 46,956 km, C3 >= 0)
 *          * Apex Counterweight Sling (h ≈ 100,000 km, C3 = +52.68 km^2/s^2)
 *
 *   2. Interplanetary Transfer Trajectories:
 *      - Models heliocentric transfer injection from equatorial apex/tether release.
 *      - Computes heliocentric departure injection velocity: v_helio = v_earth + v_inf.
 *      - Models transfer orbits to Mars, Asteroid Belt (Ceres), and Jupiter (plus Venus, Saturn).
 *      - Calculates delta-V, propellant mass fraction, and payload multipliers saved compared
 *        to conventional chemical rocket launches (e.g. 13 - 16 km/s delta-V eliminated!).
 *      - Calculates high-energy fast-transit trajectories (e.g. Mars transit reduced from 259 to ~99 days).
 *
 *   3. 2D / 3D Orbital Trajectory Rendering Point Generator:
 *      - Generates smooth point arrays for 2D Canvas and 3D WebGL (Three.js) orbital path visualization.
 *      - Automatically handles closed ellipses, circles, and open hyperbolic trajectories with asymptotes.
 *      - Provides native Three.js geometry and line helpers (`toThreeGeometry`, `toThreeLine`).
 *
 * Export:
 *   Exposed as `window.OrbitalMissions` (browser) and `module.exports` (Node.js/CommonJS).
 * ==============================================================================================
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.OrbitalMissions = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ============================================================================================
  // FUNDAMENTAL ASTRODYNAMICAL & PHYSICAL CONSTANTS (WGS84 & IAU/JPL HORIZONS)
  // ============================================================================================
  const CONSTANTS = Object.freeze({
    // Earth Physical Constants
    MU_EARTH: 3.986004418e14,          // Earth standard gravitational parameter [m^3/s^2]
    R_EARTH: 6378137.0,                // Earth equatorial radius [m] (WGS-84)
    OMEGA_EARTH: 7.2921159e-5,         // Earth sidereal angular rotation velocity [rad/s]
    R_GEO: 42164169.46,                // Geostationary orbit radius = (MU / OMEGA^2)^(1/3) [m]
    H_GEO: 35786032.46,                // Geostationary altitude above surface [m] (~35,786 km)
    R_ESCAPE: 53123598.0,              // Escape threshold radius = 2^(1/3) * R_GEO [m]
    H_ESCAPE: 46745461.0,              // Analytical escape threshold altitude [m] (~46,956 km nominal)
    H_ESCAPE_BENCHMARK_KM: 46956.0,    // Standard astrodynamics literature benchmark altitude [km]
    H_APEX: 100000000.0,               // Space elevator apex counterweight altitude [m] (100,000 km)
    G0: 9.80665,                       // Standard Earth surface acceleration of gravity [m/s^2]

    // Solar System & Heliocentric Constants
    MU_SUN: 1.32712440018e20,          // Sun gravitational parameter [m^3/s^2]
    AU_METERS: 1.495978707e11,         // Astronomical Unit [m]
    R_EARTH_ORBIT: 1.495978707e11,     // Earth mean heliocentric distance (1.0 AU) [m]
    V_EARTH_ORBIT: 29784.69,           // Earth mean heliocentric circular speed [m/s] (~29.78 km/s)

    // Three.js Simulator Visual Scale Reference
    SCENE_EARTH_RADIUS: 100.0,         // Three.js unit radius of Earth globe
    SCENE_TETHER_LENGTH: 350.0         // Three.js unit length of tether (representing 100,000 km)
  });

  // ============================================================================================
  // CELESTIAL TARGET CATALOG (INTERPLANETARY DESTINATIONS)
  // ============================================================================================
  const TARGET_BODIES = Object.freeze({
    mars: {
      id: 'mars',
      name: 'Mars',
      semiMajorAxisAU: 1.523679,
      semiMajorAxisMeters: 1.523679 * CONSTANTS.AU_METERS,
      eccentricity: 0.0934,
      radiusKm: 3389.5,
      massKg: 6.4171e23,
      orbitalPeriodDays: 686.98,
      direction: 'prograde',
      colorHex: 0xef4444,
      description: 'Primary human interplanetary destination and industrial colony.'
    },
    asteroid: {
      id: 'asteroid',
      name: 'Asteroid Belt (Ceres)',
      semiMajorAxisAU: 2.7675,
      semiMajorAxisMeters: 2.7675 * CONSTANTS.AU_METERS,
      eccentricity: 0.0758,
      radiusKm: 469.7,
      massKg: 9.393e20,
      orbitalPeriodDays: 1681.6,
      direction: 'prograde',
      colorHex: 0xf59e0b,
      description: 'Main Asteroid Belt resource extraction and raw materials hub.'
    },
    ceres: {
      id: 'ceres',
      name: 'Asteroid Belt (Ceres)',
      semiMajorAxisAU: 2.7675,
      semiMajorAxisMeters: 2.7675 * CONSTANTS.AU_METERS,
      eccentricity: 0.0758,
      radiusKm: 469.7,
      massKg: 9.393e20,
      orbitalPeriodDays: 1681.6,
      direction: 'prograde',
      colorHex: 0xf59e0b,
      description: 'Main Asteroid Belt resource extraction and raw materials hub.'
    },
    jupiter: {
      id: 'jupiter',
      name: 'Jupiter',
      semiMajorAxisAU: 5.2044,
      semiMajorAxisMeters: 5.2044 * CONSTANTS.AU_METERS,
      eccentricity: 0.0489,
      radiusKm: 69911.0,
      massKg: 1.8982e27,
      orbitalPeriodDays: 4332.59,
      direction: 'prograde',
      colorHex: 0xfbbf24,
      description: 'Outer solar system gas giant, Jovian moon systems, and Trojan gateways.'
    },
    venus: {
      id: 'venus',
      name: 'Venus',
      semiMajorAxisAU: 0.723332,
      semiMajorAxisMeters: 0.723332 * CONSTANTS.AU_METERS,
      eccentricity: 0.0067,
      radiusKm: 6051.8,
      massKg: 4.8675e24,
      orbitalPeriodDays: 224.70,
      direction: 'retrograde',
      colorHex: 0xf472b6,
      description: 'Inner solar system target requiring retrograde orbital launch shedding velocity.'
    },
    mercury: {
      id: 'mercury',
      name: 'Mercury',
      semiMajorAxisAU: 0.387098,
      semiMajorAxisMeters: 0.387098 * CONSTANTS.AU_METERS,
      eccentricity: 0.2056,
      radiusKm: 2439.7,
      massKg: 3.3011e23,
      orbitalPeriodDays: 87.97,
      direction: 'retrograde',
      colorHex: 0x94a3b8,
      description: 'Deep solar gravitational well target demanding large retrograde velocity depletion.'
    },
    saturn: {
      id: 'saturn',
      name: 'Saturn',
      semiMajorAxisAU: 9.5826,
      semiMajorAxisMeters: 9.5826 * CONSTANTS.AU_METERS,
      eccentricity: 0.0555,
      radiusKm: 58232.0,
      massKg: 5.6834e26,
      orbitalPeriodDays: 10759.22,
      direction: 'prograde',
      colorHex: 0xe2e8f0,
      description: 'Ringed world, Titan atmospheric exploration, and outer solar system frontier.'
    }
  });

  // ============================================================================================
  // SECTION 1: PLANETARY ESCAPE & HYPERBOLIC EXCESS ENERGY ENGINE
  // ============================================================================================

  /**
   * Calculates the instantaneous orbital state, velocities, specific orbital energy,
   * hyperbolic excess energy (C3), and resulting Keplerian trajectory for a payload
   * released from the space elevator tether at any given altitude and latitude.
   *
   * @param {number} altitudeMeters - Altitude above Earth surface [meters or km]
   * @param {number} [latitudeDeg=0.0] - Geodetic latitude of the ground anchor [degrees]
   * @returns {Object} Comprehensive orbital state telemetry object
   */
  function calculateReleaseState(altitudeMeters, latitudeDeg = 0.0) {
    let altM = Number(altitudeMeters);
    if (isNaN(altM) || altM < 0) altM = 0;

    // Gracefully auto-detect if user passed km instead of meters (e.g. altitude < 1500)
    if (altM > 0 && altM <= 1500.0) {
      altM *= 1000.0;
    }

    const latDeg = Number(latitudeDeg) || 0.0;
    const latRad = latDeg * (Math.PI / 180.0);
    const cosLat = Math.cos(latRad);

    // 1. Geocentric Radial Distances
    const r = CONSTANTS.R_EARTH + altM;                     // Geocentric radius [m]
    const r_axis = r * cosLat;                              // Distance from Earth rotation axis [m]

    // 2. Co-rotational Tangential Velocity (Earth Sidereal Frame)
    const v_tan = CONSTANTS.OMEGA_EARTH * r_axis;           // Tangential release velocity [m/s]

    // 3. Gravitational Field Velocities
    const v_circ = Math.sqrt(CONSTANTS.MU_EARTH / r);       // Local circular orbital velocity [m/s]
    const v_esc = Math.sqrt((2.0 * CONSTANTS.MU_EARTH) / r);// Local gravitational escape velocity [m/s]

    // 4. Specific Orbital Energy (epsilon) & Hyperbolic Excess Energy (C3)
    // epsilon = 0.5 * v^2 - mu / r [J/kg or m^2/s^2]
    const epsilon = 0.5 * Math.pow(v_tan, 2) - (CONSTANTS.MU_EARTH / r);

    // C3 = v_tan^2 - v_esc^2 = 2 * epsilon [km^2/s^2]
    const c3 = (Math.pow(v_tan, 2) - Math.pow(v_esc, 2)) / 1e6;

    // Hyperbolic Excess Velocity at Infinity (v_inf)
    const v_inf = c3 > 0 ? Math.sqrt(c3 * 1e6) : 0.0;       // [m/s]
    const v_inf_km_s = v_inf / 1000.0;                      // [km/s]

    // 5. Keplerian Orbital Elements Derivation
    const altKm = altM / 1000.0;
    const isAtGeo = Math.abs(altM - CONSTANTS.H_GEO) <= 250000.0; // +/- 250 km GEO tolerance window

    let orbitType = 'ellipse';
    let regime = '';
    let regimeKey = '';
    let a = 0.0;                                            // Semi-major axis [m]
    let e = 0.0;                                            // Eccentricity
    let p = 0.0;                                            // Semi-latus rectum [m]
    let periapsisRadius = 0.0;                              // Periapsis radius [m]
    let apoapsisRadius = 0.0;                               // Apoapsis radius [m]
    let periodSec = null;                                   // Orbital period [s]
    let intersectsEarth = false;
    let releasePointApsis = 'unknown';
    let asymptoteDeflectionDeg = null;
    let trueAnomalyAsymptoteRad = null;

    // Specific angular momentum: h_ang = r_axis * v_tan (for equatorial: r * v_tan)
    const h_ang = r_axis * v_tan;

    if (isAtGeo && Math.abs(latDeg) < 0.2) {
      // ----------------------------------------------------------------------------------------
      // REGIME: Geostationary Circular Orbit (GEO)
      // ----------------------------------------------------------------------------------------
      regimeKey = 'GEO_CIRCULAR';
      regime = 'Geostationary Circular Zero-G Orbit (GEO)';
      orbitType = 'circular';
      a = r;
      e = 0.0;
      p = r;
      periapsisRadius = r;
      apoapsisRadius = r;
      periodSec = (2.0 * Math.PI) / CONSTANTS.OMEGA_EARTH;   // 1 sidereal day (~86,164 s)
      releasePointApsis = 'circular';
    } else if (c3 < 0.0) {
      // ----------------------------------------------------------------------------------------
      // REGIME: Bound Elliptical Earth Orbits (Sub-GEO or Super-GEO)
      // ----------------------------------------------------------------------------------------
      orbitType = 'ellipse';
      // Vis-viva: 1/a = 2/r - v^2/mu
      const invA = (2.0 / r) - (Math.pow(v_tan, 2) / CONSTANTS.MU_EARTH);
      a = 1.0 / invA;

      // Eccentricity from angular momentum: e = sqrt(1 - h^2 / (mu * a))
      const eSq = Math.max(0.0, 1.0 - (Math.pow(h_ang, 2) / (CONSTANTS.MU_EARTH * a)));
      e = Math.sqrt(eSq);
      p = a * (1.0 - Math.pow(e, 2));

      if (v_tan < v_circ) {
        // Below GEO: Tangential speed is less than circular velocity.
        // Therefore, the release point is the APOGEE of the orbit!
        releasePointApsis = 'apogee';
        apoapsisRadius = r;
        periapsisRadius = Math.max(0.0, 2.0 * a - r);

        if (periapsisRadius < CONSTANTS.R_EARTH) {
          intersectsEarth = true;
          orbitType = 'suborbital';
          if (altM < 100000.0) {
            regimeKey = 'ATMOSPHERIC';
            regime = 'Troposphere / Sub-orbital Atmosphere';
          } else {
            regimeKey = 'SUBORBITAL_DECAY';
            regime = 'Sub-orbital Decay (Earth Intersecting)';
          }
        } else {
          regimeKey = 'SUB_GEO_ELLIPSE';
          regime = 'Sub-GEO Elliptical Earth Orbit';
        }
      } else {
        // Above GEO (but below escape): Tangential speed exceeds circular velocity.
        // Therefore, the release point is the PERIGEE of the orbit!
        releasePointApsis = 'perigee';
        periapsisRadius = r;
        apoapsisRadius = 2.0 * a - r;
        regimeKey = 'SUPER_GEO_ELLIPSE';
        regime = 'Super-GEO Elliptical Orbit (Deep Space Apogee)';
      }

      // Kepler's Third Law: T = 2 * pi * sqrt(a^3 / mu)
      periodSec = 2.0 * Math.PI * Math.sqrt(Math.pow(a, 3) / CONSTANTS.MU_EARTH);
    } else {
      // ----------------------------------------------------------------------------------------
      // REGIME: Parabolic / Hyperbolic Planetary Escape (h >= 46,956 km nominal)
      // ----------------------------------------------------------------------------------------
      orbitType = c3 === 0.0 ? 'parabola' : 'hyperbola';
      // For hyperbola: a is conventionally negative in celestial mechanics (epsilon > 0)
      a = -CONSTANTS.MU_EARTH / (2.0 * epsilon);

      // Eccentricity for hyperbola: e = sqrt(1 + 2*eps*h^2/mu^2) > 1.0
      e = Math.sqrt(1.0 + (2.0 * epsilon * Math.pow(h_ang, 2)) / Math.pow(CONSTANTS.MU_EARTH, 2));
      p = r * (1.0 + e); // At periapsis release

      releasePointApsis = 'periapsis';
      periapsisRadius = r;
      apoapsisRadius = Infinity;
      periodSec = null; // Unbounded trajectory

      // Hyperbolic asymptote geometry
      trueAnomalyAsymptoteRad = Math.acos(-1.0 / e);
      // Turning deflection angle: sin(delta/2) = 1/e
      asymptoteDeflectionDeg = (2.0 * Math.asin(1.0 / e)) * (180.0 / Math.PI);

      if (altKm >= 99000.0) {
        regimeKey = 'APEX_SLING';
        regime = 'Apex Counterweight Sling (Deep Space Direct)';
      } else if (altKm >= CONSTANTS.H_ESCAPE_BENCHMARK_KM || altM >= CONSTANTS.H_ESCAPE) {
        regimeKey = 'HYPERBOLIC_ESCAPE';
        regime = 'Hyperbolic Planetary Escape Trajectory';
      } else {
        regimeKey = 'ESCAPE_THRESHOLD';
        regime = 'Parabolic Earth Gravity Well Escape';
      }
    }

    return {
      altitudeMeters: altM,
      altitudeKm: altKm,
      latitudeDeg: latDeg,
      radiusMeters: r,
      radiusKm: r / 1000.0,
      radiusAxisMeters: r_axis,
      radiusAxisKm: r_axis / 1000.0,
      v_tan,
      v_tan_km_s: v_tan / 1000.0,
      v_circ,
      v_circ_km_s: v_circ / 1000.0,
      v_esc,
      v_esc_km_s: v_esc / 1000.0,
      epsilon,
      epsilon_MJ_kg: epsilon / 1e6,
      c3,
      v_inf,
      v_inf_km_s,
      regime,
      regimeKey,
      orbit: {
        type: orbitType,
        semiMajorAxis: a,
        semiMajorAxisKm: a / 1000.0,
        eccentricity: e,
        semiLatusRectum: p,
        periapsisRadius,
        periapsisAltitudeKm: (periapsisRadius - CONSTANTS.R_EARTH) / 1000.0,
        apoapsisRadius,
        apoapsisAltitudeKm: apoapsisRadius === Infinity ? Infinity : (apoapsisRadius - CONSTANTS.R_EARTH) / 1000.0,
        periodSec,
        periodHours: periodSec ? periodSec / 3600.0 : null,
        periodDays: periodSec ? periodSec / 86400.0 : null,
        intersectsEarth,
        releasePointApsis,
        asymptoteDeflectionDeg,
        trueAnomalyAsymptoteRad
      },
      constants: {
        muEarth: CONSTANTS.MU_EARTH,
        rEarth: CONSTANTS.R_EARTH,
        omegaEarth: CONSTANTS.OMEGA_EARTH,
        hGeoKm: CONSTANTS.H_GEO / 1000.0,
        hEscapeKm: CONSTANTS.H_ESCAPE / 1000.0,
        hEscapeBenchmarkKm: CONSTANTS.H_ESCAPE_BENCHMARK_KM,
        hApexKm: CONSTANTS.H_APEX / 1000.0
      }
    };
  }

  // ============================================================================================
  // SECTION 2: INTERPLANETARY TRANSFER TRAJECTORIES & MISSION OPTIMIZATION ENGINE
  // ============================================================================================

  /**
   * Resolves target celestial body descriptor from string ID, name, or custom object.
   *
   * @param {string|Object} target - Target ID ('mars', 'asteroid', 'jupiter', etc.) or object
   * @returns {Object} Target body specification object
   */
  function resolveTargetBody(target) {
    if (!target) return TARGET_BODIES.mars;
    if (typeof target === 'object') {
      const rM = target.semiMajorAxisMeters || (target.semiMajorAxisAU ? target.semiMajorAxisAU * CONSTANTS.AU_METERS : CONSTANTS.AU_METERS * 1.524);
      return {
        id: target.id || 'custom',
        name: target.name || 'Custom Target Body',
        semiMajorAxisAU: target.semiMajorAxisAU || (rM / CONSTANTS.AU_METERS),
        semiMajorAxisMeters: rM,
        eccentricity: target.eccentricity || 0.05,
        radiusKm: target.radiusKm || 3000.0,
        direction: target.direction || (rM >= CONSTANTS.R_EARTH_ORBIT ? 'prograde' : 'retrograde'),
        colorHex: target.colorHex || 0x38bdf8,
        description: target.description || 'User-defined celestial destination.'
      };
    }
    const key = String(target).trim().toLowerCase();
    return TARGET_BODIES[key] || TARGET_BODIES.mars;
  }

  /**
   * Models the complete interplanetary transfer injection from equatorial space elevator release,
   * comparing Hohmann minimum-energy transfers with actual high-energy direct-sling trajectories.
   * Quantifies delta-V, rocket propellant mass fraction, and payload multiplier savings vs. rockets.
   *
   * @param {string|Object} targetBody - Target destination ('mars', 'asteroid', 'jupiter', etc.)
   * @param {number} [releaseAlt=100000000.0] - Tether release altitude [meters or km] (default: Apex)
   * @returns {Object} Comprehensive interplanetary mission analysis and delta-V budget
   */
  function calculateHeliocentricTransfer(targetBody, releaseAlt = CONSTANTS.H_APEX) {
    const target = resolveTargetBody(targetBody);

    // Normalize release altitude
    let altM = Number(releaseAlt);
    if (isNaN(altM) || altM <= 0) altM = CONSTANTS.H_APEX;
    if (altM <= 1500.0) altM *= 1000.0; // Auto-detect km

    // Evaluate Space Elevator Geocentric Release State
    const releaseState = calculateReleaseState(altM, 0.0);
    const c3Provided = releaseState.c3;                     // [km^2/s^2]
    const vInfProvided = releaseState.v_inf_km_s;           // [km/s]

    // 1. Classical Heliocentric Hohmann Transfer Orbit to Target
    const rEarth = CONSTANTS.R_EARTH_ORBIT;                 // 1.0 AU [m]
    const rTarget = target.semiMajorAxisMeters;              // Target radius [m]
    const aHohmann = (rEarth + rTarget) / 2.0;               // Hohmann semi-major axis [m]
    const aHohmannAU = aHohmann / CONSTANTS.AU_METERS;

    // Required heliocentric departure velocity from Earth orbit (vis-viva around Sun):
    // v_dep = sqrt(mu_sun * (2/r_earth - 1/a_hohmann))
    const vDepHohmannMs = Math.sqrt(CONSTANTS.MU_SUN * ((2.0 / rEarth) - (1.0 / aHohmann)));
    const vDepHohmann = vDepHohmannMs / 1000.0;             // [km/s]

    // Required hyperbolic excess velocity (v_inf) from Earth:
    const vInfRequired = Math.abs(vDepHohmannMs - CONSTANTS.V_EARTH_ORBIT) / 1000.0; // [km/s]
    const c3Required = Math.pow(vInfRequired, 2);           // [km^2/s^2]

    // Hohmann Time of Flight: T_hohmann = pi * sqrt(a^3 / mu_sun)
    const tofHohmannSec = Math.PI * Math.sqrt(Math.pow(aHohmann, 3) / CONSTANTS.MU_SUN);
    const tofHohmannDays = tofHohmannSec / 86400.0;
    const tofHohmannYears = tofHohmannDays / 365.25;

    // Heliocentric arrival velocity at target orbit:
    const vArrHohmannMs = Math.sqrt(CONSTANTS.MU_SUN * ((2.0 / rTarget) - (1.0 / aHohmann)));
    const vArrHohmann = vArrHohmannMs / 1000.0;             // [km/s]
    const vTargetOrbitalMs = Math.sqrt(CONSTANTS.MU_SUN / rTarget);
    const vTargetOrbital = vTargetOrbitalMs / 1000.0;       // [km/s]
    const vInfArrival = Math.abs(vArrHohmannMs - vTargetOrbitalMs) / 1000.0; // [km/s]

    // 2. Space Elevator Actual Transfer Injection Performance
    // Heliocentric injection velocity from prograde (midnight) apex release:
    // v_helio = v_earth_orbital + v_hyperbolic_infinity
    const vHelioProvidedMs = CONSTANTS.V_EARTH_ORBIT + (vInfProvided * 1000.0);
    const vHelioProvided = vHelioProvidedMs / 1000.0;       // [km/s]

    // Space elevator post-release burn required:
    let burnRequiredKmS = 0.0;
    let isDirectInjection = false;

    if (c3Provided >= c3Required) {
      // The elevator provides sufficient or excess energy for direct target insertion with ZERO burn!
      burnRequiredKmS = 0.0;
      isDirectInjection = true;
    } else {
      // Deficit in hyperbolic excess velocity must be made up via propulsive delta-V:
      burnRequiredKmS = Math.max(0.0, vInfRequired - vInfProvided);
      isDirectInjection = false;
    }

    // Actual heliocentric orbit achieved by elevator injection (if unassisted):
    let actualA_AU = null;
    let actualPerihelionAU = 1.0;
    let actualAphelionAU = null;
    let actualEccentricity = null;
    let fastTransitDays = null;
    let fastTransitSavingsDays = null;

    if (vInfProvided > 0) {
      // 1/a = 2/r - v^2/mu
      const invAActual = (2.0 / rEarth) - (Math.pow(vHelioProvidedMs, 2) / CONSTANTS.MU_SUN);
      if (invAActual > 0) {
        const aActualM = 1.0 / invAActual;
        actualA_AU = aActualM / CONSTANTS.AU_METERS;
        const aphelionM = 2.0 * aActualM - rEarth;
        actualAphelionAU = aphelionM / CONSTANTS.AU_METERS;
        actualEccentricity = (actualAphelionAU - actualPerihelionAU) / (actualAphelionAU + actualPerihelionAU);

        // Fast transit time evaluation to target (if actual aphelion >= target distance)
        if (actualAphelionAU >= target.semiMajorAxisAU) {
          // True anomaly at target orbit intersection: r = p / (1 + e * cos(theta))
          const pM = aActualM * (1.0 - Math.pow(actualEccentricity, 2));
          const cosThetaTarget = (pM / rTarget - 1.0) / actualEccentricity;
          if (Math.abs(cosThetaTarget) <= 1.0) {
            const thetaTarget = Math.acos(cosThetaTarget);
            // Eccentric anomaly: tan(E/2) = sqrt((1-e)/(1+e)) * tan(theta/2)
            const tanHalfE = Math.sqrt((1.0 - actualEccentricity) / (1.0 + actualEccentricity)) * Math.tan(thetaTarget / 2.0);
            const ETarget = 2.0 * Math.atan(tanHalfE);
            // Kepler's equation: M = E - e * sin(E)
            const MTarget = ETarget - actualEccentricity * Math.sin(ETarget);
            // Orbital period of the high-energy transfer ellipse:
            const periodSec = 2.0 * Math.PI * Math.sqrt(Math.pow(aActualM, 3) / CONSTANTS.MU_SUN);
            fastTransitDays = (MTarget / (2.0 * Math.PI)) * (periodSec / 86400.0);
            fastTransitSavingsDays = Math.max(0.0, tofHohmannDays - fastTransitDays);
          }
        }
      } else {
        // Hyperbolic escape from Solar System (Galactic Escape)
        actualA_AU = Infinity;
        actualAphelionAU = Infinity;
        actualEccentricity = 1.0 + Math.abs(invAActual);
      }
    }

    // 3. Conventional Chemical Rocket Baseline Comparison (From Earth Ground to Target)
    // Stage 1: Earth Surface to 200 km Circular LEO
    // Typical real-world launch delta-V breakdown:
    // v_leo_ideal (7,784 m/s) + gravity losses (1,200 m/s) + aero drag (350 m/s) + steering (66 m/s) = ~9,400 m/s
    const deltaVToLEO = 9.400;                              // [km/s]
    const rLEO = CONSTANTS.R_EARTH + 200000.0;              // 200 km LEO radius [m]
    const vCircLEO = Math.sqrt(CONSTANTS.MU_EARTH / rLEO) / 1000.0; // 7.784 km/s
    const vEscLEO = Math.sqrt((2.0 * CONSTANTS.MU_EARTH) / rLEO) / 1000.0; // 11.019 km/s

    // Stage 2: Trans-Planetary Injection Burn from LEO (TMI / TJI):
    // v_inj = sqrt(v_esc^2 + C3)
    const vInjLEO = Math.sqrt(Math.pow(vEscLEO, 2) + c3Required);
    const deltaVInjLEO = vInjLEO - vCircLEO;                // [km/s]
    const totalDeltaVRocket = deltaVToLEO + deltaVInjLEO;   // [km/s]

    // Delta-V Savings Achieved by Space Elevator:
    const deltaVSaved = totalDeltaVRocket - burnRequiredKmS;
    const deltaVSavingsPercent = (deltaVSaved / totalDeltaVRocket) * 100.0;

    // Tsiolkovsky Rocket Equation Fuel Mass Ratios:
    // m_0 / m_f = exp(Delta-V / (I_sp * g_0))
    // Methalox: Isp = 380 s, v_exhaust = 3.727 km/s
    const ispMethalox = 380.0;
    const vExhaustMethalox = (ispMethalox * CONSTANTS.G0) / 1000.0; // 3.727 km/s
    const massRatioRocketMethalox = Math.exp(totalDeltaVRocket / vExhaustMethalox);
    const fuelMassFractionRocket = 1.0 - (1.0 / massRatioRocketMethalox);

    // Hydrolox (Deep Space Upper Stage): Isp = 450 s, v_exhaust = 4.413 km/s
    const ispHydrolox = 450.0;
    const vExhaustHydrolox = (ispHydrolox * CONSTANTS.G0) / 1000.0;
    const massRatioRocketHydrolox = Math.exp(totalDeltaVRocket / vExhaustHydrolox);

    // Payload Multiplier: Elevator launches 100% dry payload with electric traction!
    // Conventional rocket can only deliver 1 / mass_ratio of launch pad mass as payload!
    const payloadMultiplier = massRatioRocketMethalox;

    return {
      target: {
        id: target.id,
        name: target.name,
        distanceAU: target.semiMajorAxisAU,
        distanceMeters: rTarget,
        orbitalSpeedKmS: vTargetOrbital,
        description: target.description
      },
      releaseState: {
        altitudeMeters: altM,
        altitudeKm: releaseState.altitudeKm,
        regime: releaseState.regime,
        c3Provided: c3Provided,
        vInfProvided: vInfProvided,
        vTanKmS: releaseState.v_tan_km_s,
        vEscKmS: releaseState.v_esc_km_s
      },
      hohmannTransfer: {
        semiMajorAxisAU: aHohmannAU,
        departureVelocityHelioKmS: vDepHohmann,
        departureVInfKmS: vInfRequired,
        departureC3: c3Required,
        arrivalVelocityHelioKmS: vArrHohmann,
        arrivalVInfKmS: vInfArrival,
        timeOfFlightDays: tofHohmannDays,
        timeOfFlightYears: tofHohmannYears
      },
      spaceElevatorInjection: {
        releaseAltitudeKm: releaseState.altitudeKm,
        c3Provided: c3Provided,
        vInfProvided: vInfProvided,
        vHelioInjectionKmS: vHelioProvided,
        burnRequiredKmS: burnRequiredKmS,
        isDirectInjection: isDirectInjection,
        actualOrbit: {
          semiMajorAxisAU: actualA_AU,
          perihelionAU: actualPerihelionAU,
          aphelionAU: actualAphelionAU,
          eccentricity: actualEccentricity,
          fastTransitDays: fastTransitDays,
          fastTransitSavingsDays: fastTransitSavingsDays
        }
      },
      conventionalRocketComparison: {
        leoAltitudeKm: 200.0,
        deltaVToLEOKmS: deltaVToLEO,
        deltaVInjectionLEOKmS: deltaVInjLEO,
        totalDeltaVRocketKmS: totalDeltaVRocket,
        deltaVElevatorBurnKmS: burnRequiredKmS,
        deltaVSavedKmS: deltaVSaved,
        deltaVSavingsPercent: deltaVSavingsPercent,
        fuelMassRatioMethalox: massRatioRocketMethalox,
        fuelMassFractionRocket: fuelMassFractionRocket,
        fuelMassRatioHydrolox: massRatioRocketHydrolox,
        payloadMultiplier: payloadMultiplier
      },
      summary: `Interplanetary transfer to ${target.name} from space elevator release at ${releaseState.altitudeKm.toLocaleString()} km:\n` +
        `• Space Elevator C3 provided: ${c3Provided.toFixed(2)} km²/s² (v_inf = ${vInfProvided.toFixed(3)} km/s)\n` +
        `• Target required C3: ${c3Required.toFixed(2)} km²/s² (v_inf = ${vInfRequired.toFixed(3)} km/s)\n` +
        `• Post-release chemical burn required: ${burnRequiredKmS.toFixed(3)} km/s (${isDirectInjection ? 'DIRECT ZERO-BURN INJECTION' : 'Deep-space trim burn'})\n` +
        `• Conventional Earth launch Delta-V: ${totalDeltaVRocket.toFixed(2)} km/s (Methalox fuel mass fraction: ${(fuelMassFractionRocket * 100).toFixed(1)}%)\n` +
        `• Delta-V saved: ${deltaVSaved.toFixed(2)} km/s (${deltaVSavingsPercent.toFixed(1)}% reduction!)\n` +
        (fastTransitDays ? `• High-energy fast transit time: ${fastTransitDays.toFixed(1)} days (${fastTransitSavingsDays.toFixed(1)} days faster than standard Hohmann!)` : `• Hohmann transit time: ${tofHohmannDays.toFixed(1)} days (${tofHohmannYears.toFixed(2)} years)`)
    };
  }

  /**
   * Calculates the optimal tether release altitude required for a 100% zero-burn,
   * propellantless Hohmann transfer injection to any specified celestial target.
   *
   * @param {string|Object} targetBody - Celestial target
   * @returns {Object} Optimal altitude telemetry
   */
  function getOptimalReleaseAltitude(targetBody) {
    const target = resolveTargetBody(targetBody);
    const rEarth = CONSTANTS.R_EARTH_ORBIT;
    const rTarget = target.semiMajorAxisMeters;
    const aHohmann = (rEarth + rTarget) / 2.0;

    const vDepHohmannMs = Math.sqrt(CONSTANTS.MU_SUN * ((2.0 / rEarth) - (1.0 / aHohmann)));
    const vInfReqMs = Math.abs(vDepHohmannMs - CONSTANTS.V_EARTH_ORBIT);
    const c3Req = Math.pow(vInfReqMs / 1000.0, 2);

    // Binary search along tether altitude from escape threshold (46,745 km) to 150,000 km
    let lowAlt = CONSTANTS.H_ESCAPE;
    let highAlt = 150000000.0;

    for (let iter = 0; iter < 45; iter++) {
      const mid = (lowAlt + highAlt) / 2.0;
      const state = calculateReleaseState(mid, 0.0);
      if (state.c3 < c3Req) {
        lowAlt = mid;
      } else {
        highAlt = mid;
      }
    }

    const optimalAltM = (lowAlt + highAlt) / 2.0;
    const optimalState = calculateReleaseState(optimalAltM, 0.0);

    return {
      targetName: target.name,
      targetDistanceAU: target.semiMajorAxisAU,
      requiredC3: c3Req,
      optimalAltitudeMeters: optimalAltM,
      optimalAltitudeKm: optimalAltM / 1000.0,
      tangentialVelocityKmS: optimalState.v_tan_km_s,
      escapeVelocityKmS: optimalState.v_esc_km_s,
      c3Achieved: optimalState.c3,
      isBeyondApex: optimalAltM > CONSTANTS.H_APEX
    };
  }

  // ============================================================================================
  // SECTION 3: 2D & 3D ORBITAL TRAJECTORY RENDERING POINT GENERATOR
  // ============================================================================================

  /**
   * Generates a high-resolution array of points representing the released Keplerian orbital
   * trajectory in 2D and 3D space, ready for Canvas 2D and WebGL / Three.js visualization.
   *
   * @param {number} altitudeMeters - Release altitude [meters or km]
   * @param {Object} [options={}] - Configuration options
   * @param {number} [options.latitudeDeg=0.0] - Anchor latitude [degrees]
   * @param {number} [options.numPoints=360] - Number of points to sample
   * @param {string|number} [options.scale='physical'] - 'physical' (meters), 'km', 'scene' (Three.js units), or numeric
   * @param {string} [options.plane='XZ'] - 'XZ' (equatorial plane when Y is Earth polar axis) or 'XY' (2D Cartesian)
   * @param {number} [options.maxDistanceMeters] - Cutoff distance for open hyperbolas [meters]
   * @param {boolean} [options.suborbitalClip=false] - Whether to clip subterranean points below Earth surface
   * @returns {Object} Trajectory point cloud dataset with apsides and Three.js helpers
   */
  function generateOrbitPoints(altitudeMeters, options = {}) {
    let altM = Number(altitudeMeters);
    if (isNaN(altM) || altM < 0) altM = 0;
    if (altM > 0 && altM <= 1500.0) altM *= 1000.0; // Auto-detect km

    const latDeg = options.latitudeDeg !== undefined ? Number(options.latitudeDeg) : 0.0;
    const numPoints = Math.max(24, options.numPoints || (altM >= CONSTANTS.H_ESCAPE ? 240 : 360));
    const plane = (options.plane || 'XZ').toUpperCase();

    // Scale calculation:
    // 'physical': 1.0 (meters)
    // 'km': 0.001
    // 'scene': scaled to Three.js simulator dimensions (Earth radius = 100.0, Apex = 450.0)
    let scaleFactor = 1.0;
    if (options.scale === 'scene') {
      scaleFactor = CONSTANTS.SCENE_EARTH_RADIUS / CONSTANTS.R_EARTH; // ~1.567856e-5
    } else if (options.scale === 'km') {
      scaleFactor = 1e-3;
    } else if (typeof options.scale === 'number' && options.scale > 0) {
      scaleFactor = options.scale;
    }

    // Evaluate release state
    const state = calculateReleaseState(altM, latDeg);
    const orbit = state.orbit;
    const r0 = state.radiusMeters;
    const e = orbit.eccentricity;
    const p = orbit.semiLatusRectum;

    const points = [];
    const points2D = [];
    const points3D = [];

    // Helper to project polar coordinates (r, theta) into 2D and 3D
    function addPoint(rMeters, thetaRad, isSubsurface = false) {
      const rScaled = rMeters * scaleFactor;
      const cosT = Math.cos(thetaRad);
      const sinT = Math.sin(thetaRad);

      let x2D = rScaled * cosT;
      let y2D = rScaled * sinT;

      let x3D = 0, y3D = 0, z3D = 0;
      if (plane === 'XZ') {
        // Standard WebGL convention: Y is Earth polar axis, X-Z is equatorial plane
        x3D = rScaled * cosT;
        y3D = 0; // Equatorial
        z3D = rScaled * sinT;
      } else {
        // Standard XY Cartesian plane
        x3D = rScaled * cosT;
        y3D = rScaled * sinT;
        z3D = 0;
      }

      // Vis-viva velocity at this radius:
      const invA = (2.0 / rMeters) - (orbit.type === 'hyperbola' ? -CONSTANTS.MU_EARTH / (2.0 * state.epsilon) : 1.0 / orbit.semiMajorAxis);
      const vInstMs = Math.sqrt(Math.max(0, CONSTANTS.MU_EARTH * invA));

      const pt = {
        x: x3D,
        y: y3D,
        z: z3D,
        x2D,
        y2D,
        radiusMeters: rMeters,
        radiusScaled: rScaled,
        thetaRad,
        thetaDeg: thetaRad * (180.0 / Math.PI),
        velocityKmS: vInstMs / 1000.0,
        subsurface: isSubsurface
      };

      points.push(pt);
      points2D.push({ x: x2D, y: y2D });
      points3D.push({ x: x3D, y: y3D, z: z3D });
    }

    if (orbit.type === 'circular') {
      // ----------------------------------------------------------------------------------------
      // CIRCULAR ORBIT (GEO)
      // ----------------------------------------------------------------------------------------
      for (let i = 0; i <= numPoints; i++) {
        const theta = (i / numPoints) * 2.0 * Math.PI;
        addPoint(r0, theta, false);
      }
    } else if (orbit.type === 'ellipse' || orbit.type === 'suborbital') {
      // ----------------------------------------------------------------------------------------
      // BOUND ELLIPTICAL ORBITS
      // ----------------------------------------------------------------------------------------
      // If released below GEO, release point is APOGEE (theta = 0 relative to release).
      // If released above GEO, release point is PERIGEE (theta = 0 relative to release).
      const thetaPeriapsisOffset = orbit.releasePointApsis === 'apogee' ? Math.PI : 0.0;

      for (let i = 0; i <= numPoints; i++) {
        const theta = (i / numPoints) * 2.0 * Math.PI;
        // Keplerian conic equation: r = p / (1 + e * cos(theta - theta_p))
        const rTrue = p / (1.0 + e * Math.cos(theta - thetaPeriapsisOffset));
        const isSub = rTrue < CONSTANTS.R_EARTH;

        if (options.suborbitalClip && isSub) {
          continue; // Skip underground segment if requested
        }
        addPoint(rTrue, theta, isSub);
      }
    } else {
      // ----------------------------------------------------------------------------------------
      // OPEN HYPERBOLIC / PARABOLIC ESCAPE TRAJECTORIES
      // ----------------------------------------------------------------------------------------
      // Periapsis is at release point (theta = 0).
      // Asymptote angle: theta_inf = acos(-1 / e)
      const thetaInf = orbit.trueAnomalyAsymptoteRad || Math.acos(-1.0 / e);
      // Cut off sampling just before asymptote divergence:
      const maxTheta = thetaInf * 0.94;

      for (let i = 0; i <= numPoints; i++) {
        const alpha = (i / numPoints) * 2.0 - 1.0; // Sample from -1.0 to +1.0
        const theta = alpha * maxTheta;
        const rTrue = p / (1.0 + e * Math.cos(theta));

        // Cutoff distance check (if specified)
        if (options.maxDistanceMeters && rTrue > options.maxDistanceMeters) {
          continue;
        }

        addPoint(rTrue, theta, false);
      }
    }

    // Apsides coordinates in 3D:
    const periapsisPt = {
      radiusMeters: orbit.periapsisRadius,
      radiusScaled: orbit.periapsisRadius * scaleFactor,
      altitudeKm: orbit.periapsisAltitudeKm,
      x: plane === 'XZ' ? orbit.periapsisRadius * scaleFactor : orbit.periapsisRadius * scaleFactor,
      y: 0,
      z: 0
    };

    const apoapsisPt = orbit.apoapsisRadius === Infinity ? null : {
      radiusMeters: orbit.apoapsisRadius,
      radiusScaled: orbit.apoapsisRadius * scaleFactor,
      altitudeKm: orbit.apoapsisAltitudeKm,
      x: plane === 'XZ' ? -orbit.apoapsisRadius * scaleFactor : -orbit.apoapsisRadius * scaleFactor,
      y: 0,
      z: 0
    };

    const releasePointPt = points.length > 0 ? points[0] : null;

    return {
      altitudeMeters: altM,
      altitudeKm: state.altitudeKm,
      orbitType: orbit.type,
      regime: state.regime,
      eccentricity: e,
      semiMajorAxisKm: orbit.semiMajorAxisKm,
      periapsis: periapsisPt,
      apoapsis: apoapsisPt,
      releasePoint: releasePointPt,
      scaleFactor,
      numPoints: points.length,
      points,
      points2D,
      points3D,

      /**
       * Instantiates a native Three.js BufferGeometry from the trajectory point cloud.
       * @param {Object} [threeInstance] - Optional THREE object (defaults to window.THREE)
       * @returns {THREE.BufferGeometry|null}
       */
      toThreeGeometry: function (threeInstance) {
        const T = threeInstance || (typeof window !== 'undefined' ? window.THREE : null);
        if (!T) {
          console.warn('[OrbitalMissions] THREE.js is not available in global scope.');
          return null;
        }
        const positions = new Float32Array(points3D.length * 3);
        for (let i = 0; i < points3D.length; i++) {
          positions[i * 3 + 0] = points3D[i].x;
          positions[i * 3 + 1] = points3D[i].y;
          positions[i * 3 + 2] = points3D[i].z;
        }
        const geo = new T.BufferGeometry();
        geo.setAttribute('position', new T.BufferAttribute(positions, 3));
        return geo;
      },

      /**
       * Constructs a rendered Three.js Line object with auto-tuned neon orbital colors.
       * @param {Object} [threeInstance] - THREE object
       * @param {Object} [materialOptions] - Custom Three.js LineBasicMaterial options
       * @returns {THREE.Line|null}
       */
      toThreeLine: function (threeInstance, materialOptions = {}) {
        const T = threeInstance || (typeof window !== 'undefined' ? window.THREE : null);
        if (!T) return null;
        const geo = this.toThreeGeometry(T);
        if (!geo) return null;

        let lineColor = 0x38bdf8; // Cyan default
        if (orbit.type === 'circular') lineColor = 0x4ade80;        // Neon green (GEO)
        else if (orbit.type === 'suborbital') lineColor = 0xf87171;  // Red alert (re-entry)
        else if (orbit.type === 'hyperbola') lineColor = 0xfbbf24;   // Gold (escape)

        const mat = new T.LineBasicMaterial(Object.assign({
          color: lineColor,
          linewidth: 2,
          transparent: true,
          opacity: 0.85
        }, materialOptions));

        const line = new T.Line(geo, mat);
        line.name = `OrbitPath_${orbit.type}_${state.altitudeKm.toFixed(0)}km`;
        return line;
      }
    };
  }

  /**
   * Generates heliocentric transfer visualization points from Earth (1.0 AU)
   * to any target planet (e.g. Mars, Ceres, Jupiter) for Sun-centered orbital diagrams.
   *
   * @param {string|Object} targetBody - Target destination
   * @param {number} [releaseAlt=100000000.0] - Space elevator altitude
   * @param {Object} [options={}] - Options (numPoints, scaleAU)
   * @returns {Object} Heliocentric transfer point cloud dataset
   */
  function generateHeliocentricPoints(targetBody, releaseAlt = CONSTANTS.H_APEX, options = {}) {
    const transfer = calculateHeliocentricTransfer(targetBody, releaseAlt);
    const numPoints = Math.max(36, options.numPoints || 180);
    const scaleAU = options.scaleAU || 100.0; // Default: 1 AU = 100 units

    const rEarthAU = 1.0;
    const rTargetAU = transfer.target.distanceAU;
    const aTransferAU = transfer.hohmannTransfer.semiMajorAxisAU;
    const eTransfer = Math.abs(rTargetAU - rEarthAU) / (rTargetAU + rEarthAU);
    const pAU = aTransferAU * (1.0 - Math.pow(eTransfer, 2));

    const earthOrbitPoints = [];
    const targetOrbitPoints = [];
    const transferArcPoints = [];

    // 1. Earth Orbit (1.0 AU Circle)
    for (let i = 0; i <= numPoints; i++) {
      const theta = (i / numPoints) * 2.0 * Math.PI;
      earthOrbitPoints.push({
        x: rEarthAU * scaleAU * Math.cos(theta),
        y: 0,
        z: rEarthAU * scaleAU * Math.sin(theta)
      });
    }

    // 2. Target Orbit Circle
    for (let i = 0; i <= numPoints; i++) {
      const theta = (i / numPoints) * 2.0 * Math.PI;
      targetOrbitPoints.push({
        x: rTargetAU * scaleAU * Math.cos(theta),
        y: 0,
        z: rTargetAU * scaleAU * Math.sin(theta)
      });
    }

    // 3. Transfer Arc from Earth Departure to Target Arrival (0 to PI)
    for (let i = 0; i <= numPoints; i++) {
      const theta = (i / numPoints) * Math.PI; // Departure at 0, arrival at PI
      const rAU = pAU / (1.0 + eTransfer * Math.cos(theta));
      transferArcPoints.push({
        x: rAU * scaleAU * Math.cos(theta),
        y: 0,
        z: rAU * scaleAU * Math.sin(theta)
      });
    }

    return {
      target: transfer.target,
      scaleAU,
      earthOrbitPoints,
      targetOrbitPoints,
      transferArcPoints,
      transfer
    };
  }

  // ============================================================================================
  // SECTION 4: MISSION REPORT & TELEMETRY FORMATTER
  // ============================================================================================

  /**
   * Formats a complete interplanetary mission plan as an executive telemetry report.
   *
   * @param {Object} transferPlan - Output from calculateHeliocentricTransfer
   * @returns {string} Formatted text report
   */
  function formatMissionReport(transferPlan) {
    if (!transferPlan || !transferPlan.target) return 'No mission data available.';
    const t = transferPlan;
    const r = t.conventionalRocketComparison;
    const s = t.spaceElevatorInjection;
    const h = t.hohmannTransfer;

    return [
      `================================================================================`,
      ` SPACE ELEVATOR INTERPLANETARY MISSION ANALYSIS: ${t.target.name.toUpperCase()}`,
      `================================================================================`,
      `Target Distance:            ${t.target.distanceAU.toFixed(4)} AU (${(t.target.distanceMeters / 1e9).toFixed(1)} million km)`,
      `Space Elevator Release Alt: ${t.releaseState.altitudeKm.toLocaleString()} km (${t.releaseState.regime})`,
      `--------------------------------------------------------------------------------`,
      `1. ORBITAL LAUNCH DYNAMICS (EARTH DEPARTURE):`,
      `   • Co-rotational Tangential Speed:  ${t.releaseState.vTanKmS.toFixed(3)} km/s`,
      `   • Local Escape Velocity:           ${t.releaseState.vEscKmS.toFixed(3)} km/s`,
      `   • Hyperbolic Excess Energy (C3):   ${s.c3Provided >= 0 ? '+' : ''}${s.c3Provided.toFixed(2)} km²/s²`,
      `   • Hyperbolic Excess Velocity:      ${s.vInfProvided.toFixed(3)} km/s`,
      `   • Heliocentric Injection Speed:    ${s.vHelioInjectionKmS.toFixed(3)} km/s (Earth prograde)`,
      `--------------------------------------------------------------------------------`,
      `2. HOHMANN TRANSFER PROFILE TO ${t.target.name.toUpperCase()}:`,
      `   • Required Departure C3:           ${h.departureC3.toFixed(2)} km²/s²`,
      `   • Required Departure v_inf:        ${h.departureVInfKmS.toFixed(3)} km/s`,
      `   • Standard Hohmann Transit Time:   ${h.timeOfFlightDays.toFixed(1)} days (${h.timeOfFlightYears.toFixed(2)} years)`,
      `   • Target Arrival Velocity:         ${h.arrivalVelocityHelioKmS.toFixed(3)} km/s`,
      `   • Target Relative Excess v_inf:    ${h.arrivalVInfKmS.toFixed(3)} km/s`,
      `--------------------------------------------------------------------------------`,
      `3. SPACE ELEVATOR ADVANTAGES & DELTA-V SAVINGS:`,
      `   • Post-Release Burn Required:      ${s.burnRequiredKmS.toFixed(3)} km/s (${s.isDirectInjection ? 'DIRECT PROPULSIONLESS INJECTION' : 'Deep-space trim'})`,
      `   • Conventional Chemical Launch:    ${r.totalDeltaVRocketKmS.toFixed(2)} km/s total Delta-V`,
      `     - Surface to 200 km LEO:         ${r.deltaVToLEOKmS.toFixed(2)} km/s (gravity/drag losses included)`,
      `     - LEO Trans-Injection Burn:      ${r.deltaVInjectionLEOKmS.toFixed(2)} km/s`,
      `   • Delta-V Saved by Elevator:       ${r.deltaVSavedKmS.toFixed(2)} km/s (${r.deltaVSavingsPercent.toFixed(1)}% SAVINGS!)`,
      `   • Conventional Rocket Mass Ratio:  ${r.fuelMassRatioMethalox.toFixed(1)} : 1 (Methalox propellant mass fraction: ${(r.fuelMassFractionRocket * 100).toFixed(1)}%)`,
      `   • Payload Mass Multiplier:         ${r.payloadMultiplier.toFixed(1)}x more useful payload delivered per ton!`,
      s.actualOrbit.fastTransitDays ?
      `   • High-Energy Fast Transit:        ${s.actualOrbit.fastTransitDays.toFixed(1)} days (${s.actualOrbit.fastTransitSavingsDays.toFixed(1)} days shaved off transit!)` : '',
      `================================================================================`
    ].filter(Boolean).join('\n');
  }

  // ============================================================================================
  // PUBLIC API EXPORT OBJECT
  // ============================================================================================
  const OrbitalMissions = {
    // Physical Constants and Celestial Catalog
    CONSTANTS,
    TARGET_BODIES,

    // Core Required Functions
    calculateReleaseState,
    calculateHeliocentricTransfer,
    generateOrbitPoints,

    // Advanced Operational Extensions
    generateHeliocentricPoints,
    getOptimalReleaseAltitude,
    resolveTargetBody,
    formatMissionReport
  };

  return OrbitalMissions;
}));
