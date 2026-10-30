param([string]$tag = 'v4c', [int]$ext = 5376, [int]$floaterStep = 40)
# v4 terrain pipeline: generate (island plus ocean ring), clip pass, floater scan. No void-fill passes (they are destructive for v4).
# Log: rebuild\v4\gen_log.txt
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$logFile = "$rb\v4\gen_log.txt"
function Log($s) { $line = ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s); $line | Out-File $logFile -Append -Encoding utf8 }
function Studio($argsFile) { & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\studio.ps1" -argsFile $argsFile | Out-String }
Log "generation begin tag=$tag ext=$ext"
& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\tg_run.ps1" -x0 (-$ext) -x1 $ext -z0 (-$ext) -z1 $ext -tag $tag -pollSecs 30 -maxMinutes 20 | ForEach-Object { Log ("tg : " + $_) }
Log 'generation END, clip pass over the island'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\clip_run.ps1" -x0 -3584 -x1 3584 -z0 -3584 -z1 3584 -tag $tag -pollSecs 20 -maxMinutes 25 | ForEach-Object { Log ("clip : " + $_) }
Log 'clip END, floater scan (background thread in Studio)'
$fd = "$rb\v4\_floater_data.json"
[IO.File]::WriteAllText($fd, (@{ x0 = -3580; x1 = 3580; z0 = -3580; z1 = 3580; step = $floaterStep } | ConvertTo-Json -Compress))
$fr = & powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\runluau.ps1" -file "$rb\v4\floater_scan_bg.luau" -data $fd | Out-String
Log ("floater start: " + $fr.Trim())
$pf = "$rb\v4\_poll_float.json"
[IO.File]::WriteAllText($pf, (@{ code = 'if _G.FLOATREP then return _G.FLOATREP end return "RUNNING " .. string.format("%.0f", os.clock() - (_G.FLOATSTART or os.clock()))' } | ConvertTo-Json -Compress))
$tf = Get-Date
while ($true) {
  Start-Sleep -Seconds 20
  $p = (Studio $pf).Trim()
  if ($p -notmatch '^RUNNING') { Log ("floater : " + $p.Substring(0, [Math]::Min(1800, $p.Length))); break }
  if (((Get-Date) - $tf).TotalMinutes -gt 30) { Log 'floater TIMEOUT'; break }
}
Log 'all END'
