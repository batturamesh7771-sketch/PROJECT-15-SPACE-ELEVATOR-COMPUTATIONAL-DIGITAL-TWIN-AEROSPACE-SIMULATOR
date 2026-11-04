Set swApp = CreateObject("SldWorks.Application")
Set doc = swApp.ActiveDoc
If doc Is Nothing Then
    WScript.Echo "No active doc"
Else
    WScript.Echo "Active doc title: " & doc.GetTitle
    WScript.Echo "Doc type: " & doc.GetType
    If doc.GetType = 2 Then ' Assembly
        comps = doc.GetComponents(False)
        WScript.Echo "Component count: " & UBound(comps) + 1
        For i = 0 To UBound(comps)
            Set comp = comps(i)
            WScript.Echo "Comp " & i & ": " & comp.Name2 & " | Suppressed: " & comp.IsSuppressed & " | Hidden: " & comp.IsHidden(False)
        Next
    End If
End If
