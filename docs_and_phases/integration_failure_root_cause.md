# Root-Cause Diagnostics & Integration Failure Audit

**Date:** 2 November 2026  
**Document ID:** `docs/integration_failure_root_cause.md`  
**Status:** Root Cause Isolated & Resolution Engineered  

---

### 1. Executive Summary & Core Diagnostic Findings

The reason the user observed the "previous interface" upon visiting `http://127.0.0.1:8090/` has been definitively diagnosed:

1. **DOM Overlap & Occlusion:**
   - In `index.html`, the **old hardcoded DOM structures** were still physically present in the HTML `<body>`:
     - `<div id="search-box-container">...</div>` (the old top search bar)
     - `<div id="hud">...</div>` (the old left 14-row telemetry card)
     - `<div id="graphs-container">...</div>` (the old 2 small canvas panels on the top right)
     - `<div id="controls-panel">...</div>` (the old bottom-left transmission buttons)
     - `<div id="profile-container">...</div>` (the old vertical slider on the far right)
   - These legacy elements had `z-index: 20` to `30`, opaque dark backgrounds (`rgba(8, 14, 24, 0.92)`), and were hardcoded at fixed coordinates across all four corners of the viewport.
   - When `dashboard_ui.js` loaded and dynamically appended its `#se-hud-overlay` (`z-index: 50`), the old DOM elements and CSS rules were still active, causing a collision where the old DOM cards visually masked, overlapped, and conflicted with the new dashboard components!

2. **Web Server Process State:**
   - Port 8090 server task was cleanly terminated during the subagent system message restart, leaving the port closed or returning stale cached pages.

3. **Multi-File Path Drift:**
   - Edits were made across both `C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html` and `E:\Downloads\index.html`.
   - The authoritative project root must be strictly `C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\`, and `E:\Downloads\index.html` will be kept as an exact synchronized replica.

---

### 2. The Clean Engineering Solution

1. **Remove all legacy DOM elements and legacy CSS from `index.html`:**
   - Delete `#hud`, `#graphs-container`, `#controls-panel`, `#profile-container`, `#search-box-container`, and `#hint` from the HTML DOM and style blocks.
2. **Mount the new Cybernetic Dashboard as the native HTML structure:**
   - The entire futuristic UI (Top bar with 10 tabs, Left mission control, View modes, Simulation tools, Center 3D viewport, Right Canvas 2D graphs and heatmaps, Bottom 5 workspace decks, and Bottom dock bar) will be authored directly into the static HTML DOM of `index.html`.
3. **Preserve 100% of the authentic Three.js Scene & CAD Models:**
   - Ground Skyscraper: `international_space_elevator.glb` (crowned at $Y=0$)
   - Cargo Climber: `dm_space_day_1_-_space_elevator_(1).glb` (traveling the ribbon)
   - Apex Station: `day1_space_elevator.glb` (anchored at $Y=350$ / 100,000 km)
   - Earth Globe with Blue Marble satellite texture and normal vector pinning.
4. **Wire all controls, telemetry, and graphs to the central physics engine:**
   - Connect Play/Pause/Reset, speed warp (1x - 1000x), Google geocoding search, camera guidance locks, and real-time Chart updating at 60 FPS.
5. **Start the persistent server daemon on port 8090 and verify live.**
