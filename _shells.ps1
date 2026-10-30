Write-Output ("now " + (Get-Date).ToString('HH:mm:ss'))
$procs = Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(powershell|pwsh|cmd|conhost)\.exe$' }
foreach ($p in ($procs | Sort-Object CreationDate)) {
  $gp = Get-Process -Id $p.ProcessId -ErrorAction SilentlyContinue
  $cmd = [string]$p.CommandLine
  if ($cmd.Length -gt 110) { $cmd = $cmd.Substring(0, 110) + '...' }
  $cpu = ''; if ($gp) { $cpu = [math]::Round($gp.CPU, 1) }
  $par = Get-CimInstance Win32_Process -Filter ("ProcessId=" + $p.ParentProcessId) -ErrorAction SilentlyContinue
  $pn = ''; if ($par) { $pn = $par.Name }
  Write-Output ($p.CreationDate.ToString('HH:mm:ss') + "  pid " + $p.ProcessId + "  " + $p.Name + "  parent " + $p.ParentProcessId + " (" + $pn + ")  cpu " + $cpu + "s  cmd: " + $cmd)
}
