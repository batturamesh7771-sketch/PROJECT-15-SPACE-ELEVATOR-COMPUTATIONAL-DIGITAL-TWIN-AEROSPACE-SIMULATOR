Option Explicit

Dim swApp, partTpl, baseDir, partsDir, stepDir, rendersDir
Dim model, featMgr, skMgr, sel, feat
Dim matProps(8)

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

Sub SetAppearance(doc, r, g, b)
    Dim p(8)
    p(0) = r / 255.0
    p(1) = g / 255.0
    p(2) = b / 255.0
    p(3) = 0.6 ' Ambient
    p(4) = 0.8 ' Diffuse
    p(5) = 0.5 ' Specular
    p(6) = 0.3 ' Shininess
    p(7) = 0.0 ' Transparency
    p(8) = 0.0 ' Emission
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
' 1. EP_01_SemiSubmersible_Hull.SLDPRT
' ==============================================================================
WScript.Echo "Building EP_01_SemiSubmersible_Hull..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Pontoon 1 (Z: -40 to -24, X: -50 to +50, Height: 10m from Y = -38 to -28)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -50.0, -40.0, 0, 50.0, -24.0, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 10.0, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Pontoon 2 (Z: +24 to +40, X: -50 to +50, Height: 10m from Y = -38 to -28)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -50.0, 24.0, 0, 50.0, 40.0, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 10.0, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Four stability columns (Diameter = 14m, Height = 28m up to Y = 0)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 -32.0, -32.0, 0, 7.0
model.CreateCircleByRadius2  32.0, -32.0, 0, 7.0
model.CreateCircleByRadius2 -32.0,  32.0, 0, 7.0
model.CreateCircleByRadius2  32.0,  32.0, 0, 7.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 28.0, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Deck with integrated Moonpool hole (84m x 84m with 28m diameter central circle, Y = 0 to 5m)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -42.0, -42.0, 0, 42.0, 42.0, 0
model.CreateCircleByRadius2 0, 0, 0, 14.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 5.0, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 35, 55, 75 ' Dark Marine Epoxy Steel
SaveAndClose model, "EP_01_SemiSubmersible_Hull"

' ==============================================================================
' 2. EP_02_Outer_Gimbal_Ring.SLDPRT
' ==============================================================================
WScript.Echo "Building EP_02_Outer_Gimbal_Ring..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Outer Ring: OD = 26m (R=13), ID = 21m (R=10.5), Height = 3.5m (Y = 0.75 to 4.25)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 13.0
model.CreateCircleByRadius2 0, 0, 0, 10.5
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 3.5, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' External Trunnion Pins along X-axis (Diameter = 1.8m, Length = 2.0m on each side)
model.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 1.75, 0, 0.9
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 15.0, 15.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 215, 165, 30 ' Safety Industrial Gold
SaveAndClose model, "EP_02_Outer_Gimbal_Ring"

' ==============================================================================
' 3. EP_03_Inner_Gimbal_And_Capstan_Hub.SLDPRT
' ==============================================================================
WScript.Echo "Building EP_03_Inner_Gimbal_And_Capstan_Hub..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Inner Ring: OD = 19.5m (R = 9.75), ID = 14.0m (R = 7.0), Height = 3.5m
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 0, 0, 9.75
model.CreateCircleByRadius2 0, 0, 0, 7.00
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 3.5, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' External Trunnions along Z-axis (Diameter = 1.6m, R = 0.8, at Y = 1.75m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 0, 1.75, 0, 0.8
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 11.25, 11.25, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Winch Bridge Structure with central fairlead opening (1.2m x 0.2m)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -7.0, -2.5, 0, -0.6, 2.5, 0
skMgr.CreateCornerRectangle  0.6, -2.5, 0,  7.0, 2.5, 0
skMgr.CreateCornerRectangle -0.6,  0.1, 0,  0.6, 2.5, 0
skMgr.CreateCornerRectangle -0.6, -2.5, 0,  0.6, -0.1, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 1.5, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Dual Winch Drums (Diameter = 3.0m, R = 1.5m at X = -2.5 and +2.5, Width = 2.5m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2 -2.5, 1.75, 0, 1.5
model.CreateCircleByRadius2  2.5, 1.75, 0, 1.5
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 1.25, 1.25, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 160, 165, 175 ' Brushed Titanium
SaveAndClose model, "EP_03_Inner_Gimbal_And_Capstan_Hub"

' ==============================================================================
' 4. EP_04_Lightning_And_Wind_Arrestor_Tower.SLDPRT
' ==============================================================================
WScript.Echo "Building EP_04_Lightning_And_Wind_Arrestor_Tower..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Tapered cone: Base OD = 14m (R = 7.0), Base ID = 13.5m (R = 6.75)
' Top Exit OD = 3.0m (R = 1.5), Top ID = 2.5m (R = 1.25), Height = 35m
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 0, 0, 0, 0, 35.0, 0
skMgr.CreateLine 6.75, 0.0, 0, 1.25, 35.0, 0
skMgr.CreateLine 1.25, 35.0, 0, 1.50, 35.0, 0
skMgr.CreateLine 1.50, 35.0, 0, 7.00, 0.0, 0
skMgr.CreateLine 7.00, 0.0, 0, 6.75, 0.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' 4 Radial inspection cutouts
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -1.2, 12.0, 0, 1.2, 18.0, 0
skMgr.CreateCornerRectangle -0.8, 22.0, 0, 0.8, 28.0, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 10.0, 10.0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 200, 205, 210 ' Marine White Structural Alloy
SaveAndClose model, "EP_04_Lightning_And_Wind_Arrestor_Tower"

WScript.Echo "All Sub-Assembly 01 parts built successfully!"
