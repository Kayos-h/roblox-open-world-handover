"--- port 58741 ---"
Get-NetTCPConnection -LocalPort 58741 -ErrorAction SilentlyContinue | Select-Object State,OwningProcess | Format-Table -AutoSize | Out-String
"--- node ---"
Get-Process node -ErrorAction SilentlyContinue | Select-Object Id,StartTime | Format-Table -AutoSize | Out-String
"--- studio ---"
Get-Process RobloxStudioBeta -ErrorAction SilentlyContinue | Select-Object Id,StartTime,MainWindowTitle | Format-Table -AutoSize | Out-String
"--- python (memory freeer?) ---"
Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'" | Select-Object ProcessId,CommandLine | Format-List | Out-String
"--- cmd windows (bridge bat) ---"
Get-CimInstance Win32_Process -Filter "Name='cmd.exe'" | Where-Object { $_.CommandLine -match 'bridge|robloxstudio' } | Select-Object ProcessId,CommandLine | Format-List | Out-String
