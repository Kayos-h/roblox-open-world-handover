# photo round 4 (after the round-3 fixes): high shots (photo mode on), then ground shots. Output shots\v4\r4\*.jpg and r4_log.txt
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$out = "$town\shots\v4\r4"
$log = "$out\r4_log.txt"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
Log 'high shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode on -csv "$town\shots\v4\views_r4_high.csv" -dir $out | ForEach-Object { Log $_ }
Log 'low shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode off -csv "$town\shots\v4\views_r4_low.csv" -dir $out | ForEach-Object { Log $_ }
Log 'ROUND4 END'
