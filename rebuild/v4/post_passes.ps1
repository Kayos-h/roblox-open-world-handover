param([string]$tag = 'v4a', [int]$x0 = -3584, [int]$x1 = 3584, [int]$z0 = -3584, [int]$z1 = 3584, [int]$floaterStep = 40)
# Post-generation terrain passes for v4: void fill 1, void fill 2, clip, floater scan. Log: rebuild\v4\post_passes_log.txt
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$logFile = "$rb\v4\post_passes_log.txt"
function Log($s) { $line = ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s); $line | Out-File $logFile -Append -Encoding utf8; Write-Host $line }
function Studio($argsFile) { & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\studio.ps1" -argsFile $argsFile | Out-String }
function PollArgs($luauFile, $outFile) { [IO.File]::WriteAllText($outFile, (@{ code = [IO.File]::ReadAllText($luauFile) } | ConvertTo-Json -Compress -Depth 3)) }

$data = @{ x0 = $x0; x1 = $x1; z0 = $z0; z1 = $z1; tag = $tag } | ConvertTo-Json -Compress
$dataFile = "$rb\v4\_post_data.json"
[IO.File]::WriteAllText($dataFile, $data)

function RunPass($name, $luau, $pollLuau, $maxMin) {
  Log "== $name start"
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\runluau.ps1" -file "$rb\$luau" -data $dataFile | Out-String
  Log ("start: " + $r.Trim().Substring(0, [Math]::Min(120, $r.Trim().Length)))
  $pa = "$rb\v4\_poll_$name.json"
  PollArgs "$rb\$pollLuau" $pa
  $t0 = Get-Date
  while ($true) {
    Start-Sleep -Seconds 20
    $p = (Studio $pa).Trim()
    $short = $p.Substring(0, [Math]::Min(260, $p.Length))
    Log "$name : $short"
    if ($p -match 'done=true') { break }
    if (((Get-Date) - $t0).TotalMinutes -gt $maxMin) { Log "$name TIMEOUT"; break }
  }
}

Log "post passes begin tag=$tag"
RunPass 'fill1' 'fill_voids.luau' 'fill_poll.luau' 25
RunPass 'fill2' 'fill_voids2.luau' 'fill2_poll.luau' 25
Log '== clip start'
& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\clip_run.ps1" -x0 $x0 -x1 $x1 -z0 $z0 -z1 $z1 -tag $tag -pollSecs 20 -maxMinutes 25 | ForEach-Object { Log ("clip : " + $_) }
Log '== floater scan'
$fd = "$rb\v4\_floater_data.json"
[IO.File]::WriteAllText($fd, (@{ x0 = $x0 + 4; x1 = $x1 - 4; z0 = $z0 + 4; z1 = $z1 - 4; step = $floaterStep } | ConvertTo-Json -Compress))
$fr = & powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\runluau.ps1" -file "$rb\v4\floater_scan_bg.luau" -data $fd | Out-String
Log ("floater start: " + $fr.Trim())
$pollCode = 'if _G.FLOATREP then return _G.FLOATREP end return "RUNNING " .. string.format("%.0f", os.clock() - (_G.FLOATSTART or os.clock()))'
$pf = "$rb\v4\_poll_float.json"
[IO.File]::WriteAllText($pf, (@{ code = $pollCode } | ConvertTo-Json -Compress))
$tf = Get-Date
while ($true) {
  Start-Sleep -Seconds 20
  $p = (Studio $pf).Trim()
  if ($p -notmatch '^RUNNING') { Log ("floater : " + $p.Substring(0, [Math]::Min(1800, $p.Length))); break }
  if (((Get-Date) - $tf).TotalMinutes -gt 30) { Log 'floater TIMEOUT'; break }
}
Log 'post passes END'
