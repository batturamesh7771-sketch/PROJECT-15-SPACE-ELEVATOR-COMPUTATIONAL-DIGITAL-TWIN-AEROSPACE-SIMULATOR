Option Explicit
Dim swApp, model, assy, stepPath, pngPath, errs, warns

Set swApp = GetObject("", "SldWorks.Application")
Set model = swApp.ActiveDoc
If model Is Nothing Then
    Set model = swApp.OpenDoc6("C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Assemblies\04_GEO_Orbital_Terminal_Station.SLDASM", 2, 1, "", errs, warns)
End If

Set assy = model
assy.ResolveAllLightWeightComponents True
assy.ForceRebuild3 False
assy.ShowNamedView2 "*Isometric", 7
assy.ViewZoomtofit2

stepPath = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\ANSYS_Exports_STEP\GEO_Orbital_Terminal_Station_Complete.STEP"
pngPath = "C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Investor_Renders\GEO_Orbital_Terminal_Station_Isometric.PNG"

model.SaveAs3 stepPath, 0, 2
model.SaveAs3 pngPath, 0, 2

WScript.Echo "STEP and PNG re-exported with resolved geometry!"
