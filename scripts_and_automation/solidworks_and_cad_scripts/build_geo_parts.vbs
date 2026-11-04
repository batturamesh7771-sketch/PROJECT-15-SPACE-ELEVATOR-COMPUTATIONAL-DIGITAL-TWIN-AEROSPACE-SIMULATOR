Option Explicit

Dim swApp, partTpl, baseDir, partsDir, stepDir, rendersDir
Dim model, featMgr, skMgr, sel, feat
Dim pi, i, angle, x1, z1, x2, z2

Set swApp = GetObject("", "SldWorks.Application")
If swApp Is Nothing Then
    Set swApp = CreateObject("SldWorks.Application")
End If

swApp.Visible = True
swApp.UserControl = True
swApp.SetUserPreferenceToggle 10, False ' swInputDimValOnCreate = False
swApp.SetUserPreferenceIntegerValue 192, 1 ' swLightBackground (Plain White)

partTpl = swApp.GetUserPreferenceStringValue(8)
baseDir = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
partsDir = baseDir & "\Parts_GEO"
stepDir = baseDir & "\ANSYS_Exports_STEP"
rendersDir = baseDir & "\Investor_Renders"
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

Sub SaveAndClose(doc, name)
    Dim partPath, stepPath, pngPath
    partPath = partsDir & "\" & name & ".SLDPRT"
    stepPath = stepDir & "\" & name & ".STEP"
    pngPath = rendersDir & "\" & name & ".PNG"

    doc.ForceRebuild3 False
    doc.ShowNamedView2 "*Isometric", 7
    doc.ViewZoomtofit2

    doc.SaveAs3 partPath, 0, 2
    doc.SaveAs3 stepPath, 0, 2
    doc.SaveAs3 pngPath, 0, 2
    WScript.Echo "Generated: " & name & " (.SLDPRT, .STEP, .PNG)"
    swApp.CloseDoc doc.GetTitle
End Sub

' ==============================================================================
' MODULE 1: GEO_01_Central_Transit_Core.SLDPRT (180m Backbone Guideway)
' ==============================================================================
WScript.Echo "[1/7] Building GEO_01_Central_Transit_Core..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' 1.1 Main Hollow Cylinder: OD = 18.0m (R=9.0), ID = 10.0m (R=5.0)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 9.0
model.CreateCircleByRadius2 0, 0, 0, 5.0
skMgr.InsertSketch True
' Total Height = 180m (Y: -90m to +90m)
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 90.0, 90.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 1.2 6 External Longitudinal Stiffener Ribs (Width 1.2m, Radial 1.5m, Length 160m)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
For i = 0 To 5
    angle = i * 60.0 * pi / 180.0
    x1 = 9.0 * Cos(angle)
    z1 = 9.0 * Sin(angle)
    x2 = 10.5 * Cos(angle)
    z2 = 10.5 * Sin(angle)
    skMgr.CreateCornerRectangle x1 - 0.6, z1 - 0.6, 0, x2 + 0.6, z2 + 0.6, 0
Next
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 80.0, 80.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 1.3 4 Maglev Climber Docking Apertures / Collars at Y = +25m and Y = -25m
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0,  25.0, 0, 3.0
model.CreateCircleByRadius2 0, -25.0, 0, 3.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 10.2, 10.2, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 170, 175, 185, 0.7, 0.8, 0.65, 0.70, 0.0 ' Grade 5 Titanium Alloy
SaveAndClose model, "GEO_01_Central_Transit_Core"

' ==============================================================================
' MODULE 2: GEO_02_Pressurized_Torus_Hab_Ring.SLDPRT (208m Centrifugal Ring)
' ==============================================================================
WScript.Echo "[2/7] Building GEO_02_Pressurized_Torus_Hab_Ring..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Torus Cross-Section: Major Radius = 95.0m, Width = 18.0m (X: 86.0 to 104.0), Height = 14.0m (Y: -7.0 to +7.0)
' Revolve around Global Vertical Y-Axis in Front Plane
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 0, -50.0, 0, 0, 50.0, 0

' Outer aerodynamic capsule profile (chamfered corners)
skMgr.CreateLine 86.0, -4.0, 0, 86.0,  4.0, 0
skMgr.CreateLine 86.0,  4.0, 0, 89.0,  7.0, 0
skMgr.CreateLine 89.0,  7.0, 0, 101.0, 7.0, 0
skMgr.CreateLine 101.0, 7.0, 0, 104.0, 4.0, 0
skMgr.CreateLine 104.0, 4.0, 0, 104.0,-4.0, 0
skMgr.CreateLine 104.0,-4.0, 0, 101.0,-7.0, 0
skMgr.CreateLine 101.0,-7.0, 0, 89.0, -7.0, 0
skMgr.CreateLine 89.0, -7.0, 0, 86.0, -4.0, 0

' Inner hollow habitable core (wall thickness = 0.85m)
skMgr.CreateLine 86.85, -3.5, 0, 86.85,  3.5, 0
skMgr.CreateLine 86.85,  3.5, 0, 89.5,   6.15, 0
skMgr.CreateLine 89.5,   6.15,0, 100.5,  6.15, 0
skMgr.CreateLine 100.5,  6.15,0, 103.15, 3.5, 0
skMgr.CreateLine 103.15, 3.5, 0, 103.15,-3.5, 0
skMgr.CreateLine 103.15,-3.5, 0, 100.5, -6.15, 0
skMgr.CreateLine 100.5, -6.15,0, 89.5,  -6.15, 0
skMgr.CreateLine 89.5,  -6.15,0, 86.85, -3.5, 0

skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Circumferential Whipple Shield Reinforcement Ribs (upper and lower accent rings)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 0, -50.0, 0, 0, 50.0, 0
skMgr.CreateCornerRectangle 85.5,  3.5, 0, 86.0,  5.5, 0
skMgr.CreateCornerRectangle 85.5, -5.5, 0, 86.0, -3.5, 0
skMgr.CreateCornerRectangle 104.0, 3.5, 0, 104.5, 5.5, 0
skMgr.CreateCornerRectangle 104.0,-5.5, 0, 104.5,-3.5, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

SetAppearance model, 235, 238, 242, 0.6, 0.9, 0.4, 0.2, 0.0 ' Clean Titanium White MLI
SaveAndClose model, "GEO_02_Pressurized_Torus_Hab_Ring"

' ==============================================================================
' MODULE 3: GEO_03_Structural_Spoke_Corridors.SLDPRT (4 Radial Transit Tubes)
' ==============================================================================
WScript.Echo "[3/7] Building GEO_03_Structural_Spoke_Corridors..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' 4 Orthogonal Transit Tubes extending from R = 8.5m to R = 86.0m (Width = 5.0m, Height = 4.0m)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
' Spoke +X
skMgr.CreateCornerRectangle  8.5, -2.5, 0,  86.0, 2.5, 0
' Spoke -X
skMgr.CreateCornerRectangle -86.0,-2.5, 0, -8.5,  2.5, 0
' Spoke +Z
skMgr.CreateCornerRectangle -2.5,  8.5, 0,  2.5,  86.0, 0
' Spoke -Z
skMgr.CreateCornerRectangle -2.5, -86.0, 0, 2.5, -8.5, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 2.0, 2.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Triangular Gusset Reinforcements at Core Junction (R = 8.5m)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -8.0, -8.0, 0, 8.0, 8.0, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 2.5, 2.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 90, 95, 105, 0.7, 0.8, 0.5, 0.2, 0.0 ' Carbon-Composite / Titanium Gray
SaveAndClose model, "GEO_03_Structural_Spoke_Corridors"

' ==============================================================================
' MODULE 4: GEO_04_Geodesic_Biosphere_Spheres.SLDPRT (Eco-Dome Biospheres)
' ==============================================================================
WScript.Echo "[4/7] Building GEO_04_Geodesic_Biosphere_Spheres..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Biosphere Sphere: Center at X = 50.0m, Y = 0, Diameter = 26.0m (Radius = 13.0m)
' Revolve in Front Plane around local vertical centerline at X = 50.0m
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 50.0, -14.0, 0, 50.0, 14.0, 0
' Semi-circle profile
model.Create3PointArc 50.0, -13.0, 0, 50.0, 13.0, 0, 63.0, 0.0, 0
skMgr.CreateLine 50.0, -13.0, 0, 50.0, 13.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Geodesic Exo-Skeleton Ring 1 (Equatorial spaceframe ring, OD = 27.2m, ID = 26.0m, thickness = 0.8m)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 50.0, 0, 0, 13.6
model.CreateCircleByRadius2 50.0, 0, 0, 13.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.5, 0.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Geodesic Exo-Skeleton Ring 2 (Vertical meridional spaceframe ring)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 50.0, 0, 0, 13.6
model.CreateCircleByRadius2 50.0, 0, 0, 13.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.5, 0.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 120, 160, 180, 0.5, 0.9, 0.95, 0.85, 0.45 ' Translucent Silica Glass
SaveAndClose model, "GEO_04_Geodesic_Biosphere_Spheres"

' ==============================================================================
' MODULE 5: GEO_05_Mega_Solar_Photovoltaic_Wings.SLDPRT (Multi-MW Arrays)
' ==============================================================================
WScript.Echo "[5/7] Building GEO_05_Mega_Solar_Photovoltaic_Wings..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Root Pivot Joint: Cylindrical joint along Z-axis (Dia = 3.5m, Length = 18m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 1.75
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 9.0, 9.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 2 Ultra-High-Aspect-Ratio Solar Wings: Span = 95m, Width = 22m, Thickness = 0.35m
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
' Starboard Wing (+X: 10m to 105m, Z: -11m to +11m)
skMgr.CreateCornerRectangle  10.0, -11.0, 0,  105.0, 11.0, 0
' Port Wing (-X: -105m to -10m, Z: -11m to +11m)
skMgr.CreateCornerRectangle -105.0, -11.0, 0, -10.0, 11.0, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.175, 0.175, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Substrate Reinforcement Booms along wing centerlines
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle  10.0, -0.75, 0,  105.0, 0.75, 0
skMgr.CreateCornerRectangle -105.0, -0.75, 0, -10.0, 0.75, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.45, 0.45, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 10, 25, 70, 0.8, 0.9, 0.90, 0.95, 0.0 ' Deep Photovoltaic Sapphire Blue
SaveAndClose model, "GEO_05_Mega_Solar_Photovoltaic_Wings"

' ==============================================================================
' MODULE 6: GEO_06_Communications_Spire_And_RCS_Mast.SLDPRT (Axial Spire)
' ==============================================================================
WScript.Echo "[6/7] Building GEO_06_Communications_Spire_And_RCS_Mast..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Vertical Tapered Spire: Y = 90.0m to 175.0m (Length = 85.0m), Base R = 5.0m, Tip R = 1.1m
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 0, 90.0, 0, 0, 175.0, 0
skMgr.CreateLine 0.0, 90.0,  0, 5.0, 90.0,  0
skMgr.CreateLine 5.0, 90.0,  0, 1.1, 175.0, 0
skMgr.CreateLine 1.1, 175.0, 0, 0.0, 175.0, 0
skMgr.CreateLine 0.0, 175.0, 0, 0.0, 90.0,  0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' 3 Parabolic High-Gain Antennas (Diameter = 8.0m, mounted at Y = 120m, 140m, 160m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 5.0, 120.0, 0, 4.0
model.CreateCircleByRadius2 5.0, 140.0, 0, 3.5
model.CreateCircleByRadius2 4.0, 160.0, 0, 3.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.8, 0.8, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 4 Radial RCS Thruster Outriggers at Y = 130.0m (Span = 18.0m along X and Z)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -18.0, -0.6, 0, 18.0, 0.6, 0
skMgr.CreateCornerRectangle -0.6, -18.0, 0, 0.6, 18.0, 0
skMgr.InsertSketch True
' Offset to Y = 130m
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 1.2, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 240, 240, 245, 0.7, 0.9, 0.5, 0.3, 0.0 ' White Thermal Aerospace Alloy
SaveAndClose model, "GEO_06_Communications_Spire_And_RCS_Mast"

' ==============================================================================
' MODULE 7: GEO_07_Continuous_Tether_Ribbon.SLDPRT (Physical 400m Cable)
' ==============================================================================
WScript.Echo "[7/7] Building GEO_07_Continuous_Tether_Ribbon..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' 1.0m Wide x 0.004m Thick Graphene Ribbon
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -0.50, -0.002, 0, 0.50, 0.002, 0
skMgr.InsertSketch True
' Mid-Plane Extrusion: Total Length = 400.0m (passing through entire station)
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 200.0, 200.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 45, 58, 72, 0.8, 0.8, 0.8, 0.6, 0.0 ' Crystalline Graphene Slate
SaveAndClose model, "GEO_07_Continuous_Tether_Ribbon"

WScript.Echo "ALL 7 GEO ORBITAL STATION MODULES GENERATED SUCCESSFULLY!"
