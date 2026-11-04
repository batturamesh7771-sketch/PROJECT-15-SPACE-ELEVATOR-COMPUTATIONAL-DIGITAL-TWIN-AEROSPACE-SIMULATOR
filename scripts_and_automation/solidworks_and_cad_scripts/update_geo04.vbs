Option Explicit

Dim swApp, partTpl, baseDir, partsDir, stepDir, rendersDir
Dim model, featMgr, skMgr
Dim pi, i, angle, cx, cz

Set swApp = GetObject("", "SldWorks.Application")
If swApp Is Nothing Then
    Set swApp = CreateObject("SldWorks.Application")
End If

swApp.Visible = True
swApp.UserControl = True
swApp.SetUserPreferenceToggle 10, False
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

WScript.Echo "Updating GEO_04_Geodesic_Biosphere_Spheres with 4 Eco-Domes..."
Set model = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = model.SketchManager
Set featMgr = model.FeatureManager

' 4 Spherical Biosphere Domes centered at R = 50m on the 4 spokes (+X, -X, +Z, -Z)
' Eco-Dome 1 (+X at 50, 0, 0)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 50.0, -14.0, 0, 50.0, 14.0, 0
model.Create3PointArc 50.0, -13.0, 0, 50.0, 13.0, 0, 63.0, 0.0, 0
skMgr.CreateLine 50.0, -13.0, 0, 50.0, 13.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Eco-Dome 2 (-X at -50, 0, 0)
model.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine -50.0, -14.0, 0, -50.0, 14.0, 0
model.Create3PointArc -50.0, -13.0, 0, -50.0, 13.0, 0, -37.0, 0.0, 0
skMgr.CreateLine -50.0, -13.0, 0, -50.0, 13.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Eco-Dome 3 (+Z at 0, 0, 50)
model.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 50.0, -14.0, 0, 50.0, 14.0, 0
model.Create3PointArc 50.0, -13.0, 0, 50.0, 13.0, 0, 63.0, 0.0, 0
skMgr.CreateLine 50.0, -13.0, 0, 50.0, 13.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Eco-Dome 4 (-Z at 0, 0, -50)
model.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine -50.0, -14.0, 0, -50.0, 14.0, 0
model.Create3PointArc -50.0, -13.0, 0, -50.0, 13.0, 0, -37.0, 0.0, 0
skMgr.CreateLine -50.0, -13.0, 0, -50.0, 13.0, 0
skMgr.InsertSketch True
featMgr.FeatureRevolve2 True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True

' Equatorial Spaceframe Rings (OD = 27.2m, ID = 26.0m) on all 4 domes
model.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
model.CreateCircleByRadius2  50.0, 0,  0.0, 13.6
model.CreateCircleByRadius2  50.0, 0,  0.0, 13.0
model.CreateCircleByRadius2 -50.0, 0,  0.0, 13.6
model.CreateCircleByRadius2 -50.0, 0,  0.0, 13.0
model.CreateCircleByRadius2   0.0, 0,  50.0, 13.6
model.CreateCircleByRadius2   0.0, 0,  50.0, 13.0
model.CreateCircleByRadius2   0.0, 0, -50.0, 13.6
model.CreateCircleByRadius2   0.0, 0, -50.0, 13.0
skMgr.InsertSketch True
featMgr.FeatureExtrusion2 True, False, False, 0, 0, 0.5, 0.5, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False

SetAppearance model, 120, 160, 180, 0.5, 0.9, 0.95, 0.85, 0.45 ' Translucent Silica Glass

model.ForceRebuild3 False
model.ShowNamedView2 "*Isometric", 7
model.ViewZoomtofit2

Dim partPath, stepPath, pngPath
partPath = partsDir & "\GEO_04_Geodesic_Biosphere_Spheres.SLDPRT"
stepPath = stepDir & "\GEO_04_Geodesic_Biosphere_Spheres.STEP"
pngPath = rendersDir & "\GEO_04_Geodesic_Biosphere_Spheres.PNG"

model.SaveAs3 partPath, 0, 2
model.SaveAs3 stepPath, 0, 2
model.SaveAs3 pngPath, 0, 2
WScript.Echo "GEO_04 updated with all 4 domes successfully!"
swApp.CloseDoc model.GetTitle
