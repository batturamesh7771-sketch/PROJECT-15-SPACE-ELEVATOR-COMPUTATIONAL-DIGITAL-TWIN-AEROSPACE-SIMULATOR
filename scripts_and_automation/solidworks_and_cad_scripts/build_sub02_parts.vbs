Option Explicit

Dim swApp, partTpl, baseDir, partsDir, stepDir, rendersDir
Dim model, featMgr, skMgr, sel, feat
Dim pi, r_out, r_in, angle, i, x1, z1, x2, z2

Set swApp = GetObject("", "SldWorks.Application")
If swApp Is Nothing Then
    Set swApp = CreateObject("SldWorks.Application")
End If

swApp.Visible = True
swApp.UserControl = True
swApp.SetUserPreferenceToggle 10, False ' swInputDimValOnCreate = False

partTpl = swApp.GetUserPreferenceStringValue(8)
baseDir = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
partsDir = baseDir & "\Parts"
stepDir = baseDir & "\ANSYS_Exports_STEP"
rendersDir = baseDir & "\Renders"
pi = 3.14159265358979

Sub SetAppearance(doc, r, g, b)
    Dim p(8)
    p(0) = r / 255.0
    p(1) = g / 255.0
    p(2) = b / 255.0
    p(3) = 0.6
    p(4) = 0.8
    p(5) = 0.5
    p(6) = 0.3
    p(7) = 0.0
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
' 1. CL_01_Hex_Composite_Chassis.SLDPRT
' ==============================================================================
WScript.Echo "Building CL_01_Hex_Composite_Chassis..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Outer hex profile (R = 1.8475 m -> width across flats = 3.2 m)
' Inner hex profile (R = 1.755 m -> wall thickness = 0.08 m)
' Central tether passage slot: 1.30m x 0.30m (X: -0.65 to 0.65, Z: -0.15 to 0.15)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True

r_out = 1.84752
r_in = 1.75514

For i = 0 To 5
    x1 = r_out * Cos((i * 60 + 30) * pi / 180.0)
    z1 = r_out * Sin((i * 60 + 30) * pi / 180.0)
    x2 = r_out * Cos(((i + 1) * 60 + 30) * pi / 180.0)
    z2 = r_out * Sin(((i + 1) * 60 + 30) * pi / 180.0)
    skMgr.CreateLine x1, z1, 0, x2, z2, 0
Next

For i = 0 To 5
    x1 = r_in * Cos((i * 60 + 30) * pi / 180.0)
    z1 = r_in * Sin((i * 60 + 30) * pi / 180.0)
    x2 = r_in * Cos(((i + 1) * 60 + 30) * pi / 180.0)
    z2 = r_in * Sin(((i + 1) * 60 + 30) * pi / 180.0)
    skMgr.CreateLine x1, z1, 0, x2, z2, 0
Next

' Central tether channel slot
skMgr.CreateCornerRectangle -0.65, -0.15, 0, 0.65, 0.15, 0

skMgr.InsertSketch True
' Extrude 5.0m height
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 5.0, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Front and rear inspection / roller access windows (1.4m x 3.6m, Y = 0.7 to 4.3m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -0.70, 0.70, 0, 0.70, 4.30, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 2.0, 2.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 30, 30, 35 ' Aerospace Carbon Fiber Composite
SaveAndClose model, "CL_01_Hex_Composite_Chassis"

' ==============================================================================
' 2. CL_02_Pinch_Drive_Roller.SLDPRT
' ==============================================================================
WScript.Echo "Building CL_02_Pinch_Drive_Roller..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Drum: Diameter = 0.40m (R = 0.20m), Active Width = 1.10m (X: -0.55 to +0.55m)
model.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 0.20
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.55, 0.55, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Shafts: Diameter = 0.12m (R = 0.06m), Length = 0.25m each side (Total X: -0.80 to +0.80m)
model.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 0.06
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.80, 0.80, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Hub Motor Housings: Diameter = 0.36m (R = 0.18m), Width = 0.18m (X: -0.98 to -0.80 and +0.80 to +0.98m)
model.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 0.18
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.98, 0.98, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 190, 140, 50 ' High-Friction DLC/Titanium Gold
SaveAndClose model, "CL_02_Pinch_Drive_Roller"

' ==============================================================================
' 3. CL_03_Hydraulic_Clamping_Actuator_Yoke.SLDPRT
' ==============================================================================
WScript.Echo "Building CL_03_Hydraulic_Clamping_Actuator_Yoke..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Actuator Block: 1.40m wide (X: -0.70 to +0.70), 0.45m high (Y: -0.225 to +0.225), 0.60m deep (Z: 0 to 0.60m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -0.70, -0.225, 0, 0.70, 0.225, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 0.60, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Twin Cylinder Bores (Diameter = 0.24m, R = 0.12m at X = -0.35 and +0.35m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 -0.35, 0, 0, 0.12
model.CreateCircleByRadius2  0.35, 0, 0, 0.12
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 0.15, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 185, 35, 35 ' Anodized Aerospace Red
SaveAndClose model, "CL_03_Hydraulic_Clamping_Actuator_Yoke"

' ==============================================================================
' 4. CL_04_Thermal_Radiator_Wing.SLDPRT
' ==============================================================================
WScript.Echo "Building CL_04_Thermal_Radiator_Wing..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Main Wing Panel: Span = 3.5m (X: 0 to 3.5m), Height = 4.2m (Y: 0 to 4.2m), Thickness = 0.04m (Z: -0.02 to +0.02m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle 0.0, 0.0, 0, 3.5, 4.2, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.02, 0.02, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 12 Longitudinal cooling heat-pipe ribs
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
For i = 1 To 12
    skMgr.CreateCornerRectangle 0.25 * i - 0.02, 0.1, 0, 0.25 * i + 0.02, 4.1, 0
Next
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.035, 0.035, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 220, 225, 235 ' Silver Specular Radiator
SaveAndClose model, "CL_04_Thermal_Radiator_Wing"

' ==============================================================================
' 5. CL_05_Laser_PV_Receiver_Dish.SLDPRT
' ==============================================================================
WScript.Echo "Building CL_05_Laser_PV_Receiver_Dish..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Photovoltaic Receiver Array: OD = 9.0m (R = 4.5m), Aperture = 1.6m (R = 0.8m), Thickness = 0.10m
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 4.50
model.CreateCircleByRadius2 0, 0, 0, 0.80
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.10, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' 8 Radial support struts
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
For i = 0 To 7
    angle = i * 45.0 * pi / 180.0
    x1 = 1.0 * Cos(angle)
    z1 = 1.0 * Sin(angle)
    x2 = 4.3 * Cos(angle)
    z2 = 4.3 * Sin(angle)
    skMgr.CreateCornerRectangle x1 - 0.08, z1 - 0.08, 0, x2 + 0.08, z2 + 0.08, 0
Next
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 0.35, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 20, 60, 160 ' Deep Photovoltaic Sapphire Blue
SaveAndClose model, "CL_05_Laser_PV_Receiver_Dish"

WScript.Echo "All Sub-Assembly 02 parts built successfully!"
