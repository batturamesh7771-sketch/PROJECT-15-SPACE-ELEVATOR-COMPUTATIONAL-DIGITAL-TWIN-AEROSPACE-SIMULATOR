src_js = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"

with open(src_js, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('function updateMaterialCard')
idx_end = text.find('function handleTabSwitch', idx)

new_func = """function updateMaterialCard(matKey) {
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
    if (elViable) elViable.innerText = "✓ " + mat.viability;
    const elTaper = document.getElementById('se-deck-taper');
    if (elTaper) elTaper.innerText = mat.taperRatio;

    // Dynamically update Physics Engine material constants in real time!
    if (window.SpaceElevatorPhysics && window.SpaceElevatorPhysics.CONSTANTS) {
      window.SpaceElevatorPhysics.CONSTANTS.SIGMA_ULT = mat.utsNum * 1e9;
      window.SpaceElevatorPhysics.CONSTANTS.RHO_CABLE = mat.densityNum;
      window.SpaceElevatorPhysics.CONSTANTS.SIGMA_WORK = (mat.utsNum * 1e9) / 2.0;
    }
  }

  """

text = text[:idx] + new_func + text[idx_end:]

with open(src_js, "w", encoding="utf-8") as f:
    f.write(text)
print("Updated updateMaterialCard via index slicing!")
