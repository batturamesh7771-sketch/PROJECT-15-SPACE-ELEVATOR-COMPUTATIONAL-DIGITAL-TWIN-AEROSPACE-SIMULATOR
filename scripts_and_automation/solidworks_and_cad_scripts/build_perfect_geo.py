import os
import sys
import math
import win32com.client
import pythoncom

def build_geo_system():
    pythoncom.CoInitialize()
    print("[1/6] Connecting to SolidWorks COM API...")
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.Visible = True
    sw.UserControl = True
    sw.SetUserPreferenceToggle(10, False) # swInputDimValOnCreate = False
    sw.SetUserPreferenceIntegerValue(192, 1) # Plain White Background

    part_tpl = sw.GetUserPreferenceStringValue(8)
    assy_tpl = sw.GetUserPreferenceStringValue(9)
    print("      Part Template:", part_tpl)
    print("      Assy Template:", assy_tpl)

    base_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
    parts_geo_dir = os.path.join(base_dir, "Parts_GEO")
    assy_dir = os.path.join(base_dir, "Assemblies")
    step_dir = os.path.join(base_dir, "ANSYS_Exports_STEP")
    render_dir = os.path.join(base_dir, "Investor_Renders")
    renders_main = os.path.join(base_dir, "Renders")

    for d in [parts_geo_dir, assy_dir, step_dir, render_dir, renders_main]:
        os.makedirs(d, exist_ok=True)

    def set_appearance(doc, r, g, b, ambient=0.7, diffuse=0.85, specular=0.7, shininess=0.6, transparency=0.0):
        try:
            # 9 doubles: R, G, B, Ambient, Diffuse, Specular, Shininess, Transparency, Emission
            vals = [r/255.0, g/255.0, b/255.0, ambient, diffuse, specular, shininess, transparency, 0.0]
            doc.MaterialPropertyValues = vals
        except Exception as e:
            print(f"      Notice on appearance: {e}")

    def save_and_close(doc, name, out_dir=parts_geo_dir):
        doc.ClearSelection2(True)
        doc.ForceRebuild3(False)
        doc.ShowNamedView2("*Isometric", 7)
        doc.ViewZoomtofit2()

        prt_path = os.path.join(out_dir, name + ".SLDPRT")
        stp_path = os.path.join(step_dir, name + ".STEP")
        png_path = os.path.join(render_dir, name + ".PNG")

        doc.SaveAs3(prt_path, 0, 2)
        doc.SaveAs3(stp_path, 0, 2)
        doc.SaveAs3(png_path, 0, 2)
        title = doc.GetTitle
        sw.CloseDoc(title)
        print(f"      Saved: {name} (.SLDPRT, .STEP, .PNG)")

    # =========================================================================
    # REBUILD MODULE 4: GEO_04_Geodesic_Biosphere_Spheres.SLDPRT
    # 4 Solid Spheres (Dia = 26m) centered at R = 50m on the 4 spokes (+X, -X, +Z, -Z)
    # with Equatorial Exo-Skeleton Structural Rings
    # =========================================================================
    print("[2/6] Building high-fidelity GEO_04_Geodesic_Biosphere_Spheres...")
    doc4 = sw.NewDocument(part_tpl, 0, 0.0, 0.0)
    sk4 = doc4.SketchManager
    ft4 = doc4.FeatureManager

    # We revolve 4 solid spheres directly:
    # Sphere 1 (+X at 50, 0, 0)
    doc4.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk4.InsertSketch(True)
    sk4.CreateCenterLine(50.0, -25.0, 0.0, 50.0, 25.0, 0.0)
    sk4.CreateArc(50.0, 0.0, 0.0, 50.0, -13.0, 0.0, 50.0, 13.0, 0.0, 1)
    sk4.CreateLine(50.0, 13.0, 0.0, 50.0, -13.0, 0.0)
    sk4.InsertSketch(True)
    ft4.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 2*math.pi, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True)

    # Sphere 2 (-X at -50, 0, 0)
    doc4.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk4.InsertSketch(True)
    sk4.CreateCenterLine(-50.0, -25.0, 0.0, -50.0, 25.0, 0.0)
    sk4.CreateArc(-50.0, 0.0, 0.0, -50.0, 13.0, 0.0, -50.0, -13.0, 0.0, 1)
    sk4.CreateLine(-50.0, -13.0, 0.0, -50.0, 13.0, 0.0)
    sk4.InsertSketch(True)
    ft4.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 2*math.pi, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True)

    # Sphere 3 (+Z at 0, 0, 50) - sketched on Right Plane (YZ plane)
    doc4.Extension.SelectByID2("Right Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk4.InsertSketch(True)
    sk4.CreateCenterLine(50.0, -25.0, 0.0, 50.0, 25.0, 0.0)
    sk4.CreateArc(50.0, 0.0, 0.0, 50.0, -13.0, 0.0, 50.0, 13.0, 0.0, 1)
    sk4.CreateLine(50.0, 13.0, 0.0, 50.0, -13.0, 0.0)
    sk4.InsertSketch(True)
    ft4.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 2*math.pi, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True)

    # Sphere 4 (-Z at 0, 0, -50) - sketched on Right Plane (YZ plane)
    doc4.Extension.SelectByID2("Right Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk4.InsertSketch(True)
    sk4.CreateCenterLine(-50.0, -25.0, 0.0, -50.0, 25.0, 0.0)
    sk4.CreateArc(-50.0, 0.0, 0.0, -50.0, 13.0, 0.0, -50.0, -13.0, 0.0, 1)
    sk4.CreateLine(-50.0, -13.0, 0.0, -50.0, 13.0, 0.0)
    sk4.InsertSketch(True)
    ft4.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 2*math.pi, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True)

    # Equatorial Exo-Skeleton Spaceframe Rings on all 4 spheres
    doc4.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk4.InsertSketch(True)
    for cx, cz in [(50.0, 0.0), (-50.0, 0.0), (0.0, 50.0), (0.0, -50.0)]:
        doc4.CreateCircleByRadius2(cx, cz, 0.0, 13.8)
        doc4.CreateCircleByRadius2(cx, cz, 0.0, 13.0)
    sk4.InsertSketch(True)
    ft4.FeatureExtrusion2(True, False, False, 0, 0, 0.75, 0.75, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    set_appearance(doc4, 140, 205, 235, ambient=0.6, diffuse=0.9, specular=0.95, shininess=0.85, transparency=0.45) # Translucent Silica Glass
    save_and_close(doc4, "GEO_04_Geodesic_Biosphere_Spheres")

    # =========================================================================
    # REBUILD MODULE 5: GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT
    # 6 Radial Photovoltaic Wings at 60 deg intervals (Sketchfab Reference Design)
    # =========================================================================
    print("[3/6] Building 6-Wing Radial Array GEO_05_Mega_Solar_Photovoltaic_Wings...")
    doc5 = sw.NewDocument(part_tpl, 0, 0.0, 0.0)
    sk5 = doc5.SketchManager
    ft5 = doc5.FeatureManager

    # Central structural ring hub (OD = 22m, ID = 18m, height = 3.0m)
    doc5.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk5.InsertSketch(True)
    doc5.CreateCircleByRadius2(0.0, 0.0, 0.0, 11.0)
    doc5.CreateCircleByRadius2(0.0, 0.0, 0.0, 9.0)
    sk5.InsertSketch(True)
    ft5.FeatureExtrusion2(True, False, False, 0, 0, 1.5, 1.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    # 6 Radial Solar Array Wings: radiating at 0, 60, 120, 180, 240, 300 degrees
    # Each wing: length = 85m (R: 11m to 96m), chord = 16m, thickness = 0.35m
    doc5.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk5.InsertSketch(True)
    for i in range(6):
        deg = i * 60.0
        rad = math.radians(deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        # Perpendicular unit vector
        px = -sin_a
        pz = cos_a

        # 4 corners of rectangular wing from R=12 to R=95, half-width = 8.0m
        r1, r2, hw = 12.0, 95.0, 8.0
        c1x = r1 * cos_a - hw * px
        c1z = r1 * sin_a - hw * pz
        c2x = r2 * cos_a - hw * px
        c2z = r2 * sin_a - hw * pz
        c3x = r2 * cos_a + hw * px
        c3z = r2 * sin_a + hw * pz
        c4x = r1 * cos_a + hw * px
        c4z = r1 * sin_a + hw * pz

        sk5.CreateLine(c1x, c1z, 0.0, c2x, c2z, 0.0)
        sk5.CreateLine(c2x, c2z, 0.0, c3x, c3z, 0.0)
        sk5.CreateLine(c3x, c3z, 0.0, c4x, c4z, 0.0)
        sk5.CreateLine(c4x, c4z, 0.0, c1x, c1z, 0.0)

    sk5.InsertSketch(True)
    ft5.FeatureExtrusion2(True, False, False, 0, 0, 0.175, 0.175, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    # 6 Central Structural Reinforcement Booms (truss spines)
    doc5.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sk5.InsertSketch(True)
    for i in range(6):
        deg = i * 60.0
        rad = math.radians(deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        px = -sin_a
        pz = cos_a

        r1, r2, hw = 11.0, 95.0, 0.9
        c1x = r1 * cos_a - hw * px
        c1z = r1 * sin_a - hw * pz
        c2x = r2 * cos_a - hw * px
        c2z = r2 * sin_a - hw * pz
        c3x = r2 * cos_a + hw * px
        c3z = r2 * sin_a + hw * pz
        c4x = r1 * cos_a + hw * px
        c4z = r1 * sin_a + hw * pz

        sk5.CreateLine(c1x, c1z, 0.0, c2x, c2z, 0.0)
        sk5.CreateLine(c2x, c2z, 0.0, c3x, c3z, 0.0)
        sk5.CreateLine(c3x, c3z, 0.0, c4x, c4z, 0.0)
        sk5.CreateLine(c4x, c4z, 0.0, c1x, c1z, 0.0)

    sk5.InsertSketch(True)
    ft5.FeatureExtrusion2(True, False, False, 0, 0, 0.5, 0.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)

    set_appearance(doc5, 15, 30, 85, ambient=0.7, diffuse=0.95, specular=0.98, shininess=0.95, transparency=0.0) # Deep Photovoltaic Sapphire Blue
    save_and_close(doc5, "GEO_05_Mega_Solar_Photovoltaic_Wings")

    # =========================================================================
    # REBUILD MASTER ASSEMBLY 04: 04_GEO_Orbital_Terminal_Station.SLDASM
    # =========================================================================
    print("[4/6] Preloading all 7 GEO modules into SolidWorks memory...")
    geo_parts = [
        "GEO_01_Central_Transit_Core.SLDPRT",
        "GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT",
        "GEO_03_Structural_Spoke_Corridors.SLDPRT",
        "GEO_04_Geodesic_Biosphere_Spheres.SLDPRT",
        "GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT",
        "GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT",
        "GEO_07_Continuous_Tether_Ribbon.SLDPRT"
    ]
    loaded_docs = {}
    for pf in geo_parts:
        pp = os.path.join(parts_geo_dir, pf)
        err = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warn = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        pdoc = sw.OpenDoc6(pp, 1, 1, "", err, warn)
        loaded_docs[pf] = pdoc
        print(f"      Loaded in RAM: {pf}")

    print("[5/6] Assembling 04_GEO_Orbital_Terminal_Station.SLDASM...")
    assy = sw.NewDocument(assy_tpl, 0, 0.0, 0.0)
    if not assy:
        print("ERROR: Could not create assembly!")
        return

    # Add components cleanly via AddComponent4
    # 1. Central Transit Core at origin (0, 0, 0)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_01_Central_Transit_Core.SLDPRT"), "", 0.0, 0.0, 0.0)
    # 2. Pressurized Torus Hab Ring at origin (0, 0, 0)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT"), "", 0.0, 0.0, 0.0)
    # 3. Structural Spoke Corridors at origin (0, 0, 0)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_03_Structural_Spoke_Corridors.SLDPRT"), "", 0.0, 0.0, 0.0)
    # 4. Geodesic Biosphere Spheres at origin (0, 0, 0)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_04_Geodesic_Biosphere_Spheres.SLDPRT"), "", 0.0, 0.0, 0.0)
    # 5. Mega Solar Photovoltaic Wings at Upper Guideway Bulkhead (Y = +75.0m)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT"), "", 0.0, 75.0, 0.0)
    # 6. Communications Spire and RCS Mast at Core Top (Y = 0.0m)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT"), "", 0.0, 0.0, 0.0)
    # 7. Continuous 400m Graphene Tether passing through origin (0, 0, 0)
    assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_07_Continuous_Tether_Ribbon.SLDPRT"), "", 0.0, 0.0, 0.0)

    # Force rebuild, clear selections, set isometric view & zoom to fit
    assy.ClearSelection2(True)
    assy.ForceRebuild3(False)
    assy.ShowNamedView2("*Isometric", 7)
    assy.ViewZoomtofit2()

    master_assy_path = os.path.join(assy_dir, "04_GEO_Orbital_Terminal_Station.SLDASM")
    step_export_path = os.path.join(step_dir, "GEO_Orbital_Terminal_Station_Complete.STEP")
    render_img_path = os.path.join(render_dir, "GEO_Orbital_Terminal_Station_Isometric.PNG")

    assy.SaveAs3(master_assy_path, 0, 2)
    assy.SaveAs3(step_export_path, 0, 2)
    assy.SaveAs3(render_img_path, 0, 2)
    print(f"      Saved: {master_assy_path}")
    print(f"      Exported STEP: {step_export_path}")
    print(f"      Saved High-Res Render: {render_img_path}")

    # =========================================================================
    # REBUILD MASTER SHOWCASE ASSEMBLY: 00_Space_Elevator_Master_Showcase.SLDASM
    # Multi-tier vertical spacing so assemblies never collide or collapse!
    # Earth Port (Y=0m) -> Climber (Y=60m) -> GEO Terminal (Y=180m) -> Apex (Y=320m)
    # =========================================================================
    print("[6/6] Updating 00_Space_Elevator_Master_Showcase.SLDASM with decoupled vertical tiers...")
    sub01 = os.path.join(assy_dir, "01_Earth_Port_Platform.SLDASM")
    sub02 = os.path.join(assy_dir, "02_Tether_Climber_20T.SLDASM")
    sub03 = os.path.join(assy_dir, "03_Tether_And_Apex_Hub.SLDASM")
    sub04 = master_assy_path

    # Preload assemblies
    for sa in [sub01, sub02, sub03]:
        err = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warn = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        sw.OpenDoc6(sa, 2, 1, "", err, warn)

    showcase_assy = sw.NewDocument(assy_tpl, 0, 0.0, 0.0)
    # Tier 1: Earth Port Platform at sea level (Y = 0m)
    showcase_assy.AddComponent4(sub01, "", 0.0, 0.0, 0.0)
    # Tier 2: 20-Metric-Ton Climber ascending at Y = +60.0m
    showcase_assy.AddComponent4(sub02, "", 0.0, 60.0, 0.0)
    # Tier 3: GEO Orbital Terminal Station at Y = +180.0m
    showcase_assy.AddComponent4(sub04, "", 0.0, 180.0, 0.0)
    # Tier 4: Apex Counterweight Hub at Y = +320.0m
    showcase_assy.AddComponent4(sub03, "", 0.0, 320.0, 0.0)

    showcase_assy.ClearSelection2(True)
    showcase_assy.ForceRebuild3(False)
    showcase_assy.ShowNamedView2("*Isometric", 7)
    showcase_assy.ViewZoomtofit2()

    showcase_path = os.path.join(assy_dir, "00_Space_Elevator_Master_Showcase.SLDASM")
    showcase_step = os.path.join(step_dir, "00_Space_Elevator_Master_Showcase.STEP")
    showcase_png = os.path.join(renders_main, "00_Space_Elevator_Master_Showcase.PNG")
    showcase_investor_png = os.path.join(render_dir, "00_Space_Elevator_Master_Showcase.PNG")

    showcase_assy.SaveAs3(showcase_path, 0, 2)
    showcase_assy.SaveAs3(showcase_step, 0, 2)
    showcase_assy.SaveAs3(showcase_png, 0, 2)
    showcase_assy.SaveAs3(showcase_investor_png, 0, 2)
    print(f"      Saved: {showcase_path}")
    print(f"      Exported STEP: {showcase_step}")
    print(f"      Saved Showcase Renders")

    # Restore preferences
    sw.SetUserPreferenceToggle(10, True)
    sw.Visible = True
    sw.UserControl = True
    print("\nALL HIGH-FIDELITY AEROSPACE MODULES & MASTER SHOWCASES SUCCESSFULLY BUILT AND ACTIVE IN SOLIDWORKS!")

if __name__ == "__main__":
    try:
        build_geo_system()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
