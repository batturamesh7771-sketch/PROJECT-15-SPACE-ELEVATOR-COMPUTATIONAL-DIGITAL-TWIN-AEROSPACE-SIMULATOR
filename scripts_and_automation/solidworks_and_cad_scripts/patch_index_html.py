import os, re

target_file = r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html'
with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Locate index for line: const canvasGrav = document.getElementById('graph-gravity');
start_idx = -1
for i, line in enumerate(lines):
    if "const canvasGrav = document.getElementById('graph-gravity');" in line:
        start_idx = i
        break

end_idx = -1
for i, line in enumerate(lines):
    if "function animate(currentTime) {" in line:
        end_idx = i
        break

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

if start_idx != -1 and end_idx != -1:
    replacement = """
    // =========================================================================
    // HIGH-TECH AEROSPACE CYBERNETIC DASHBOARD INITIALIZATION
    // =========================================================================
    function setCam(mode) {
      cameraMode = mode;
      const worldPos = new THREE.Vector3();
      if (mode === 'base' || mode === 'earth') {
        baseAnchorGroup.getWorldPosition(worldPos);
        controls.target.copy(worldPos.clone().add(new THREE.Vector3(0, 8, 0)));
        camera.position.copy(worldPos.clone().add(new THREE.Vector3(28, 18, 32)));
      } else if (mode === 'geo' || mode === 'station') {
        upperStationGroup.getWorldPosition(worldPos);
        controls.target.copy(worldPos);
        camera.position.copy(worldPos.clone().add(new THREE.Vector3(30, 20, 50)));
      } else if (mode === 'full') {
        controls.target.set(0, 0, 0);
        camera.position.set(0, 150, 550);
      } else if (mode === 'climber') {
        const climberWorld = new THREE.Vector3();
        climberNode.getWorldPosition(climberWorld);
        controls.target.copy(climberWorld);
        camera.position.copy(climberWorld.clone().add(new THREE.Vector3(15, 12, 20)));
      } else if (mode === 'tether') {
        const climberWorld = new THREE.Vector3();
        climberNode.getWorldPosition(climberWorld);
        controls.target.copy(climberWorld);
        camera.position.copy(climberWorld.clone().add(new THREE.Vector3(50, 15, 50)));
      } else if (mode === 'analysis') {
        controls.target.set(0, 175, 0);
        camera.position.set(200, 175, 200);
      }
    }

    if (window.SpaceElevatorUI) {
      SpaceElevatorUI.init({
        callbacks: {
          onPlayPause: (running) => {
            if (!running) {
              window._lastClimbDirection = climbDirection;
              climbDirection = 0;
            } else {
              climbDirection = window._lastClimbDirection || 1;
            }
          },
          onReset: () => {
            climbAltitudeKm = 0.0;
            simElapsedSec = 0;
            climbDirection = 0;
          },
          onSpeedChange: (speed) => {
            timeScale = speed;
          },
          onViewModeChange: (mode) => {
            setCam(mode);
          },
          onLocationChange: (lat, lng, name) => {
            groundElevatorToLatLng(lat, lng, name);
          }
        }
      });
    }

"""
    new_lines = lines[:start_idx] + [replacement] + lines[end_idx:]
    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Successfully patched index.html lines!")
