import os, shutil

target_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(target_file, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update checkLoaded to dismiss overlay safely with a fallback timer
old_check_loaded = """    let loadedModels = 0;

    function checkLoaded() {

      loadedModels++;

      if (loadedModels >= 3) {

        const overlay = document.getElementById('loader-overlay');

        overlay.style.opacity = '0';

        setTimeout(() => overlay.style.display = 'none', 300);

      }

    }"""

new_check_loaded = """    let loadedModels = 0;
    function dismissLoader() {
      const overlay = document.getElementById('loader-overlay');
      if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => { if (overlay) overlay.style.display = 'none'; }, 400);
      }
    }

    function checkLoaded() {
      loadedModels++;
      if (loadedModels >= 2) {
        dismissLoader();
      }
    }

    // Safety timeout: dismiss loader after 2.5s maximum regardless of network/asset status
    setTimeout(dismissLoader, 2500);"""

if old_check_loaded in c:
    c = c.replace(old_check_loaded, new_check_loaded)
    print("Replaced old_check_loaded successfully!")
else:
    print("Warning: old_check_loaded exact string not matched, attempting regex/normalized replace")
    # let's find function checkLoaded()
    idx = c.find("function checkLoaded()")
    if idx != -1:
        # find matching bracket
        end_idx = c.find("}", idx)
        end_idx = c.find("}", end_idx + 1)
        start_idx = c.rfind("let loadedModels = 0;", 0, idx)
        c = c[:start_idx] + new_check_loaded + c[end_idx + 1:]
        print("Replaced checkLoaded via index range successfully!")

# 2. Fix groundElevatorToLatLng HUD updates
old_hud_block = """      // HUD updates

      document.getElementById('val-loc').innerText = locationName || "Custom Geo Coordinate";

      document.getElementById('val-coords').innerText = `${Math.abs(lat).toFixed(2)} ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lng).toFixed(2)} ${lng >= 0 ? 'E' : 'W'}`;



      // Nonequatorial stability penalty calculation

      const tiltAngle = Math.abs(lat) * 0.42;

      const penaltyEl = document.getElementById('val-penalty');

      if (Math.abs(lat) < 4.0) {

        penaltyEl.className = "val highlight-geo";

        penaltyEl.innerText = "0.0 Tilt (Ideal Equatorial Balance, 100% Efficiency)";

      } else if (Math.abs(lat) < 22.0) {

        penaltyEl.className = "val highlight-gold";

        penaltyEl.innerText = `${tiltAngle.toFixed(1)} Lateral Bending Shear (Guy-Wire Stabilized)`;

      } else {

        penaltyEl.className = "val highlight-alert";

        penaltyEl.innerText = `${tiltAngle.toFixed(1)} CRITICAL OFF-AXIS LOAD: High Restoring Torque!`;

      }"""

new_hud_block = """      // Safe HUD updates (forwarded to SpaceElevatorUI if available)
      const elLoc = document.getElementById('val-loc');
      if (elLoc) elLoc.innerText = locationName || "Custom Geo Coordinate";
      const elCoords = document.getElementById('val-coords');
      if (elCoords) elCoords.innerText = `${Math.abs(lat).toFixed(2)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lng).toFixed(2)}° ${lng >= 0 ? 'E' : 'W'}`;

      const tiltAngle = Math.abs(lat) * 0.42;
      const penaltyEl = document.getElementById('val-penalty');
      if (penaltyEl) {
        if (Math.abs(lat) < 4.0) {
          penaltyEl.className = "val highlight-geo";
          penaltyEl.innerText = "0.0° Tilt (Ideal Equatorial Balance, 100% Efficiency)";
        } else if (Math.abs(lat) < 22.0) {
          penaltyEl.className = "val highlight-gold";
          penaltyEl.innerText = `${tiltAngle.toFixed(1)}° Lateral Bending Shear (Guy-Wire Stabilized)`;
        } else {
          penaltyEl.className = "val highlight-alert";
          penaltyEl.innerText = `${tiltAngle.toFixed(1)}° CRITICAL OFF-AXIS LOAD: High Restoring Torque!`;
        }
      }"""

if old_hud_block in c:
    c = c.replace(old_hud_block, new_hud_block)
    print("Replaced old_hud_block successfully!")
else:
    # search around val-loc
    loc_idx = c.find("document.getElementById('val-loc')")
    if loc_idx != -1:
        start_b = c.rfind("// HUD updates", 0, loc_idx)
        # find end of penalty block
        end_b = c.find("groundElevatorToLatLng(0.0, -90.5", loc_idx)
        end_b = c.rfind("}", 0, end_b) + 1
        c = c[:start_b] + new_hud_block + "\n    }\n" + c[end_b:]
        print("Replaced HUD block via index range successfully!")

# 3. Fix pac-input Google Maps search input check
c = c.replace(
"""    const searchInput = document.getElementById('pac-input');

    if (window.google && google.maps && google.maps.places) {""",
"""    const searchInput = document.getElementById('pac-input');
    if (searchInput && window.google && google.maps && google.maps.places) {"""
)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(c)

print("Saved updated index.html!")

# Sync to E:\Downloads\index.html
shutil.copyfile(target_file, r'E:\Downloads\index.html')
print("Synced to E:\\Downloads\\index.html successfully!")
