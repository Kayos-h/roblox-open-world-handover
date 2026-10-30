param([string]$area, [int]$batch = 80, [int]$from = 0, [int]$count = 999999, [switch]$dry)
# v5 PLACEHOLDER driver (DRAFT, not yet run): sends the V5 models of a plan (mapplan\<area>.json) to Studio as coloured block placeholders through place_v5_ph.luau.
# Only models that are in plan_v5\V5_MANIFEST.csv and NOT yet in asset_ids.csv become placeholders; built and uploaded models are placed by build_v4.ps1 as usual.
#   .\build_v5_ph.ps1 -area v5_himalaya -dry        shows the count and size table without touching Studio
#   .\build_v5_ph.ps1 -area v5_himalaya -batch 60
$ErrorActionPreference = 'Continue'
$base = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$plan = Get-Content "$base\mapplan\$area.json" -Raw | ConvertFrom-Json
$ids = @{}
Import-Csv "$base\asset_ids.csv" | ForEach-Object { if ($_.asset_id) { $ids[$_.name] = 1 } }
$man = @{}
Import-Csv "$base\plan_v5\V5_MANIFEST.csv" | ForEach-Object { $man[$_.id] = $_ }
function Colour([string]$row) {
  switch -Regex ($row) {
    '^CP' { return @(198, 88, 52) } '^WT' { return @(96, 86, 134) } '^(HM|HL|SP)' { return @(200, 206, 214) } '^(EV|FR|RW)' { return @(80, 130, 70) }
    '^TW' { return @(78, 76, 86) } '^NE' { return @(190, 160, 100) } '^(DS|SD)' { return @(214, 150, 90) } '^VC' { return @(54, 50, 58) }
    '^(CO|HB)' { return @(110, 108, 110) } '^(RD|BR|RV)' { return @(140, 134, 126) } '^(PL|VL)' { return @(206, 120, 84) } '^VG' { return @(60, 110, 60) }
    '^FL' { return @(118, 116, 122) } '^LM(0[3-8])' { return @(200, 206, 214) } default { return @(150, 142, 158) }
  }
}
$pl = @($plan.placements)
$items = New-Object System.Collections.Generic.List[object]
$skippedBuilt = 0; $unknown = 0
for ($i = $from; $i -lt [Math]::Min($pl.Count, $from + $count); $i++) {
  $p = $pl[$i]
  if ($ids.ContainsKey($p.model)) { $skippedBuilt++; continue }
  $m = $man[$p.model]
  if (-not $m) { $unknown++; continue }
  $items.Add([ordered]@{ key = "$area#$i"; m = $p.model; x = $p.x; z = $p.z; rot = $(if ($p.rot) { $p.rot } else { 0 }); g = $(if ($p.group) { $p.group } else { 'Misc' }); yo = $(if ($p.y_offset) { $p.y_offset } else { 0 });
      sx = [double]$m.size_x; sy = [double]$m.size_y; sz = [double]$m.size_z; c = (Colour $m.row) })
}
Write-Host "$($items.Count) placeholder(s) for $area; $skippedBuilt already uploaded (use build_v4.ps1); $unknown not V5 models."
if ($dry) { exit 0 }
$tpl = [IO.File]::ReadAllText("$base\rebuild\v5\place_v5_ph.luau")
$headers = @{ 'Accept' = 'application/json, text/event-stream'; 'Content-Type' = 'application/json' }
$mcp = 'http://localhost:58741/mcp'
$placed = 0; $failed = 0
for ($s = 0; $s -lt $items.Count; $s += $batch) {
  $chunk = $items.GetRange($s, [Math]::Min($batch, $items.Count - $s))
  $data = @{ area = $area; items = $chunk } | ConvertTo-Json -Compress -Depth 6
  $body = @{ jsonrpc = '2.0'; id = 3; method = 'tools/call'; params = @{ name = 'execute_luau'; arguments = @{ code = $tpl.Replace('__DATA__', $data) } } } | ConvertTo-Json -Depth 6 -Compress
  try {
    $resp = Invoke-WebRequest -Uri $mcp -Method POST -Headers $headers -Body ([Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 600 -UseBasicParsing
    $mm = [regex]::Match($resp.Content, 'data:\s*(\{.*\})', 'Singleline')
    $j = ($(if ($mm.Success) { $mm.Groups[1].Value } else { $resp.Content }) | ConvertFrom-Json)
    $txt = ($j.result.content | Where-Object { $_.type -eq 'text' } | Select-Object -First 1).text
    Write-Host ("batch {0}: {1}" -f $s, $txt.Substring(0, [Math]::Min(160, $txt.Length)))
  } catch { Write-Host "batch $s failed: $($_.Exception.Message)"; $failed++ }
}
Write-Host "done; batches failed: $failed"
