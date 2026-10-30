# photo round 5 (after the round-4 fixes). Output shots\v4\r5\*.jpg and r5_log.txt
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$out = "$town\shots\v4\r5"
$log = "$out\r5_log.txt"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
Log 'high shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode on -csv "$town\shots\v4\views_r5_high.csv" -dir $out | ForEach-Object { Log $_ }
Log 'low shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode off -csv "$town\shots\v4\views_r5.csv" -dir $out | ForEach-Object { Log $_ }
Log 'ROUND5 END'
