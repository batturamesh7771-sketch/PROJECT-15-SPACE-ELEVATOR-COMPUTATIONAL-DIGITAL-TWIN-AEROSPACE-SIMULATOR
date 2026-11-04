Option Explicit
Dim swApp, doc, errs, warns

Set swApp = CreateObject("SldWorks.Application")
swApp.Visible = True
swApp.UserControl = True

errs = CLng(0)
warns = CLng(0)
On Error Resume Next
Set doc = swApp.OpenDoc6("C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Assemblies\00_Space_Elevator_Master_Showcase.SLDASM", 2, 1, "", errs, warns)
If Not doc Is Nothing Then
    doc.ShowNamedView2 "*Isometric", 7
    doc.ViewZoomtofit2
End If
WScript.Echo "Showcase assembly opened in SolidWorks GUI!"
