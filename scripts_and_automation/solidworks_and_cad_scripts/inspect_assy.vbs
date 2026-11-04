Set swApp = CreateObject("SldWorks.Application")
swApp.Visible = True
Dim fileErr, fileWarn
Set doc = swApp.OpenDoc6("C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Assemblies\04_GEO_Orbital_Terminal_Station.SLDASM", 2, 1, "", fileErr, fileWarn)
If doc Is Nothing Then
    WScript.Echo "Failed to open assembly. Error: " & fileErr
Else
    WScript.Echo "Assembly opened: " & doc.GetTitle
    comps = doc.GetComponents(False)
    If IsArray(comps) Then
        WScript.Echo "Components count: " & (UBound(comps) + 1)
        For i = 0 To UBound(comps)
            Set c = comps(i)
            WScript.Echo " - " & c.Name2 & " (Path: " & c.GetPathName & ")"
        Next
    Else
        WScript.Echo "No components found!"
    End If
End If
