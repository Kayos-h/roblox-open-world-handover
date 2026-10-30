param([string]$area, [int]$batch = 120, [int]$from = 0, [int]$count = 999999, [switch]$noglow, [string]$nocollide = '')
# v4 placement driver: sends batches of a plan (mapplan\<area>.json) to Studio through place_v4.luau.
# Differences to the v3 build.ps1: only the needed palette entries per batch, direct HTTP call (no PowerShell spawn per batch), noglow option.
$ErrorActionPreference = 'Continue'
$base = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$dir = "$base\mapplan"
$log = "$dir\build\build_log.txt"
$plan = Get-Content "$dir\$area.json" -Raw | ConvertFrom-Json
function L($s) { $line = '{0} [{1}] {2}' -f (Get-Date -Format 'HH:mm:ss'), $area, $s; $line | Out-File $log -Append -Encoding utf8; Write-Host $line }

$ids = @{}
Import-Csv "$base\asset_ids.csv" | ForEach-Object { if ($_.asset_id) { $ids[$_.name] = [int64]$_.asset_id } }
$pal = Get-Content "$base\library\palette.json" -Raw | ConvertFrom-Json
$palMap = @{}; foreach ($prop in $pal.PSObject.Properties) { $palMap[$prop.Name] = $prop.Value }
# colour keys per model: old models from catalog.json (pieces), new ones from v4_meta.json (materials)
$keys = @{}
foreach ($c in (Get-Content "$base\mapplan\catalog.json" -Raw -Encoding UTF8 | ConvertFrom-Json)) { $keys[$c.id] = @($c.pieces) }
$meta = Get-Content "$base\library\v4_meta.json" -Raw | ConvertFrom-Json
foreach ($p in $meta.PSObject.Properties) { $keys[$p.Name] = @($p.Value.materials) }
$tpl = [IO.File]::ReadAllText("$base\rebuild\v4\place_v4.luau")
$opts = @{ noglow = [bool]$noglow; nocollide = @($nocollide -split ',' | Where-Object { $_ }) }

$headers = @{ 'Accept' = 'application/json, text/event-stream'; 'Content-Type' = 'application/json' }
$mcp = 'http://localhost:58741/mcp'
function Send-Luau([string]$code) {
  $body = @{ jsonrpc = '2.0'; id = 3; method = 'tools/call'; params = @{ name = 'execute_luau'; arguments = @{ code = $code } } } | ConvertTo-Json -Depth 6 -Compress
  for ($try = 1; $try -le 8; $try++) {
    try {
      $resp = Invoke-WebRequest -Uri $mcp -Method POST -Headers $headers -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 600 -UseBasicParsing
      $m = [regex]::Match($resp.Content, 'data:\s*(\{.*\})', 'Singleline')
      $j = ($(if ($m.Success) { $m.Groups[1].Value } else { $resp.Content }) | ConvertFrom-Json)
      $txt = ($j.result.content | Where-Object { $_.type -eq 'text' } | Select-Object -First 1).text
      if ($txt -match '"success":true') {
        $inner = $txt | ConvertFrom-Json
        return [string]$inner.returnValue
      }
      if ($txt -match '"success":false') { return 'FAILED LUAU: ' + $txt.Substring(0, [Math]::Min(300, $txt.Length)) }
      $last = $txt
    } catch { $last = $_.Exception.Message }
    Start-Sleep -Seconds ([Math]::Min(20, 3 * $try))
  }
  return 'FAILED: ' + $last
}

$pl = @($plan.placements)
$last = [Math]::Min($pl.Count - 1, $from + $count - 1)
$waiting = 0; $skippedTown = 0; $sent = 0; $placedTotal = 0; $failedTotal = 0
$missing = @{}
$t0 = Get-Date
for ($s = $from; $s -le $last; $s += $batch) {
  $items = New-Object System.Collections.Generic.List[object]
  $palSub = @{}
  for ($i = $s; $i -le [Math]::Min($last, $s + $batch - 1); $i++) {
    $p = $pl[$i]
    if ($p.skip) { continue }
    if ($area -notlike 'town1*' -and $p.x -ge -318 -and $p.x -le 318 -and $p.z -ge -545 -and $p.z -le 311) { $skippedTown++; continue }
    if (-not $ids.ContainsKey($p.model)) { $waiting++; $missing[$p.model] = 1; continue }
    $it = [ordered]@{ key = "$area#$i"; m = $p.model; id = $ids[$p.model]; x = $p.x; z = $p.z; rot = $(if ($p.rot) { $p.rot } else { 0 }); g = $(if ($p.group) { $p.group } else { 'Misc' }) }
    if ($p.scale) { $it.s = $p.scale }
    if ($p.y_offset) { $it.yo = $p.y_offset }
    $items.Add($it)
    foreach ($k in $keys[$p.model]) { $kk = $k -replace '_\d+$', ''; if ($palMap.ContainsKey($kk)) { $palSub[$kk] = $palMap[$kk] } }
  }
  if ($items.Count -eq 0) { continue }
  $data = @{ area = $area; items = $items; pal = $palSub; opts = $opts } | ConvertTo-Json -Compress -Depth 8
  $r = Send-Luau ($tpl.Replace('__DATA__', $data))
  $sent += $items.Count
  try { $j = $r | ConvertFrom-Json; $placedTotal += [int]$j.placed; $failedTotal += [int]$j.failed; if ($j.failed -gt 0) { L ("batch " + $s + " failures: " + (($j.errs | Select-Object -First 3) -join ' | ')) } } catch { L ("batch $s raw: " + $r.Substring(0, [Math]::Min(200, $r.Length))) }
  if ((($s - $from) / $batch) % 10 -eq 0) { L ("progress {0}/{1} placed {2} failed {3} ({4:N0}s)" -f ([Math]::Min($last + 1, $s + $batch)), ($last + 1), $placedTotal, $failedTotal, ((Get-Date) - $t0).TotalSeconds) }
  if ($r -like 'FAILED*') { L "STOPPING at item ${s}: $r"; exit 1 }
}
L ("done; sent {0} placed {1} failed {2}; waiting for upload: {3} ({4}); skipped in Town 1 zone: {5}" -f $sent, $placedTotal, $failedTotal, $waiting, (($missing.Keys | Select-Object -First 8) -join ','), $skippedTown)
