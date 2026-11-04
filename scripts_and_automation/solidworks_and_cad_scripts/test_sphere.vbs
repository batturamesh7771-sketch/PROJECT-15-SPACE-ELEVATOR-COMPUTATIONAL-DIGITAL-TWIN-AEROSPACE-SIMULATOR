Option Explicit

Dim swApp, partTpl, doc, skMgr, featMgr
Dim baseDir, testPath, pngPath, feat

Set swApp = GetObject("", "SldWorks.Application")
swApp.Visible = True
swApp.UserControl = True
swApp.SetUserPreferenceToggle 10, False
swApp.SetUserPreferenceIntegerValue 192, 1

partTpl = swApp.GetUserPreferenceStringValue(8)
baseDir = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1"
testPath = baseDir & "\Parts_GEO\test_sphere.SLDPRT"
pngPath = baseDir & "\Investor_Renders\test_sphere.PNG"

Set doc = swApp.NewDocument(partTpl, 0, 0, 0)
Set skMgr = doc.SketchManager
Set featMgr = doc.FeatureManager

doc.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
skMgr.InsertSketch True
skMgr.CreateCenterLine 0, -25.0, 0, 0, 25.0, 0
skMgr.CreateArc 0, 0, 0, 0, -13.0, 0, 0, 13.0, 0, 1
skMgr.CreateLine 0, 13.0, 0, 0, -13.0, 0
skMgr.InsertSketch True

Set feat = featMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.283185307, 0, False, False, 0.0, 0.0, 0, 0, 0, True, True, True)
If feat Is Nothing Then
    WScript.Echo "Revolve returned Nothing!"
Else
    WScript.Echo "Revolve created feature: " & feat.Name
End If

doc.ShowNamedView2 "*Isometric", 7
doc.ViewZoomtofit2
doc.SaveAs3 testPath, 0, 2
doc.SaveAs3 pngPath, 0, 2
swApp.CloseDoc doc.GetTitle
