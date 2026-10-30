# Read-only diagnosis of the Blender MCP link (port 9876). Prints facts only; changes nothing.
Write-Output "=== Blender process"
Get-Process blender -ErrorAction SilentlyContinue | Select-Object Id, Responding, CPU, WorkingSet64 | Format-Table -AutoSize | Out-String -Width 200

Write-Output "=== Connections ON port 9876 (the add-on side)"
Get-NetTCPConnection -LocalPort 9876 -ErrorAction SilentlyContinue | Select-Object State, LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess | Format-Table -AutoSize | Out-String -Width 200

Write-Output "=== Connections TO port 9876 (the MCP server side)"
Get-NetTCPConnection -RemotePort 9876 -ErrorAction SilentlyContinue | Select-Object State, LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess | Format-Table -AutoSize | Out-String -Width 200

Write-Output "=== Helper processes whose command line mentions blender (not Blender itself)"
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'blender' -and $_.Name -notmatch '^blender' } | Select-Object ProcessId, ParentProcessId, Name, CreationDate, CommandLine | Format-List | Out-String -Width 250

Write-Output "=== uv / uvx / mcp processes"
Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '^(uv|uvx|mcp)' } | Select-Object Id, ProcessName, StartTime | Format-Table -AutoSize | Out-String -Width 200

Write-Output "=== Socket probe (2 s timeout, connect then close)"
try {
  $c = New-Object System.Net.Sockets.TcpClient
  $iar = $c.BeginConnect('127.0.0.1', 9876, $null, $null)
  $ok = $iar.AsyncWaitHandle.WaitOne(2000)
  if ($ok -and $c.Connected) { Write-Output "connect OK: something accepts connections on 9876" } else { Write-Output "connect FAILED or timed out" }
  $c.Close()
} catch { Write-Output ("probe error: " + $_.Exception.Message) }
