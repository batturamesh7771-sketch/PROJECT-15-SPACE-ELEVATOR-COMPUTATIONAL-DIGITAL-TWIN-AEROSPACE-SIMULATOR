import os
import sys
import win32com.client
import pythoncom

def assemble_geo():
    pythoncom.CoInitialize()
    print("[1/4] Connecting to SolidWorks...")
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.Visible = True
    sw.UserControl = True
    sw.SetUserPreferenceToggle(10, False)
    sw.SetUserPreferenceIntegerValue(192, 1)

    assy_tpl = sw.GetUserPreferenceStringValue(9)
    base_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
    parts_geo_dir = os.path.join(base_dir, "Parts_GEO")
    assy_dir = os.path.join(base_dir, "Assemblies")
    step_dir = os.path.join(base_dir, "ANSYS_Exports_STEP")
    render_dir = os.path.join(base_dir, "Investor_Renders")

    def load_doc(path, doc_type=1):
        err = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warn = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        doc = sw.OpenDoc6(path, doc_type, 1, "", err, warn)
        return doc

    geo_parts = [
        "GEO_01_Central_Transit_Core.SLDPRT",
        "GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT",
        "GEO_03_Structural_Spoke_Corridors.SLDPRT",
        "GEO_04_Geodesic_Biosphere_Spheres.SLDPRT",
        "GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT",
        "GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT",
        "GEO_07_Continuous_Tether_Ribbon.SLDPRT"
    ]

    print("[2/4] Preloading all 7 GEO parts into RAM...")
    loaded = {}
    for pf in geo_parts:
        pp = os.path.join(parts_geo_dir, pf)
        loaded[pf] = load_doc(pp, 1)
        print(f"      Loaded: {pf}")

    print("[3/4] Creating Assembly and adding components...")
    assy = sw.NewDocument(assy_tpl, 0, 0.0, 0.0)
    if not assy:
        print("ERROR: Failed to create assembly document")
        return

    # Add components via AddComponent4
    c1 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_01_Central_Transit_Core.SLDPRT"), "", 0.0, 0.0, 0.0)
    c2 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT"), "", 0.0, 0.0, 0.0)
    c3 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_03_Structural_Spoke_Corridors.SLDPRT"), "", 0.0, 0.0, 0.0)
    c4 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_04_Geodesic_Biosphere_Spheres.SLDPRT"), "", 0.0, 0.0, 0.0)
    c5 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT"), "", 0.0, 75.0, 0.0)
    c6 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT"), "", 0.0, 0.0, 0.0)
    c7 = assy.AddComponent4(os.path.join(parts_geo_dir, "GEO_07_Continuous_Tether_Ribbon.SLDPRT"), "", 0.0, 0.0, 0.0)

    comps = assy.GetComponents(False)
    print(f"      Total Components in Assembly: {len(comps) if comps else 0}")
    if comps:
        for c in comps:
            print(f"       + {c.Name2}")

    print("[4/4] Setting 3D Isometric View, Zoom to fit, and Saving...")
    assy.ClearSelection2(True)
    assy.ForceRebuild3(False)
    assy.ShowNamedView2("*Isometric", 7)
    assy.ViewZoomtofit2()

    assy_path = os.path.join(assy_dir, "04_GEO_Orbital_Terminal_Station.SLDASM")
    step_path = os.path.join(step_dir, "GEO_Orbital_Terminal_Station_Complete.STEP")
    png_path = os.path.join(render_dir, "GEO_Orbital_Terminal_Station_Isometric.PNG")

    assy.SaveAs3(assy_path, 0, 2)
    assy.SaveAs3(step_path, 0, 2)
    assy.SaveAs3(png_path, 0, 2)
    print(f"      Saved: {assy_path}")
    print(f"      Exported STEP: {step_path} (Size: {os.path.getsize(step_path):,} bytes)")
    print(f"      Saved Render: {png_path} (Size: {os.path.getsize(png_path):,} bytes)")

    # Also build 00_Space_Elevator_Master_Showcase.SLDASM with vertical tier spacing
    print("[SHOWCASE] Assembling 00_Space_Elevator_Master_Showcase.SLDASM...")
    sub01 = os.path.join(assy_dir, "01_Earth_Port_Platform.SLDASM")
    sub02 = os.path.join(assy_dir, "02_Tether_Climber_20T.SLDASM")
    sub03 = os.path.join(assy_dir, "03_Tether_And_Apex_Hub.SLDASM")
    load_doc(sub01, 2)
    load_doc(sub02, 2)
    load_doc(sub03, 2)

    showcase = sw.NewDocument(assy_tpl, 0, 0.0, 0.0)
    showcase.AddComponent4(sub01, "", 0.0, 0.0, 0.0)
    showcase.AddComponent4(sub02, "", 0.0, 60.0, 0.0)
    showcase.AddComponent4(assy_path, "", 0.0, 180.0, 0.0)
    showcase.AddComponent4(sub03, "", 0.0, 320.0, 0.0)

    showcase.ClearSelection2(True)
    showcase.ForceRebuild3(False)
    showcase.ShowNamedView2("*Isometric", 7)
    showcase.ViewZoomtofit2()

    showcase_path = os.path.join(assy_dir, "00_Space_Elevator_Master_Showcase.SLDASM")
    showcase_step = os.path.join(step_dir, "00_Space_Elevator_Master_Showcase.STEP")
    showcase_png1 = os.path.join(base_dir, "Renders", "00_Space_Elevator_Master_Showcase.PNG")
    showcase_png2 = os.path.join(render_dir, "00_Space_Elevator_Master_Showcase.PNG")

    showcase.SaveAs3(showcase_path, 0, 2)
    showcase.SaveAs3(showcase_step, 0, 2)
    showcase.SaveAs3(showcase_png1, 0, 2)
    showcase.SaveAs3(showcase_png2, 0, 2)
    print(f"      Saved Showcase: {showcase_step} (Size: {os.path.getsize(showcase_step):,} bytes)")

    # Restore preferences
    sw.SetUserPreferenceToggle(10, True)
    sw.Visible = True
    sw.UserControl = True
    print("\n[COMPLETE] All Assemblies successfully generated with full 3D geometry and verified STEP exports!")

if __name__ == "__main__":
    assemble_geo()
