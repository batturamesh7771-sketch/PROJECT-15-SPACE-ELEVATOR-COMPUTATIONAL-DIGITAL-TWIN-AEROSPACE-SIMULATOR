import os
import shutil

src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"
src_pe = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\physics_engine.js"
src_html = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
dst_html = r"E:\Downloads\index.html"

with open(src_js, "r", encoding="utf-8") as f:
    js_text = f.read()

# -----------------------------------------------------------------------------
# 1. Fix Pearson Cable Graph: Stress curve must be completely flat horizontal line
# -----------------------------------------------------------------------------
old_stress_loop = """    // Constant Working Stress Line / Slightly tapered stress curve (Orange)
    ctxTens.strokeStyle = '#f59e0b';
    ctxTens.lineWidth = 1.6;
    ctxTens.beginPath();
    for (let px = 20; px < w - 20; px++) {
      const frac = (px - 20) / (w - 40);
      const geoFrac = H_GEO / H_APEX;
      const stressGPa = 38.0 + 10.3 * Math.exp(-Math.pow((frac - geoFrac) / 0.28, 2));
      const py = h - 14 - (stressGPa / 50.0) * (h - 22);
      if (px === 20) ctxTens.moveTo(px, py); else ctxTens.lineTo(px, py);
    }
    ctxTens.stroke();"""

new_stress_loop = """    // Constant Working Stress Line (Orange: completely flat horizontal line for true Pearson constant-stress taper)
    ctxTens.strokeStyle = '#f59e0b';
    ctxTens.lineWidth = 1.8;
    ctxTens.beginPath();
    const constStressGPa = 45.0; // Strictly constant working stress across Pearson taper length
    const pyConst = h - 14 - (constStressGPa / 50.0) * (h - 22);
    ctxTens.moveTo(20, pyConst);
    ctxTens.lineTo(w - 20, pyConst);
    ctxTens.stroke();"""

if old_stress_loop in js_text:
    js_text = js_text.replace(old_stress_loop, new_stress_loop, 1)
    print("1. Fixed Pearson Cable Graph Stress to flat horizontal line")
else:
    print("Warning: old_stress_loop exact text not matched, attempting pattern replacement")
    import re
    js_text = re.sub(
        r'// Constant Working Stress Line[\s\S]*?ctxTens\.stroke\(\);',
        new_stress_loop,
        js_text,
        count=1
    )
    print("1. Replaced Pearson stress loop via regex")

# -----------------------------------------------------------------------------
# 2. Fix Orbital C3 Math: Update default/display to 26.74 km²/s² at 76,700 km
# -----------------------------------------------------------------------------
js_text = js_text.replace(
    'id="se-orb-c3-val">0.00 km²/s²',
    'id="se-orb-c3-val">26.74 km²/s²',
    1
)
js_text = js_text.replace(
    'id="se-orb-c3-val">49.44 km²/s²',
    'id="se-orb-c3-val">26.74 km²/s²',
    1
)
print("2. Fixed Orbital C3 Math initial value to 26.74 km²/s²")

# -----------------------------------------------------------------------------
# 3. Fix Ambient Temp Label: Change 'Ambient Temp' to 'Internal Temp' (+25 °C)
# -----------------------------------------------------------------------------
js_text = js_text.replace(
    '${ICONS.thermal}<span>Ambient Temp</span>',
    '${ICONS.thermal}<span>Internal Temp</span>',
    1
)
print("3. Fixed Ambient Temp label to Internal Temp (+25 °C)")

# -----------------------------------------------------------------------------
# 4. Fix Laser Physics: Change '87.5%' to '31.2%' in UI and efficiency math
# -----------------------------------------------------------------------------
js_text = js_text.replace(
    '<span class="se-t-val" id="se-t-eff">87.5%</span>',
    '<span class="se-t-val" id="se-t-eff">31.2%</span>',
    1
)
js_text = js_text.replace(
    '87.5% laser beaming efficiency',
    '31.2% laser beaming efficiency',
    1
)
# Update power denominator from 0.875 to 0.312
js_text = js_text.replace('/ 0.875', '/ 0.312')
print("4. Fixed Laser Physics efficiency from 87.5% to 31.2%")

# -----------------------------------------------------------------------------
# 5. Fix Gravity Graph Axis: Add '(Log Scale)' to title
# -----------------------------------------------------------------------------
js_text = js_text.replace(
    '<span class="se-graph-title">GRAVITY & CENTRIFUGAL FIELD</span>',
    '<span class="se-graph-title">GRAVITY & CENTRIFUGAL FIELD (Log Scale)</span>',
    1
)
print("5. Fixed Gravity Graph Axis title to include (Log Scale)")

with open(src_js, "w", encoding="utf-8") as f:
    f.write(js_text)
print("Saved updated dashboard_ui.js")

# Also update physics_engine.js nominal laser efficiency if present
with open(src_pe, "r", encoding="utf-8") as f:
    pe_text = f.read()

pe_text = pe_text.replace("EFFICIENCY_LASER: 0.875,", "EFFICIENCY_LASER: 0.312,")
pe_text = pe_text.replace("efficiency = 0.875", "efficiency = 0.312")

with open(src_pe, "w", encoding="utf-8") as f:
    f.write(pe_text)
print("Saved updated physics_engine.js")

# Synchronize E:\Downloads\index.html
if os.path.exists(os.path.dirname(dst_html)):
    shutil.copyfile(src_html, dst_html)
    print("Synchronized to E:\\Downloads\\index.html")
