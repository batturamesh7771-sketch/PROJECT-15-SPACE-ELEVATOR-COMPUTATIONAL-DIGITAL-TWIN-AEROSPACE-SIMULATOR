Option Explicit

Dim swApp, assyTpl, baseDir, partsDir, assyDir, stepDir, renderDir
Dim assy, doc, errs, warns

Set swApp = CreateObject("SldWorks.Application")
swApp.Visible = True
swApp.UserControl = True
swApp.SetUserPreferenceToggle 10, False ' swInputDimValOnCreate = False
swApp.SetUserPreferenceIntegerValue 192, 1 ' swLightBackground (Plain White)

assyTpl = swApp.GetUserPreferenceStringValue(9)
baseDir = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
partsDir = baseDir & "\Parts_GEO"
assyDir = baseDir & "\Assemblies"
stepDir = baseDir & "\ANSYS_Exports_STEP"
renderDir = baseDir & "\Investor_Renders"

WScript.Echo "[1/4] Creating new assembly document..."
Set assy = swApp.NewDocument(assyTpl, 0, 0, 0)
If assy Is Nothing Then
    WScript.Echo "ERROR: Could not create assembly document"
    WScript.Quit 1
End If

WScript.Echo "[2/4] Inserting 7 specialized aerospace modules into assembly..."
' 1. Central Transit Core at origin (0, 0, 0)
assy.AddComponent5 partsDir & "\GEO_01_Central_Transit_Core.SLDPRT", 0, "", False, "", 0, 0, 0
WScript.Echo "      Inserted GEO_01_Central_Transit_Core (180m Mast)"

' 2. Pressurized Torus Hab Ring at origin (0, 0, 0)
assy.AddComponent5 partsDir & "\GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT", 0, "", False, "", 0, 0, 0
WScript.Echo "      Inserted GEO_02_Pressurized_Torus_Hab_Ring (208m Torus)"

' 3. Structural Spoke Corridors at origin (0, 0, 0)
assy.AddComponent5 partsDir & "\GEO_03_Structural_Spoke_Corridors.SLDPRT", 0, "", False, "", 0, 0, 0
WScript.Echo "      Inserted GEO_03_Structural_Spoke_Corridors"

' 4. Geodesic Biosphere Spheres (4 eco-domes) at origin (0, 0, 0)
assy.AddComponent5 partsDir & "\GEO_04_Geodesic_Biosphere_Spheres.SLDPRT", 0, "", False, "", 0, 0, 0
WScript.Echo "      Inserted GEO_04_Geodesic_Biosphere_Spheres"

' 5. Mega Solar Photovoltaic Wings at Upper Bulkhead (Y = +75.0m)
assy.AddComponent5 partsDir & "\GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT", 0, "", False, "", 0, 75.0, 0
WScript.Echo "      Inserted GEO_05_Mega_Solar_Photovoltaic_Wings (Y = +75m)"

' 6. Communications Spire and RCS Mast at Core Top (Y = 0.0m)
assy.AddComponent5 partsDir & "\GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT", 0, "", False, "", 0, 0, 0
WScript.Echo "      Inserted GEO_06_Communications_Spire_And_RCS_Mast (Y = +90m to +175m)"

' 7. Continuous 400m Graphene Tether passing through origin (0, 0, 0)
assy.AddComponent5 partsDir & "\GEO_07_Continuous_Tether_Ribbon.SLDPRT", 0, "", False, "", 0, 0, 0
WScript.Echo "      Inserted GEO_07_Continuous_Tether_Ribbon (400m Length)"

WScript.Echo "[3/4] Rebuilding and setting True 3D Isometric Viewport..."
assy.ForceRebuild3 False
assy.ShowNamedView2 "*Isometric", 7
assy.ViewZoomtofit2

WScript.Echo "[4/4] Saving Assembly, STEP AP214 Neutral File & Isometric Viewport Render..."
assy.SaveAs3 assyDir & "\04_GEO_Orbital_Terminal_Station.SLDASM", 0, 2
assy.SaveAs3 stepDir & "\GEO_Orbital_Terminal_Station_Complete.STEP", 0, 2
assy.SaveAs3 renderDir & "\GEO_Orbital_Terminal_Station_Isometric.PNG", 0, 2

swApp.SetUserPreferenceToggle 10, True
swApp.Visible = True
swApp.UserControl = True
WScript.Echo "MASTER GEO ORBITAL TERMINAL STATION BUILT AND ACTIVE IN SOLIDWORKS!"
