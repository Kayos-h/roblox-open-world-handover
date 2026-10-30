param([string]$tag = 'v4b', [int]$ext = 5376)
# Regenerates the whole island plus a ring of ocean out to +-$ext studs, then runs the void-fill / clip passes over the island only.
# Log: rebuild\v4\gen_log.txt
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$logFile = "$rb\v4\gen_log.txt"
function Log($s) { $line = ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s); $line | Out-File $logFile -Append -Encoding utf8 }
Log "generation begin tag=$tag ext=$ext"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\tg_run.ps1" -x0 (-$ext) -x1 $ext -z0 (-$ext) -z1 $ext -tag $tag -pollSecs 30 -maxMinutes 20 | ForEach-Object { Log ("tg : " + $_) }
Log 'generation END, starting post passes'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\v4\post_passes.ps1" -tag $tag | Out-Null
Log 'all END'
