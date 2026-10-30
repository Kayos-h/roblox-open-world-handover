Write-Output ("now: " + (Get-Date).ToString('HH:mm:ss'))
Write-Output '--- headless blender (v4worker) processes ---'
Get-CimInstance Win32_Process -Filter "Name='blender.exe'" | ForEach-Object {
  $p = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
  $cmd = [string]$_.CommandLine
  $kind = 'GUI (user window)'
  if ($cmd -match 'v4worker\.py') { $kind = 'headless' }
  $w = ''
  if ($cmd -match 'v4worker\.py"?\s+--\s+(\S+)\s+(\S+)') { $w = $Matches[1] + ' / worker ' + $Matches[2] }
  Write-Output ("pid " + $_.ProcessId + "  start " + $_.CreationDate.ToString('HH:mm:ss') + "  cpu " + [math]::Round($p.CPU, 1) + "s  mem " + [math]::Round($p.WorkingSet64 / 1MB) + "MB  " + $kind + "  " + $w)
}
Write-Output '--- v4run.ps1 launcher processes (waiting for a slot or for blender) ---'
Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { [string]$_.CommandLine -match 'v4run\.ps1' } | ForEach-Object {
  $cmd = [string]$_.CommandLine
  $w = ''; if ($cmd -match '-Worker\s+(\S+)') { $w = $Matches[1] }
  $m = ''; if ($cmd -match '-Module\s+(\S+)') { $m = $Matches[1] }
  Write-Output ("pid " + $_.ProcessId + "  start " + $_.CreationDate.ToString('HH:mm:ss') + "  worker " + $w + "  module " + $m)
}
Write-Output '--- slot semaphore probe ---'
try {
  $s = [System.Threading.Semaphore]::OpenExisting('v4blender_slots')
  $got = $s.WaitOne(0)
  if ($got) { [void]$s.Release(); Write-Output 'a slot is FREE right now (probe released it again)' } else { Write-Output 'NO free slot right now (both slots are held or leaked)' }
} catch { Write-Output ('semaphore not open (nobody holds it): ' + $_.Exception.Message) }
Write-Output '--- newest run logs ---'
Get-ChildItem 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_work' -Filter 'run_w*.log' | Sort-Object LastWriteTime -Descending | Select-Object -First 8 | ForEach-Object { Write-Output ($_.Name + "  " + $_.LastWriteTime.ToString('HH:mm:ss') + "  " + $_.Length + " bytes") }
