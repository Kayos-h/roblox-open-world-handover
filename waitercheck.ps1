$p = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { $_.CommandLine -like '*upload_after_export*' }
if ($p) { 'upload waiter running, pid ' + ($p.ProcessId -join ',') } else { 'upload waiter NOT running' }
