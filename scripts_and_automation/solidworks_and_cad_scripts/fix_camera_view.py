import os
import shutil
import re

src_html = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
dst_html = r"E:\Downloads\index.html"

with open(src_html, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update initial cameraMode to 'full'
content = content.replace("let cameraMode = 'climber';", "let cameraMode = 'full';", 1)

# 2. Add setCam('full') right before SpaceElevatorUI.init call
target_init = "if (window.SpaceElevatorUI) {\n      SpaceElevatorUI.init({"
replace_init = "// Initialize default camera perspective to Full System View\n    setCam('full');\n\n    if (window.SpaceElevatorUI) {\n      SpaceElevatorUI.init({"
if target_init in content:
    content = content.replace(target_init, replace_init, 1)

# 3. Guard climber tracking in animate loop so camera never collapses
old_track = """      if (cameraMode === 'climber') {

        const climberWorld = new THREE.Vector3();

        climberNode.getWorldPosition(climberWorld);

        controls.target.lerp(climberWorld, 0.1);

        camera.position.add(climberWorld.clone().sub(controls.target).multiplyScalar(0.1));

      }"""

new_track = """      if (cameraMode === 'climber') {
        const climberWorld = new THREE.Vector3();
        climberNode.getWorldPosition(climberWorld);
        if (climberWorld.lengthSq() > 10.0) {
          controls.target.lerp(climberWorld, 0.08);
          const camOffset = camera.position.clone().sub(controls.target);
          if (camOffset.length() < 5.0 || camOffset.length() > 250.0) {
            camOffset.set(15, 12, 20);
          }
          camera.position.copy(controls.target.clone().add(camOffset));
        }
      }"""

if old_track in content:
    content = content.replace(old_track, new_track, 1)

with open(src_html, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated", src_html)

if os.path.exists(os.path.dirname(dst_html)):
    shutil.copyfile(src_html, dst_html)
    print("Synchronized to", dst_html)
