# photo round 3: high shots (photo mode on), low shots, town shots. Output: shots\v4\r3\*.jpg and r3_log.txt
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$out = "$town\shots\v4\r3"
$log = "$out\r3_log.txt"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
Log 'high shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode on -csv "$town\shots\v4\views_r3_high.csv" -dir $out | ForEach-Object { Log $_ }
Log 'low shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode off -csv "$town\shots\v4\views_r3_low.csv" -dir $out | ForEach-Object { Log $_ }
Log 'town shots'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode off -csv "$town\shots\v4\views_r3_towns.csv" -dir $out | ForEach-Object { Log $_ }
Log 'ROUND3 END'
