Option Explicit
Dim swApp, doc, bodies, feat
Set swApp = GetObject("", "SldWorks.Application")
Set doc = swApp.OpenDoc6("C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Parts_GEO\test_sphere.SLDPRT", 1, 1, "", 0, 0)
If doc Is Nothing Then
    WScript.Echo "Doc not found"
Else
    bodies = doc.GetBodies2(-1, True)
    If IsArray(bodies) Then
        WScript.Echo "Bodies count: " & (UBound(bodies) + 1)
        For Each b In bodies
            WScript.Echo "Body type: " & b.GetType & " | Solid: " & b.IsSolidBody
        Next
    Else
        WScript.Echo "No bodies found!"
    End If
End If
swApp.CloseDoc doc.GetTitle
