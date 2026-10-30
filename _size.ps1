$t = 'C:\Users\Nitro\.kiro\crew\workspace\town'
function SizeMB($p) { $s = (Get-ChildItem -LiteralPath $p -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum; [math]::Round($s / 1MB, 1) }
Write-Output '--- town subfolders (MB) ---'
Get-ChildItem -LiteralPath $t -Directory -Force | ForEach-Object { '{0,10}  {1}' -f (SizeMB $_.FullName), $_.Name }
Write-Output '--- library subfolders (MB) ---'
Get-ChildItem -LiteralPath (Join-Path $t 'library') -Directory -Force | ForEach-Object { '{0,10}  {1}' -f (SizeMB $_.FullName), $_.Name }
$b1 = Get-ChildItem -LiteralPath $t -Recurse -File -Force -Filter '*.blend1' -ErrorAction SilentlyContinue | Measure-Object Length -Sum
Write-Output ('blend1 files: {0}  {1} MB' -f $b1.Count, [math]::Round($b1.Sum / 1MB, 1))
$lg = Get-ChildItem -LiteralPath $t -Recurse -File -Force -Include '*.log' -ErrorAction SilentlyContinue | Measure-Object Length -Sum
Write-Output ('log files: {0}  {1} MB' -f $lg.Count, [math]::Round($lg.Sum / 1MB, 1))
$tot = (Get-ChildItem -LiteralPath $t -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum)
Write-Output ('TOTAL town: {0} files, {1} MB' -f $tot.Count, [math]::Round($tot.Sum / 1MB, 1))
$d = Get-PSDrive -Name C
Write-Output ('C: free {0} GB' -f [math]::Round($d.Free / 1GB, 1))
Write-Output ('Desktop exists roblox_backup already: ' + (Test-Path 'C:\Users\Nitro\Desktop\roblox_backup'))
