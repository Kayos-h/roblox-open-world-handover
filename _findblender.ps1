$p = Get-Process blender -ErrorAction SilentlyContinue | Select-Object -First 1
if ($p) { Write-Output ("running: " + $p.Path + "  pid " + $p.Id) } else { Write-Output "blender not running" }
$cands = @("C:\Program Files\Blender Foundation", "C:\Program Files (x86)\Steam\steamapps\common\Blender")
foreach ($c in $cands) { if (Test-Path $c) { Get-ChildItem $c -Directory | ForEach-Object { Write-Output ("found dir: " + $_.FullName) } } }
Write-Output ("python: " + (Get-Command python -ErrorAction SilentlyContinue).Source)
$gpu = Get-CimInstance Win32_VideoController | Select-Object -First 2 Name, AdapterRAM
$gpu | Format-Table -AutoSize | Out-String
