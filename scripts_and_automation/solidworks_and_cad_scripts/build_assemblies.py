import os
import sys
import win32com.client
import pythoncom

def build_all_assemblies():
    pythoncom.CoInitialize()
    print("[1/5] Connecting to SolidWorks COM API...")
    sw_app = win32com.client.Dispatch("SldWorks.Application")
    sw_app.Visible = True
    sw_app.UserControl = True
    sw_app.SetUserPreferenceToggle(10, False) # swInputDimValOnCreate = False

    assy_tpl = sw_app.GetUserPreferenceStringValue(9)
    print("      Active Assembly Template:", assy_tpl)

    base_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
    parts_dir = os.path.join(base_dir, "Parts")
    assy_dir = os.path.join(base_dir, "Assemblies")
    step_dir = os.path.join(base_dir, "ANSYS_Exports_STEP")
    renders_dir = os.path.join(base_dir, "Renders")

    # Helper to load part/assy in memory
    def load_doc(path, doc_type=1): # 1 = Part, 2 = Assy
        err = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        warn = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        doc = sw_app.OpenDoc6(path, doc_type, 1, "", err, warn)
        return doc

    def save_and_close_assy(assy_model, name, keep_open=False):
        assy_path = os.path.join(assy_dir, name + ".SLDASM")
        step_path = os.path.join(step_dir, name + ".STEP")
        png_path = os.path.join(renders_dir, name + ".PNG")

        assy_model.ForceRebuild3(False)
        assy_model.ShowNamedView2("*Isometric", 7)
        assy_model.ViewZoomtofit2()

        assy_model.SaveAs3(assy_path, 0, 2)
        assy_model.SaveAs3(step_path, 0, 2)
        assy_model.SaveAs3(png_path, 0, 2)
        print(f"      Saved: {name} (.SLDASM, .STEP, .PNG)")
        if not keep_open:
            title = assy_model.GetTitle
            sw_app.CloseDoc(title)

    # Preload all parts silently into SolidWorks memory
    part_files = [
        "EP_01_SemiSubmersible_Hull.SLDPRT",
        "EP_02_Outer_Gimbal_Ring.SLDPRT",
        "EP_03_Inner_Gimbal_And_Capstan_Hub.SLDPRT",
        "EP_04_Lightning_And_Wind_Arrestor_Tower.SLDPRT",
        "CL_01_Hex_Composite_Chassis.SLDPRT",
        "CL_02_Pinch_Drive_Roller.SLDPRT",
        "CL_03_Hydraulic_Clamping_Actuator_Yoke.SLDPRT",
        "CL_04_Thermal_Radiator_Wing.SLDPRT",
        "CL_05_Laser_PV_Receiver_Dish.SLDPRT",
        "TE_01_Graphene_Tether_Segment_10m.SLDPRT",
        "AP_01_Apex_Counterweight_Core.SLDPRT",
        "AP_02_Peet_Interplanetary_Sling_Ramp.SLDPRT",
    ]
    loaded_parts = {}
    print("[2/5] Loading all 12 parametric parts into SolidWorks memory...")
    for pf in part_files:
        p_path = os.path.join(parts_dir, pf)
        loaded_parts[pf] = load_doc(p_path, 1)

    # =========================================================================
    # Sub-Assembly 01: Equatorial Marine Earth Port Platform (100 m scale)
    # =========================================================================
    print("[3/5] Assembling 01_Earth_Port_Platform.SLDASM...")
    assy01 = sw_app.NewDocument(assy_tpl, 0, 0.0, 0.0)
    assy01.AddComponent4(os.path.join(parts_dir, "EP_01_SemiSubmersible_Hull.SLDPRT"), "", 0.0, 0.0, 0.0)
    assy01.AddComponent4(os.path.join(parts_dir, "EP_02_Outer_Gimbal_Ring.SLDPRT"), "", 0.0, 0.0, 0.0)
    assy01.AddComponent4(os.path.join(parts_dir, "EP_03_Inner_Gimbal_And_Capstan_Hub.SLDPRT"), "", 0.0, 0.0, 0.0)
    assy01.AddComponent4(os.path.join(parts_dir, "EP_04_Lightning_And_Wind_Arrestor_Tower.SLDPRT"), "", 0.0, 4.25, 0.0)
    save_and_close_assy(assy01, "01_Earth_Port_Platform")

    # =========================================================================
    # Sub-Assembly 02: 20-Metric-Ton Tether Climber & Pinch-Drive Module (6 m scale)
    # =========================================================================
    print("[4/5] Assembling 02_Tether_Climber_20T.SLDASM...")
    assy02 = sw_app.NewDocument(assy_tpl, 0, 0.0, 0.0)
    # Chassis centered at origin
    assy02.AddComponent4(os.path.join(parts_dir, "CL_01_Hex_Composite_Chassis.SLDPRT"), "", 0.0, 0.0, 0.0)

    # 6 Pinch Rollers (3 opposing pairs at Y = +1.0m, +2.5m, +4.0m; Z = +0.202m and -0.202m)
    # and 6 Hydraulic Actuators (Z = +0.45m and -0.45m)
    for y_elev in [1.0, 2.5, 4.0]:
        # Front Roller & Actuator
        assy02.AddComponent4(os.path.join(parts_dir, "CL_02_Pinch_Drive_Roller.SLDPRT"), "", 0.0, y_elev, 0.202)
        assy02.AddComponent4(os.path.join(parts_dir, "CL_03_Hydraulic_Clamping_Actuator_Yoke.SLDPRT"), "", 0.0, y_elev, 0.45)
        # Rear Roller & Actuator
        assy02.AddComponent4(os.path.join(parts_dir, "CL_02_Pinch_Drive_Roller.SLDPRT"), "", 0.0, y_elev, -0.202)
        assy02.AddComponent4(os.path.join(parts_dir, "CL_03_Hydraulic_Clamping_Actuator_Yoke.SLDPRT"), "", 0.0, y_elev, -0.45)

    # 2 Radiator Wings (Starboard X = +1.65m, Port X = -1.65m)
    assy02.AddComponent4(os.path.join(parts_dir, "CL_04_Thermal_Radiator_Wing.SLDPRT"), "", 1.65, 0.4, 0.0)
    assy02.AddComponent4(os.path.join(parts_dir, "CL_04_Thermal_Radiator_Wing.SLDPRT"), "", -1.65, 0.4, 0.0)

    # Laser PV Receiver Dish at base (Y = 0.0m)
    assy02.AddComponent4(os.path.join(parts_dir, "CL_05_Laser_PV_Receiver_Dish.SLDPRT"), "", 0.0, 0.0, 0.0)

    # Insert 10m Tether Segment gripping through the roller nip
    assy02.AddComponent4(os.path.join(parts_dir, "TE_01_Graphene_Tether_Segment_10m.SLDPRT"), "", 0.0, -2.5, 0.0)
    save_and_close_assy(assy02, "02_Tether_Climber_20T")

    # =========================================================================
    # Sub-Assembly 03: Local Graphene Tether & Apex Anchor Hub
    # =========================================================================
    print("[5/5] Assembling 03_Tether_And_Apex_Hub.SLDASM...")
    assy03 = sw_app.NewDocument(assy_tpl, 0, 0.0, 0.0)
    assy03.AddComponent4(os.path.join(parts_dir, "AP_01_Apex_Counterweight_Core.SLDPRT"), "", 0.0, 0.0, 0.0)
    assy03.AddComponent4(os.path.join(parts_dir, "AP_02_Peet_Interplanetary_Sling_Ramp.SLDPRT"), "", 8.0, 0.0, 0.0)
    save_and_close_assy(assy03, "03_Tether_And_Apex_Hub")

    # =========================================================================
    # Master Assembly 00: Investor Presentation Multi-Tier Showcase Assembly
    # =========================================================================
    print("[SHOWCASE] Assembling 00_Space_Elevator_Master_Showcase.SLDASM...")
    # Preload sub-assemblies
    sub01_path = os.path.join(assy_dir, "01_Earth_Port_Platform.SLDASM")
    sub02_path = os.path.join(assy_dir, "02_Tether_Climber_20T.SLDASM")
    sub03_path = os.path.join(assy_dir, "03_Tether_And_Apex_Hub.SLDASM")
    load_doc(sub01_path, 2)
    load_doc(sub02_path, 2)
    load_doc(sub03_path, 2)

    master_assy = sw_app.NewDocument(assy_tpl, 0, 0.0, 0.0)
    # 1. Earth Port at origin (0, 0, 0)
    master_assy.AddComponent4(sub01_path, "", 0.0, 0.0, 0.0)
    # 2. Climber with tether segment 45m above Earth Port
    master_assy.AddComponent4(sub02_path, "", 0.0, 45.0, 0.0)
    # 3. Apex Hub 80m above Earth Port
    master_assy.AddComponent4(sub03_path, "", 0.0, 80.0, 0.0)

    # Save master showcase assembly (keep open for user to view live!)
    save_and_close_assy(master_assy, "00_Space_Elevator_Master_Showcase", keep_open=True)

    # Restore swInputDimValOnCreate
    sw_app.SetUserPreferenceToggle(10, True)
    print("ALL ASSEMBLIES CONSTRUCTED SUCCESSFULLY AND READY FOR INVESTOR SHOWCASE!")

if __name__ == "__main__":
    try:
        build_all_assemblies()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
