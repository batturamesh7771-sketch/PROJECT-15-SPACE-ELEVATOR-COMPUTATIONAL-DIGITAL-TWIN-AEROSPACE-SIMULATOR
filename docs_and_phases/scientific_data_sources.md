# SCIENTIFIC DATA SOURCES & PHYSICAL CONSTANTS
## SPACE ELEVATOR COMPUTATIONAL DIGITAL TWIN
**Document Identifier:** SCI-SE-2026-REF-001  
**Authority:** Standards & Reference Model Specification  
**Classification:** Engineering Baseline Constants  

---

### 1. FUNDAMENTAL ASTRODYNAMICAL CONSTANTS

| Symbol | Parameter Description | Value (SI Units) | Standard Reference |
| :--- | :--- | :--- | :--- |
| $G$ | Newtonian Gravitational Constant | $6.67430 \times 10^{-11}\text{ m}^3/(\text{kg}\cdot\text{s}^2)$ | CODATA 2018 |
| $M_\oplus$ | Earth Mass | $5.972168 \times 10^{24}\text{ kg}$ | IAU / IERS Numerical Standards 2010 |
| $\mu_\oplus$ | Earth Standard Gravitational Parameter | $3.986004418 \times 10^{14}\text{ m}^3/\text{s}^2$ | WGS-84 / EGM96 Geodetic Model |
| $R_e$ | Earth Equatorial Radius | $6,378,137.0\text{ m}$ | WGS-84 Ellipsoid |
| $R_p$ | Earth Polar Radius | $6,356,752.3142\text{ m}$ | WGS-84 Ellipsoid |
| $f$ | Earth Geometric Flattening | $1 / 298.257223563$ | WGS-84 Ellipsoid |
| $\Omega_\oplus$ | Earth Sidereal Angular Velocity | $7.2921159 \times 10^{-5}\text{ rad/s}$ | IERS Standards ($2\pi / 86,164.0905\text{ s}$) |
| $r_{geo}$ | Geostationary Orbital Radius | $42,164,169.46\text{ m}$ | $(\mu / \Omega_\oplus^2)^{1/3}$ |
| $h_{geo}$ | Geostationary Altitude above Equator | $35,786,032.46\text{ m}$ | $r_{geo} - R_e$ |
| $g_0$ | Standard Surface Acceleration | $9.80665\text{ m/s}^2$ | ISO 80000-3 Standard Gravity |
| $g_{eq}$ | Equatorial Surface Inward Gravity | $9.798285\text{ m/s}^2$ | $\mu / R_e^2$ |

---

### 2. SOLAR SYSTEM & HELIOCENTRIC KINEMATIC CONSTANTS

| Parameter | Value | Reference Standard |
| :--- | :--- | :--- |
| Astronomical Unit ($1\text{ AU}$) | $149,597,870,700\text{ m}$ | IAU Resolution B2 (2012) |
| Solar Gravitational Parameter ($\mu_\odot$) | $1.32712440018 \times 10^{20}\text{ m}^3/\text{s}^2$ | IAU 2015 |
| Earth Orbital Period ($T_{sidereal}$) | $365.256363004\text{ days}$ ($31,558,149.8\text{ s}$) | IERS 2010 |
| Earth Mean Orbital Velocity ($v_{orb}$) | $29.78\text{ km/s}$ | JPL Planetary Ephemeris DE440 |
| Earth Orbital Eccentricity ($e$) | $0.0167086$ | JPL Planetary Ephemeris DE440 |
| Earth Axial Obliquity ($\epsilon$) | $23.4392911^\circ$ ($23^\circ 26' 21.4''$) | IAU 2006 Precession Model |
| Solar Constant ($S_0$ at $1\text{ AU}$) | $1361.2\text{ W/m}^2$ | ASTM E490 / SORCE Solar Irradiance |

---

### 3. ATMOSPHERIC, ENVIRONMENTAL & RADIATION STANDARDS

1. **U.S. Standard Atmosphere 1976 (NASA-TM-X-74335):**
   - Sea-level pressure: $P_0 = 101,325\text{ Pa}$
   - Sea-level temperature: $T_0 = 288.15\text{ K}$ ($+15^\circ\text{C}$)
   - Air gas constant: $R_{air} = 287.05287\text{ J}/(\text{kg}\cdot\text{K})$
   - Density scale height: $H_\rho \approx 8,500\text{ m}$ in the troposphere.
2. **Radiation Models (NASA SP-8000 Series / AP-8 & AE-8):**
   - Inner Van Allen Proton Belt: Peaks between $1,500\text{ km}$ and $5,000\text{ km}$ altitude ($E > 10\text{ MeV}$).
   - Outer Van Allen Electron Belt: Peaks between $15,000\text{ km}$ and $25,000\text{ km}$ altitude ($E > 1\text{ MeV}$).
3. **NASA Orbital Debris Engineering Model (ORDEM 3.1):**
   - Peak debris flux localized between $750\text{ km}$ and $1,000\text{ km}$ altitude (Sun-synchronous inclination bands).
