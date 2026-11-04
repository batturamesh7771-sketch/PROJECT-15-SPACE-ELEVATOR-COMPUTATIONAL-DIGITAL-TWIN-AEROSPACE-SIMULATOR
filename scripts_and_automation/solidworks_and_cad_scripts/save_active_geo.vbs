Option Explicit

Dim swApp, model, assy, stepPath, pngPath

Set swApp = GetObject("", "SldWorks.Application")
Set model = swApp.ActiveDoc
If model Is Nothing Then
    WScript.Echo "ERROR: No active document found in SolidWorks"
    WScript.Quit 1
End If

WScript.Echo "Active Document: " & model.GetTitle
Set assy = model
On Error Resume Next
assy.ResolveAllLightWeightComponents True
On Error GoTo 0

assy.ForceRebuild3 False
assy.ShowNamedView2 "*Isometric", 7
assy.ViewZoomtofit2

stepPath = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\ANSYS_Exports_STEP\GEO_Orbital_Terminal_Station_Complete.STEP"
pngPath = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Investor_Renders\GEO_Orbital_Terminal_Station_Isometric.PNG"

model.SaveAs3 stepPath, 0, 2
model.SaveAs3 pngPath, 0, 2
WScript.Echo "Saved STEP: " & stepPath
WScript.Echo "Saved PNG: " & pngPath
WScript.Echo "Active viewport oriented to Isometric and zoomed to fit!"
