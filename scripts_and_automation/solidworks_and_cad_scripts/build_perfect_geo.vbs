Option Explicit

Dim swApp, partTpl, assyTpl, baseDir, partsDir, partsGeoDir, assyDir, stepDir, renderDir, rendersMain
Dim pi

Set swApp = GetObject("", "SldWorks.Application")
If swApp Is Nothing Then
    Set swApp = CreateObject("SldWorks.Application")
End If

swApp.Visible = True
swApp.UserControl = True
swApp.SetUserPreferenceToggle 10, False ' swInputDimValOnCreate = False
swApp.SetUserPreferenceIntegerValue 192, 1 ' swLightBackground = Plain White

partTpl = swApp.GetUserPreferenceStringValue(8)
assyTpl = swApp.GetUserPreferenceStringValue(9)
baseDir = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
partsDir = baseDir & "\Parts"
partsGeoDir = baseDir & "\Parts_GEO"
assyDir = baseDir & "\Assemblies"
stepDir = baseDir & "\ANSYS_Exports_STEP"
renderDir = baseDir & "\Investor_Renders"
rendersMain = baseDir & "\Renders"
pi = 3.14159265358979

Sub SetAppearance(doc, r, g, b, ambient, diffuse, specular, shininess, transparency)
    Dim p(8)
    p(0) = r / 255.0
    p(1) = g / 255.0
    p(2) = b / 255.0
    p(3) = ambient
    p(4) = diffuse
    p(5) = specular
    p(6) = shininess
    p(7) = transparency
    p(8) = 0.0
    doc.MaterialPropertyValues = p
End Sub

Sub SaveAndClosePart(doc, name)
    Dim partPath, stepPath, pngPath
    partPath = partsGeoDir & "\" & name & ".SLDPRT"
    stepPath = stepDir & "\" & name & ".STEP"
    pngPath = renderDir & "\" & name & ".PNG"

    doc.ClearSelection2 True
    doc.ForceRebuild3 False
    doc.ShowNamedView2 "*Isometric", 7
    doc.ViewZoomtofit2

    doc.SaveAs3 partPath, 0, 2
    doc.SaveAs3 stepPath, 0, 2
    doc.SaveAs3 pngPath, 0, 2
    WScript.Echo "      Saved: " & name & " (.SLDPRT, .STEP, .PNG)"
    swApp.CloseDoc doc.GetTitle
End Sub

' ==============================================================================
' STEP 1: REBUILD GEO_04_Geodesic_Biosphere_Spheres.SLDPRT (4 Full 3D Solid Spheres)
' ==============================================================================
WScript.Echo "[1/4] Building GEO_04_Geodesic_Biosphere_Spheres..."
Dim doc4, sk4, ft4
Set doc4 = swApp.NewDocument(partTpl, 0, 0, 0)
Set sk4 = doc4.SketchManager
Set ft4 = doc4.FeatureManager

' Sphere 1 (+X at 50, 0, 0)
doc4.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk4.InsertSketch True
sk4.CreateCenterLine 50.0, -25.0, 0, 50.0, 25.0, 0
sk4.CreateArc 50.0, 0.0, 0, 50.0, -13.0, 0, 50.0, 13.0, 0, 1
sk4.CreateLine 50.0, 13.0, 0, 50.0, -13.0, 0
sk4.InsertSketch True
ft4.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Sphere 2 (-X at -50, 0, 0)
doc4.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk4.InsertSketch True
sk4.CreateCenterLine -50.0, -25.0, 0, -50.0, 25.0, 0
sk4.CreateArc -50.0, 0.0, 0, -50.0, 13.0, 0, -50.0, -13.0, 0, 1
sk4.CreateLine -50.0, -13.0, 0, -50.0, 13.0, 0
sk4.InsertSketch True
ft4.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Sphere 3 (+Z at 0, 0, 50)
doc4.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk4.InsertSketch True
sk4.CreateCenterLine 50.0, -25.0, 0, 50.0, 25.0, 0
sk4.CreateArc 50.0, 0.0, 0, 50.0, -13.0, 0, 50.0, 13.0, 0, 1
sk4.CreateLine 50.0, 13.0, 0, 50.0, -13.0, 0
sk4.InsertSketch True
ft4.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Sphere 4 (-Z at 0, 0, -50)
doc4.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk4.InsertSketch True
sk4.CreateCenterLine -50.0, -25.0, 0, -50.0, 25.0, 0
sk4.CreateArc -50.0, 0.0, 0, -50.0, 13.0, 0, -50.0, -13.0, 0, 1
sk4.CreateLine -50.0, -13.0, 0, -50.0, 13.0, 0
sk4.InsertSketch True
ft4.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Equatorial Structural Spaceframe Rings on all 4 spheres
doc4.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk4.InsertSketch True
doc4.CreateCircleByRadius2  50.0, 0.0, 0.0, 13.8
doc4.CreateCircleByRadius2  50.0, 0.0, 0.0, 13.0
doc4.CreateCircleByRadius2 -50.0, 0.0, 0.0, 13.8
doc4.CreateCircleByRadius2 -50.0, 0.0, 0.0, 13.0
doc4.CreateCircleByRadius2   0.0, 0.0,  50.0, 13.8
doc4.CreateCircleByRadius2   0.0, 0.0,  50.0, 13.0
doc4.CreateCircleByRadius2   0.0, 0.0, -50.0, 13.8
doc4.CreateCircleByRadius2   0.0, 0.0, -50.0, 13.0
sk4.InsertSketch True
ft4.FeatureExtrusion2 True, False, False, 0, 0, 0.75, 0.75, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance doc4, 140, 205, 235, 0.6, 0.9, 0.95, 0.85, 0.45 ' Translucent Silica Glass
SaveAndClosePart doc4, "GEO_04_Geodesic_Biosphere_Spheres"

' ==============================================================================
' STEP 2: REBUILD GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT (6 Radial Wings)
' ==============================================================================
WScript.Echo "[2/4] Building 6-Wing Radial Array GEO_05_Mega_Solar_Photovoltaic_Wings..."
Dim doc5, sk5, ft5, i, rad, ca, sa, px, pz, r1, r2, hw
Dim c1x, c1z, c2x, c2z, c3x, c3z, c4x, c4z

Set doc5 = swApp.NewDocument(partTpl, 0, 0, 0)
Set sk5 = doc5.SketchManager
Set ft5 = doc5.FeatureManager

' Central rotary joint / hub (OD = 22m, ID = 18m, height = 3.0m)
doc5.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk5.InsertSketch True
doc5.CreateCircleByRadius2 0, 0, 0, 11.0
doc5.CreateCircleByRadius2 0, 0, 0, 9.0
sk5.InsertSketch True
ft5.FeatureExtrusion2 True, False, False, 0, 0, 1.5, 1.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 6 Radial Solar Array Wings: 0, 60, 120, 180, 240, 300 degrees
doc5.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk5.InsertSketch True
For i = 0 To 5
    rad = i * 60.0 * pi / 180.0
    ca = Cos(rad)
    sa = Sin(rad)
    px = -sa
    pz = ca
    r1 = 12.0
    r2 = 95.0
    hw = 8.0

    c1x = r1 * ca - hw * px: c1z = r1 * sa - hw * pz
    c2x = r2 * ca - hw * px: c2z = r2 * sa - hw * pz
    c3x = r2 * ca + hw * px: c3z = r2 * sa + hw * pz
    c4x = r1 * ca + hw * px: c4z = r1 * sa + hw * pz

    sk5.CreateLine c1x, c1z, 0, c2x, c2z, 0
    sk5.CreateLine c2x, c2z, 0, c3x, c3z, 0
    sk5.CreateLine c3x, c3z, 0, c4x, c4z, 0
    sk5.CreateLine c4x, c4z, 0, c1x, c1z, 0
Next
sk5.InsertSketch True
ft5.FeatureExtrusion2 True, False, False, 0, 0, 0.175, 0.175, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 6 Central Structural Reinforcement Booms
doc5.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
sk5.InsertSketch True
For i = 0 To 5
    rad = i * 60.0 * pi / 180.0
    ca = Cos(rad)
    sa = Sin(rad)
    px = -sa
    pz = ca
    r1 = 11.0
    r2 = 95.0
    hw = 0.9

    c1x = r1 * ca - hw * px: c1z = r1 * sa - hw * pz
    c2x = r2 * ca - hw * px: c2z = r2 * sa - hw * pz
    c3x = r2 * ca + hw * px: c3z = r2 * sa + hw * pz
    c4x = r1 * ca + hw * px: c4z = r1 * sa + hw * pz

    sk5.CreateLine c1x, c1z, 0, c2x, c2z, 0
    sk5.CreateLine c2x, c2z, 0, c3x, c3z, 0
    sk5.CreateLine c3x, c3z, 0, c4x, c4z, 0
    sk5.CreateLine c4x, c4z, 0, c1x, c1z, 0
Next
sk5.InsertSketch True
ft5.FeatureExtrusion2 True, False, False, 0, 0, 0.5, 0.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance doc5, 15, 30, 85, 0.7, 0.95, 0.98, 0.95, 0.0 ' Deep Photovoltaic Sapphire Blue
SaveAndClosePart doc5, "GEO_05_Mega_Solar_Photovoltaic_Wings"

' ==============================================================================
' STEP 3: ASSEMBLE 04_GEO_Orbital_Terminal_Station.SLDASM
' ==============================================================================
WScript.Echo "[3/4] Assembling 04_GEO_Orbital_Terminal_Station.SLDASM..."
Dim assy
Set assy = swApp.NewDocument(assyTpl, 0, 0, 0)
If assy Is Nothing Then
    WScript.Echo "ERROR: Could not create assembly!"
    WScript.Quit 1
End If

' Insert all 7 modules using AddComponent4
assy.AddComponent4 partsGeoDir & "\GEO_01_Central_Transit_Core.SLDPRT", "", 0, 0, 0
WScript.Echo "      Added GEO_01_Central_Transit_Core (180m Mast)"

assy.AddComponent4 partsGeoDir & "\GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT", "", 0, 0, 0
WScript.Echo "      Added GEO_02_Pressurized_Torus_Hab_Ring (208m Torus)"

assy.AddComponent4 partsGeoDir & "\GEO_03_Structural_Spoke_Corridors.SLDPRT", "", 0, 0, 0
WScript.Echo "      Added GEO_03_Structural_Spoke_Corridors"

assy.AddComponent4 partsGeoDir & "\GEO_04_Geodesic_Biosphere_Spheres.SLDPRT", "", 0, 0, 0
WScript.Echo "      Added GEO_04_Geodesic_Biosphere_Spheres (4 Spheres)"

assy.AddComponent4 partsGeoDir & "\GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT", "", 0, 75.0, 0
WScript.Echo "      Added GEO_05_Mega_Solar_Photovoltaic_Wings (6 Wings at Y=+75m)"

assy.AddComponent4 partsGeoDir & "\GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT", "", 0, 0, 0
WScript.Echo "      Added GEO_06_Communications_Spire_And_RCS_Mast"

assy.AddComponent4 partsGeoDir & "\GEO_07_Continuous_Tether_Ribbon.SLDPRT", "", 0, 0, 0
WScript.Echo "      Added GEO_07_Continuous_Tether_Ribbon (400m Length)"

assy.ClearSelection2 True
assy.ForceRebuild3 False
assy.ShowNamedView2 "*Isometric", 7
assy.ViewZoomtofit2

assy.SaveAs3 assyDir & "\04_GEO_Orbital_Terminal_Station.SLDASM", 0, 2
assy.SaveAs3 stepDir & "\GEO_Orbital_Terminal_Station_Complete.STEP", 0, 2
assy.SaveAs3 renderDir & "\GEO_Orbital_Terminal_Station_Isometric.PNG", 0, 2
WScript.Echo "      Saved 04_GEO_Orbital_Terminal_Station (.SLDASM, .STEP, .PNG)"

' ==============================================================================
' STEP 4: REBUILD 00_Space_Elevator_Master_Showcase.SLDASM (Multi-Tier Trajectory)
' Earth Port (Y=0m) -> Climber (Y=60m) -> GEO Terminal (Y=180m) -> Apex (Y=320m)
' ==============================================================================
WScript.Echo "[4/4] Assembling 00_Space_Elevator_Master_Showcase.SLDASM..."
Dim showcase
Set showcase = swApp.NewDocument(assyTpl, 0, 0, 0)
showcase.AddComponent4 assyDir & "\01_Earth_Port_Platform.SLDASM", "", 0, 0, 0
showcase.AddComponent4 assyDir & "\02_Tether_Climber_20T.SLDASM", "", 0, 60.0, 0
showcase.AddComponent4 assyDir & "\04_GEO_Orbital_Terminal_Station.SLDASM", "", 0, 180.0, 0
showcase.AddComponent4 assyDir & "\03_Tether_And_Apex_Hub.SLDASM", "", 0, 320.0, 0

showcase.ClearSelection2 True
showcase.ForceRebuild3 False
showcase.ShowNamedView2 "*Isometric", 7
showcase.ViewZoomtofit2

showcase.SaveAs3 assyDir & "\00_Space_Elevator_Master_Showcase.SLDASM", 0, 2
showcase.SaveAs3 stepDir & "\00_Space_Elevator_Master_Showcase.STEP", 0, 2
showcase.SaveAs3 rendersMain & "\00_Space_Elevator_Master_Showcase.PNG", 0, 2
showcase.SaveAs3 renderDir & "\00_Space_Elevator_Master_Showcase.PNG", 0, 2
WScript.Echo "      Saved 00_Space_Elevator_Master_Showcase (.SLDASM, .STEP, .PNG)"

' Leave 04_GEO_Orbital_Terminal_Station open and active for the user
swApp.ActivateDoc3 "04_GEO_Orbital_Terminal_Station.SLDASM", False, 0, 0
assy.ShowNamedView2 "*Isometric", 7
assy.ViewZoomtofit2

swApp.SetUserPreferenceToggle 10, True
swApp.Visible = True
swApp.UserControl = True
WScript.Echo "ALL STATIONS & SHOWCASES GENERATED WITH COMPLETE GEOMETRY AND ISOMETRIC VIEWPORTS!"
