import os
import shutil

src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"

with open(src_js, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Card 3 (Orbital & Mission Analysis) HTML with proper IDs
old_card3 = """<!-- Card 3: Orbital & Mission Analysis -->
        <div class="se-deck-card">
          <div class="se-card-header">
            <span class="se-card-title">ORBITAL & MISSION ANALYSIS</span>
          </div>
          <div class="se-orbit-body">
            <canvas id="se-orbit-canvas" width="90" height="96"></canvas>
            <div class="se-orbit-metrics">
              <div class="se-mat-row"><span style="color:var(--se-text-muted);">Δv to Escape</span></div>
              <div class="se-mat-row"><span class="se-t-val cyan">3.21 km/s</span></div>
              <div class="se-mat-row"><span style="color:var(--se-text-muted);">Transfer to Mars</span></div>
              <div class="se-mat-row"><span class="se-t-val cyan">5.98 km/s</span></div>
              <div class="se-mat-row"><span style="color:var(--se-text-muted);">C₃ (Current)</span></div>
              <div class="se-mat-row"><span class="se-t-val gold">49.44 km²/s²</span></div>
              <div class="se-orbit-link" id="se-btn-view-orbit">View Trajectory →</div>
            </div>
          </div>
        </div>"""

new_card3 = """<!-- Card 3: Orbital & Mission Analysis (LIVE COMPUTED FROM ORBITAL_MISSIONS.JS) -->
        <div class="se-deck-card">
          <div class="se-card-header">
            <span class="se-card-title">ORBITAL & MISSION ANALYSIS</span>
          </div>
          <div class="se-orbit-body">
            <canvas id="se-orbit-canvas" width="90" height="96"></canvas>
            <div class="se-orbit-metrics">
              <div class="se-mat-row"><span style="color:var(--se-text-muted);">Δv to Escape</span></div>
              <div class="se-mat-row"><span class="se-t-val cyan" id="se-orb-escape-val">3.21 km/s</span></div>
              <div class="se-mat-row"><span style="color:var(--se-text-muted);">Transfer to Mars</span></div>
              <div class="se-mat-row"><span class="se-t-val cyan" id="se-orb-mars-val">5.98 km/s</span></div>
              <div class="se-mat-row"><span style="color:var(--se-text-muted);">C₃ (Current)</span></div>
              <div class="se-mat-row"><span class="se-t-val gold" id="se-orb-c3-val">0.00 km²/s²</span></div>
              <div class="se-orbit-link" id="se-btn-view-orbit">View Trajectory →</div>
            </div>
          </div>
        </div>"""

content = content.replace(old_card3, new_card3, 1)

# 2. Update Card 4 (Environment & Risk) HTML with proper IDs
old_card4 = """<!-- Card 4: Environment & Risk -->
        <div class="se-deck-card">
          <div class="se-card-header">
            <span class="se-card-title">ENVIRONMENT & RISK</span>
          </div>
          <div class="se-env-grid">
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.solar}<span>Solar Flux</span></div>
              <span class="se-env-val">1,361 W/m²</span>
            </div>
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.debris}<span>Debris Flux</span></div>
              <span class="se-env-val">2.3e-6 /m²/s</span>
            </div>
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.thermal}<span>Temp (GEO)</span></div>
              <span class="se-env-val">+120 °C</span>
            </div>
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.radiation}<span>Radiation</span></div>
              <span class="se-env-val">2.1 mSv/yr</span>
            </div>
          </div>
          <div class="se-risk-badge">● Low Risk</div>
        </div>"""

new_card4 = """<!-- Card 4: Environment & Risk (LIVE COMPUTED FROM MATERIALS_ENVIRONMENT.JS) -->
        <div class="se-deck-card">
          <div class="se-card-header">
            <span class="se-card-title">ENVIRONMENT & RISK</span>
          </div>
          <div class="se-env-grid">
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.solar}<span>Solar Flux</span></div>
              <span class="se-env-val" id="se-env-solar-val">1,361 W/m²</span>
            </div>
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.debris}<span>Debris Flux</span></div>
              <span class="se-env-val" id="se-env-debris-val">2.3e-6 /m²/yr</span>
            </div>
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.thermal}<span>Ambient Temp</span></div>
              <span class="se-env-val" id="se-env-temp-val">+25 °C</span>
            </div>
            <div class="se-env-tile">
              <div class="se-env-tile-header">${ICONS.radiation}<span>Radiation Dose</span></div>
              <span class="se-env-val" id="se-env-rad-val">0.05 mSv/h</span>
            </div>
          </div>
          <div class="se-risk-badge" id="se-risk-badge">● Nominal (Low Risk)</div>
        </div>"""

content = content.replace(old_card4, new_card4, 1)

with open(src_js, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Card 3 & Card 4 HTML with IDs in dashboard_ui.js")
