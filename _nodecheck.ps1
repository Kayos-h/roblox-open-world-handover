Write-Output ('now ' + (Get-Date).ToString('HH:mm:ss'))
Get-CimInstance Win32_Process -Filter "Name='node.exe' or Name='npx.exe' or Name='cmd.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'robloxstudio|npx|mcp' } | ForEach-Object {
  $cl = $_.CommandLine
  if ($cl.Length -gt 260) { $cl = $cl.Substring(0, 260) }
  ('pid {0} parent {1} {2} :: {3}' -f $_.ProcessId, $_.ParentProcessId, $_.Name, $cl)
}
Write-Output '--- all listeners owned by node ---'
$nodePids = @(Get-Process -Name node -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
Get-NetTCPConnection -ErrorAction SilentlyContinue | Where-Object { $nodePids -contains $_.OwningProcess } | ForEach-Object { ('pid {0} {1} {2}:{3} -> {4}:{5}' -f $_.OwningProcess, $_.State, $_.LocalAddress, $_.LocalPort, $_.RemoteAddress, $_.RemotePort) }
