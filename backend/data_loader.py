# -*- coding: utf-8 -*-
"""
Space Elevator Project Context Loader
Feeds complete aerospace engineering specifications and operational envelopes
to the Multi-Agent Mixture of Experts (MoE) Decision-Making Bot.
"""

from typing import Dict, Any

SPACE_ELEVATOR_CONTEXT: Dict[str, Any] = {
    "project": {
        "name": "Project 14 - Earth Space Elevator Computational Digital Twin",
        "authority": "Autonomous Systems & Multiphysics Verification Directorate",
        "classification": "Advanced Aerospace Engineering Research",
        "simulation_endpoints": {
            "webgl_simulator": "http://127.0.0.1:8090/",
            "scientific_backend": "http://127.0.0.1:8095/"
        }
    },
    "geography_and_astrodynamics": {
        "base_station_name": "Galapagos Terrestrial Megatall Skyscraper Ground Anchor",
        "latitude_deg": 0.00,
        "longitude_deg": -90.00,
        "altitude_msl_m": 0.0,
        "earth_radius_equatorial_m": 6378137.0,
        "earth_mass_kg": 5.972168e24,
        "standard_gravitational_parameter_mu": 3.986004418e14,
        "earth_sidereal_rotation_rate_rad_s": 7.2921159e-5,
        "geostationary_orbit_radius_m": 42164169.46,
        "geostationary_orbit_altitude_km": 35786.03,
        "apex_station_altitude_km": 100000.0,
        "apex_station_geocentric_radius_km": 106378.14,
        "apex_station_counterweight_mass_mt": 5.21
    },
    "tether_specifications": {
        "total_length_km": 100000.0,
        "discretization_nodes": 1000,
        "segment_length_km": 100.0,
        "tether_geometry": "Pearson (1975) Exponential Constant-Stress Taper",
        "base_cross_sectional_area_m2": 1.0e-4,  # 1.0 cm^2
        "geo_cross_sectional_area_m2": 1.6295e-4,
        "apex_cross_sectional_area_m2": 0.937e-4,
        "taper_ratio_geo": 1.6295,
        "primary_material": "Carbon Nanotube (CNT) Macro-Yarn",
        "materials": {
            "cnt": {
                "name": "Carbon Nanotube (CNT) Macro-Yarn",
                "density_kg_m3": 1300.0,
                "ultimate_tensile_strength_gpa": 95.0,
                "design_working_stress_gpa": 47.5,
                "youngs_modulus_tpa": 1.2,
                "thermal_conductivity_w_mk": 3000.0,
                "characteristic_length_km": 3726.0,
                "taper_ratio": 1.63,
                "total_cable_mass_mt": 5.21,
                "viability": "Viable (Baseline)",
                "theme_color": "#38bdf8"
            },
            "graphene": {
                "name": "Graphene Monolayer Ribbon",
                "density_kg_m3": 2200.0,
                "ultimate_tensile_strength_gpa": 130.0,
                "design_working_stress_gpa": 65.0,
                "youngs_modulus_tpa": 1.0,
                "thermal_conductivity_w_mk": 5000.0,
                "characteristic_length_km": 3016.0,
                "taper_ratio": 2.12,
                "total_cable_mass_mt": 6.84,
                "viability": "High Performance",
                "theme_color": "#10b981"
            },
            "super_laminate": {
                "name": "Super-Laminate (CNT/PMR-15 Composite)",
                "density_kg_m3": 1800.0,
                "ultimate_tensile_strength_gpa": 75.0,
                "design_working_stress_gpa": 37.5,
                "youngs_modulus_tpa": 0.85,
                "thermal_conductivity_w_mk": 1200.0,
                "characteristic_length_km": 2126.0,
                "taper_ratio": 4.18,
                "total_cable_mass_mt": 11.45,
                "viability": "Industrial Manufacturable",
                "theme_color": "#f59e0b"
            },
            "hbn": {
                "name": "Hexagonal Boron Nitride (hBN Ceramic)",
                "density_kg_m3": 2100.0,
                "ultimate_tensile_strength_gpa": 65.0,
                "design_working_stress_gpa": 32.5,
                "youngs_modulus_tpa": 0.85,
                "thermal_conductivity_w_mk": 1700.0,
                "characteristic_length_km": 1458.0,
                "taper_ratio": 6.85,
                "total_cable_mass_mt": 18.32,
                "viability": "Radiation Hardened",
                "theme_color": "#c084fc"
            }
        }
    },
    "climber_and_propulsion": {
        "climber_tare_mass_kg": 6000.0,
        "payload_mass_kg": 14000.0,
        "total_climber_mass_kg": 20000.0,
        "nominal_cruising_speed_kmh": 450.0,
        "nominal_cruising_speed_ms": 125.0,
        "max_passenger_acceleration_ms2": 0.50,
        "traction_mechanism": "Dual-Axis Opposed Ceramic Pinch-Rollers",
        "power_beaming": {
            "ground_laser_wavelength_nm": 1064.0,
            "laser_wall_plug_efficiency": 0.60,
            "photovoltaic_receiver_efficiency": 0.52,
            "end_to_end_system_efficiency": 0.312,  # 31.2%
            "climber_motor_drive_efficiency": 0.94,
            "regenerative_braking_recovery_efficiency": 0.85
        }
    },
    "operational_constraints": {
        "min_allowable_safety_factor": 2.00,
        "warning_safety_factor_threshold": 2.05,
        "max_allowable_stress_gpa": 50.0,
        "warning_stress_threshold_gpa": 45.0,
        "coriolis_lateral_force_limit_n": 500.0,
        "passenger_internal_temp_nominal_c": 25.0,
        "passenger_internal_temp_max_c": 28.0,
        "passenger_internal_temp_min_c": 20.0
    },
    "space_environment_hazards": {
        "leo_orbital_debris_corridor_km": {"min": 200.0, "max": 1200.0, "peak_km": 800.0},
        "van_allen_inner_proton_belt_km": {"min": 1500.0, "max": 5000.0, "peak_dose_msv_h": 2.10},
        "van_allen_outer_electron_belt_km": {"min": 15000.0, "max": 25000.0, "peak_dose_msv_h": 0.85},
        "solar_constant_flux_wm2": 1361.2,
        "earth_eclipse_shadow_temp_c": -160.0,
        "direct_sun_equilibrium_temp_c": 120.0
    }
}

def get_project_context() -> Dict[str, Any]:
    """Returns the immutable master context specification for Project 14."""
    return SPACE_ELEVATOR_CONTEXT

def format_context_for_prompt() -> str:
    """Formats the engineering context as a concise reference block for LLM prompts."""
    c = SPACE_ELEVATOR_CONTEXT
    return (
        f"--- SPACE ELEVATOR MASTER ENGINEERING BASELINE ---\n"
        f"Length: {c['tether_specifications']['total_length_km']:,} km | Taper: Pearson 1975\n"
        f"Base Station: {c['geography_and_astrodynamics']['base_station_name']} ({c['geography_and_astrodynamics']['latitude_deg']}° Lat, {c['geography_and_astrodynamics']['longitude_deg']}° Lon)\n"
        f"GEO Altitude: {c['geography_and_astrodynamics']['geostationary_orbit_altitude_km']:,} km | Apex Mass: {c['geography_and_astrodynamics']['apex_station_counterweight_mass_mt']} Mt\n"
        f"Primary Material: Carbon Nanotube Macro-Yarn (UTS: 95 GPa, Density: 1,300 kg/m³, Modulus: 1.2 TPa)\n"
        f"Operational Safety Envelope: Min Safety Factor >= {c['operational_constraints']['min_allowable_safety_factor']:.2f} (Warning: < {c['operational_constraints']['warning_safety_factor_threshold']:.2f})\n"
        f"Max Axial Stress <= {c['operational_constraints']['max_allowable_stress_gpa']:.1f} GPa (Warning: > {c['operational_constraints']['warning_stress_threshold_gpa']:.1f} GPa)\n"
        f"Climber Mass: {c['climber_and_propulsion']['total_climber_mass_kg']:,} kg | Nominal Speed: {c['climber_and_propulsion']['nominal_cruising_speed_kmh']} km/h\n"
        f"Laser Beaming Efficiency: {c['climber_and_propulsion']['power_beaming']['end_to_end_system_efficiency']*100:.1f}%\n"
        f"Radiation Hazard Zones: Inner Proton Belt (1,500-5,000 km, 2.1 mSv/h), Outer Electron Belt (15,000-25,000 km, 0.85 mSv/h)\n"
        f"---------------------------------------------------"
    )
