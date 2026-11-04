Option Explicit

Dim swApp, partTpl, baseDir, partsDir, stepDir, rendersDir
Dim model, featMgr, skMgr, custPropMgr, sel, feat
Dim pi

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
' 1. TE_01_Graphene_Tether_Segment_10m.SLDPRT
' ==============================================================================
WScript.Echo "Building TE_01_Graphene_Tether_Segment_10m..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Ribbon Cross-section: Width = 1.00m (X: -0.50 to +0.50), Thickness = 0.004m (Z: -0.002 to +0.002)
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle -0.50, -0.002, 0, 0.50, 0.002, 0
skMgr.InsertSketch True

' Extrude 10.0m vertically along Y
featMgr.FeatureExtrusion2 True, False, True, 0, 0, 10.0, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Add Pearson-Aravind Custom Properties
Set custPropMgr = model.Extension.CustomPropertyManager("")
custPropMgr.Add3 "Material_Baseline", 30, "Single-Crystal Graphene Super-Laminate (rho=2260 kg/m^3, sigma_work=65 GPa)", 1
custPropMgr.Add3 "Characteristic_Length_Lc", 30, "2935.4 km", 1
custPropMgr.Add3 "Max_Taper_Ratio_GEO", 30, "5.40", 1
custPropMgr.Add3 "Base_Area_As", 30, "3.76 mm^2", 1
custPropMgr.Add3 "GEO_Area_Ag", 30, "20.29 mm^2", 1

SetAppearance model, 55, 65, 80 ' Graphene metallic slate
SaveAndClose model, "TE_01_Graphene_Tether_Segment_10m"

' ==============================================================================
' 2. AP_01_Apex_Counterweight_Core.SLDPRT
' ==============================================================================
WScript.Echo "Building AP_01_Apex_Counterweight_Core..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Central pressure vessel + dual docking cones (Diameter 16m, length 24m, end cones 4m each)
' Total height = 32m (Y: -16 to +16m). Revolve around Y axis in Front Plane.
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 0, -16.0, 0, 0, 16.0, 0

skMgr.CreateLine 0.0, -16.0, 0, 3.0, -16.0, 0
skMgr.CreateLine 3.0, -16.0, 0, 8.0, -12.0, 0
skMgr.CreateLine 8.0, -12.0, 0, 8.0,  12.0, 0
skMgr.CreateLine 8.0,  12.0, 0, 3.0,  16.0, 0
skMgr.CreateLine 3.0,  16.0, 0, 0.0,  16.0, 0
skMgr.CreateLine 0.0,  16.0, 0, 0.0, -16.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' 4 Radial Solar Array Booms (Length = 28m, Width = 6m, Thickness = 0.25m)
' Booms 1 & 2 along X-axis
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCornerRectangle  8.0, -3.0, 0,  36.0, 3.0, 0
skMgr.CreateCornerRectangle -36.0, -3.0, 0, -8.0, 3.0, 0
' Booms 3 & 4 along Z-axis
skMgr.CreateCornerRectangle -3.0,   8.0, 0,  3.0,  36.0, 0
skMgr.CreateCornerRectangle -3.0, -36.0, 0,  3.0,  -8.0, 0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.125, 0.125, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 230, 230, 235 ' White Thermal Ceramic / Mylar
SaveAndClose model, "AP_01_Apex_Counterweight_Core"

' ==============================================================================
' 3. AP_02_Peet_Interplanetary_Sling_Ramp.SLDPRT
' ==============================================================================
WScript.Echo "Building AP_02_Peet_Interplanetary_Sling_Ramp..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' Curved Guideway (Curvature radius = 45m, Length = 35m, Channel width = 3.6m, Rail height = 1.2m)
' Base structural guideway extruded along Z: Channel width = 3.6m (Z: -1.8 to +1.8m)
' Profile in Front Plane (X-Y):
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True

' Curved ramp profile (X: 0 to 30m, Y: -10 to 5m)
skMgr.CreateLine 0.0, 0.0, 0, 25.0, 10.0, 0
skMgr.CreateLine 25.0, 10.0, 0, 35.0, 18.0, 0
skMgr.CreateLine 35.0, 18.0, 0, 34.5, 19.0, 0
skMgr.CreateLine 34.5, 19.0, 0, 24.5, 11.2, 0
skMgr.CreateLine 24.5, 11.2, 0, 0.0, 1.2, 0
skMgr.CreateLine 0.0, 1.2, 0, 0.0, 0.0, 0
skMgr.InsertSketch True

' Extrude channel bed 3.6m wide (Z: -1.8 to +1.8m)
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 1.8, 1.8, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

' Twin Guide Rails (Height = 1.2m on both sides at Z = -1.8 and +1.8m)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateLine 0.0, 1.2, 0, 24.5, 11.2, 0
skMgr.CreateLine 24.5, 11.2, 0, 34.5, 19.0, 0
skMgr.CreateLine 34.5, 19.0, 0, 34.0, 20.2, 0
skMgr.CreateLine 34.0, 20.2, 0, 24.0, 12.4, 0
skMgr.CreateLine 24.0, 12.4, 0, 0.0, 2.4, 0
skMgr.CreateLine 0.0, 2.4, 0, 0.0, 1.2, 0
skMgr.InsertSketch True

' Extrude rails as thin outer flanges (offset 1.8m)
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 1.8, 1.8, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 170, 175, 185 ' Structural Titanium
SaveAndClose model, "AP_02_Peet_Interplanetary_Sling_Ramp"

WScript.Echo "All Sub-Assembly 03 parts built successfully!"
