On Error Resume Next
Dim sw, count
count = 0
Do While True
    Set sw = GetObject(, "SldWorks.Application")
    If Err.Number <> 0 Or sw Is Nothing Then Exit Do
    sw.ExitApp
    Set sw = Nothing
    count = count + 1
    WScript.Sleep 500
    If count > 20 Then Exit Do
Loop
WScript.Echo "Exited " & count & " SolidWorks instances cleanly via COM"
