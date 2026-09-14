Public Sub CheckUserStatuses()
    Dim db As DAO.Database
    Dim rs As DAO.Recordset
    Dim strSQL As String
    Dim activeCount As Long
    
    On Error GoTo ErrorHandler
    
    Set db = CurrentDb()
    strSQL = "SELECT UserID, UserName, IsActive, LastLogin FROM tblUsers WHERE IsActive = True"
    Set rs = db.OpenRecordset(strSQL, dbOpenSnapshot)
    
    activeCount = 0
    
    If Not rs.BOF And Not rs.EOF Then
        rs.MoveFirst
        Do Until rs.EOF
            activeCount = activeCount + 1
            Debug.Print "Processing user: " & rs!UserName & " (ID: " & rs!UserID & ")"
            
            If IsNull(rs!LastLogin) Then
                MsgBox "Внимание: Пользователь " & rs!UserName & " еще не заходил в систему!", vbExclamation, "Системный алерт"
            End If
            
            rs.MoveNext
        Loop
    End If
    
    MsgBox "Проверка завершена. Всего активных сотрудников найдено: " & activeCount, vbInformation, "Успех"

ExitProcedure:
    On Error Resume Next
    If Not rs Is Nothing Then rs.Close: Set rs = Nothing
    Set db = Nothing
    Exit Sub

ErrorHandler:
    MsgBox "Произошла критическая ошибка: " & Err.Description, vbCritical, "Ошибка бэкенда"
    Resume ExitProcedure
End Sub

