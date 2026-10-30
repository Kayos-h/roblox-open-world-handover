$p = Get-CimInstance Win32_Process -Filter "Name='cmd.exe'" | Where-Object { $_.CommandLine -like '*bridge_server.bat*' }
foreach ($x in $p) { Stop-Process -Id $x.ProcessId -Force; 'stopped loop pid ' + $x.ProcessId }
$k = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { $_.CommandLine -like '*keepalive.ps1*' }
'keepalive running: ' + [bool]$k
$w = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { $_.CommandLine -like '*upload_after_export*' -or $_.CommandLine -like '*upload_all*' }
'upload processes: ' + (($w | ForEach-Object { $_.ProcessId }) -join ',')
Get-Content 'C:\Users\Nitro\.kiro\crew\workspace\town\asset_ids.csv' | Measure-Object -Line | ForEach-Object { 'asset_ids.csv lines: ' + $_.Lines }
