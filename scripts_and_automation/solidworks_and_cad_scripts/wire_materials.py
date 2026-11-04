import os
import shutil

src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"
src_html = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
dst_html = r"E:\Downloads\index.html"

with open(src_js, "r", encoding="utf-8") as f:
    content = f.read()

target_update_mat = """  function updateMaterialCard(matKey) {
    const mat = MATERIALS[matKey] || MATERIALS['CNT'];
    document.getElementById('se-mat-uts').innerText = mat.uts;
    document.getElementById('se-mat-density').innerText = mat.density;
    document.getElementById('se-mat-mod').innerText = mat.modulus;
    document.getElementById('se-mat-tc').innerText = mat.thermalCond;
    document.getElementById('se-mat-viable').innerText = `✓ ${mat.viability}`;
    document.getElementById('se-deck-taper').innerText = mat.taperRatio;
  }"""

replacement_update_mat = """  function updateMaterialCard(matKey) {
    state.selectedMaterial = matKey;
    const mat = MATERIALS[matKey] || MATERIALS['CNT'];
    const elUts = document.getElementById('se-mat-uts');
    if (elUts) elUts.innerText = mat.uts;
    const elDen = document.getElementById('se-mat-density');
    if (elDen) elDen.innerText = mat.density;
    const elMod = document.getElementById('se-mat-mod');
    if (elMod) elMod.innerText = mat.modulus;
    const elTc = document.getElementById('se-mat-tc');
    if (elTc) elTc.innerText = mat.thermalCond;
    const elViable = document.getElementById('se-mat-viable');
    if (elViable) elViable.innerText = `✓ ${mat.viability}`;
    const elTaper = document.getElementById('se-deck-taper');
    if (elTaper) elTaper.innerText = mat.taperRatio;

    // Dynamically update Physics Engine material constants!
    if (window.SpaceElevatorPhysics && window.SpaceElevatorPhysics.CONSTANTS) {
      window.SpaceElevatorPhysics.CONSTANTS.SIGMA_ULT = mat.utsNum * 1e9;
      window.SpaceElevatorPhysics.CONSTANTS.RHO_CABLE = mat.densityNum;
      window.SpaceElevatorPhysics.CONSTANTS.SIGMA_WORK = (mat.utsNum * 1e9) / 2.0;
    }
  }"""

if target_update_mat in content:
    content = content.replace(target_update_mat, replacement_update_mat, 1)
    print("Replaced updateMaterialCard")

with open(src_js, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved dashboard_ui.js")

# Sync to E:\Downloads\index.html
if os.path.exists(os.path.dirname(dst_html)):
    shutil.copyfile(src_html, dst_html)
    print("Synchronized to E:\\Downloads\\index.html")
