Write-Output ('now ' + (Get-Date).ToString('HH:mm:ss'))
Write-Output '--- listeners on 58741 / 3002 / 34872 ---'
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in 58741, 3002, 34872 } | ForEach-Object {
  $p = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
  ('port {0} pid {1} {2}' -f $_.LocalPort, $_.OwningProcess, $p.ProcessName)
}
Write-Output '--- established connections into 58741 ---'
Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -eq 58741 -or $_.RemotePort -eq 58741 } | ForEach-Object {
  ('local {0}:{1} remote {2}:{3} pid {4}' -f $_.LocalAddress, $_.LocalPort, $_.RemoteAddress, $_.RemotePort, $_.OwningProcess)
}
Write-Output '--- node / npx processes ---'
Get-Process -Name node -ErrorAction SilentlyContinue | ForEach-Object { ('node pid {0} started {1} MB {2}' -f $_.Id, $_.StartTime.ToString('HH:mm:ss'), [math]::Round($_.WorkingSet64/1MB)) }
Write-Output '--- memory freeer running? ---'
Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'memory' } | ForEach-Object { ('pid {0} {1}' -f $_.ProcessId, $_.CommandLine) }
Write-Output '--- health ---'
foreach ($u in 'http://localhost:58741/health', 'http://localhost:58741/status', 'http://127.0.0.1:58741/health', 'http://localhost:3002/health') {
  try { $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 4; Write-Output ($u + ' -> ' + $r.StatusCode + ' ' + $r.Content.Substring(0, [Math]::Min(300, $r.Content.Length))) } catch { Write-Output ($u + ' -> ' + $_.Exception.Message) }
}
