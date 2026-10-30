param([string]$area, [string]$kind = 'place', [int]$from = 0, [int]$count = 999999, [int]$batch = 30)
$ErrorActionPreference = 'Continue'
$base = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$dir = "$base\mapplan"
$log = "$dir\build\build_log.txt"
$plan = Get-Content "$dir\$area.json" -Raw | ConvertFrom-Json
$argsFile = "$dir\build\_args_$area.json"

function Send-Luau([string]$code) {
  $json = @{ code = $code } | ConvertTo-Json -Compress -Depth 3
  [IO.File]::WriteAllText($argsFile, $json)
  for ($try = 1; $try -le 12; $try++) {
    $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$base\mcp_call.ps1" -tool execute_luau -argsFile $argsFile 2>&1 | Out-String
    if ($r -match '"success":true') {
      $m = [regex]::Match($r, '"returnValue":"((?:[^"\\]|\\.)*)"')
      if ($m.Success) { return ($m.Groups[1].Value -replace '\\"', '"' -replace '\\\\', '\') }
      return 'ok'
    }
    if ($r -match '"success":false') { return 'FAILED LUAU: ' + [regex]::Match($r, '"error":"((?:[^"\\]|\\.)*)"').Groups[1].Value }
    if ($r -match 'returnValue|Code executed') { return $r.Trim() }
    Start-Sleep -Seconds ([Math]::Min(20, 3 * $try))
  }
  return 'FAILED: ' + $r.Trim().Substring(0, [Math]::Min(300, $r.Trim().Length))
}
function L($s) { $line = '{0} [{1}/{2}] {3}' -f (Get-Date -Format 'HH:mm:ss'), $area, $kind, $s; $line | Out-File $log -Append -Encoding utf8; $line }

if ($kind -eq 'terrain') {
  $tpl = [IO.File]::ReadAllText("$dir\build\terrain.luau")
  $prot = @(, @(1700, 3300, -2700, -1050))
  if ($area -notlike 'town1*') { $prot += , @(-470, 470, -800, 470) }
  $ops = @($plan.terrain)
  $last = [Math]::Min($ops.Count - 1, $from + $count - 1)
  for ($i = $from; $i -le $last; $i++) {
    $op = $ops[$i]
    switch ($op.op) {
      'plateau' { $bx0 = $op.cx - $op.rx - $op.slope; $bx1 = $op.cx + $op.rx + $op.slope; $bz0 = $op.cz - $op.rz - $op.slope; $bz1 = $op.cz + $op.rz + $op.slope }
      'hill'    { $bx0 = $op.cx - $op.r; $bx1 = $op.cx + $op.r; $bz0 = $op.cz - $op.r; $bz1 = $op.cz + $op.r }
      'paint'   { $bx0 = $op.cx - $op.r; $bx1 = $op.cx + $op.r; $bz0 = $op.cz - $op.r; $bz1 = $op.cz + $op.r }
      'ramp'    { $pad = $op.width / 2 + [Math]::Max(10, [Math]::Min($op.width * 0.6, 60)); $bx0 = [Math]::Min($op.x0, $op.x1) - $pad; $bx1 = [Math]::Max($op.x0, $op.x1) + $pad; $bz0 = [Math]::Min($op.z0, $op.z1) - $pad; $bz1 = [Math]::Max($op.z0, $op.z1) + $pad }
      default   { $bx0 = [Math]::Min($op.x0, $op.x1); $bx1 = [Math]::Max($op.x0, $op.x1); $bz0 = [Math]::Min($op.z0, $op.z1); $bz1 = [Math]::Max($op.z0, $op.z1) }
    }
    $ext = [Math]::Max($bx1 - $bx0, $bz1 - $bz0)
    $step = [Math]::Min(32, [Math]::Max(8, 4 * [Math]::Round($ext / 600)))
    if ($op.op -eq 'ramp' -and $op.width -le 40) { $step = 4 }
    if ($op.op -eq 'paint' -and $op.r -le 300) { $step = 4 }
    $cells = (($bx1 - $bx0) / $step) * (($bz1 - $bz0) / $step)
    $bands = [Math]::Max(1, [Math]::Ceiling($cells / 4000))
    $bh = [Math]::Ceiling((($bz1 - $bz0) / $bands) / $step) * $step
    $bx0 = [Math]::Floor($bx0 / $step) * $step; $bz0s = [Math]::Floor($bz0 / $step) * $step
    for ($b = 0; $b -lt $bands; $b++) {
      $z0 = $bz0s + $b * $bh; $z1 = [Math]::Min($bz1 + $step, $z0 + $bh)
      $data = @{ op = $op; step = $step; protect = $prot; bx0 = $bx0; bx1 = $bx1; bz0 = $z0; bz1 = $z1 } | ConvertTo-Json -Compress -Depth 6
      $r = Send-Luau ($tpl.Replace('__DATA__', $data))
      L ("op {0} {1} band {2}/{3} step {4}: {5}" -f $i, $op.op, ($b + 1), $bands, $step, $r)
      if ($r -like 'FAILED*') { L "STOPPING at op $i band $b"; exit 1 }
    }
  }
  exit 0
}

# placements
$ids = @{}
Import-Csv "$base\asset_ids.csv" | ForEach-Object { if ($_.asset_id) { $ids[$_.name] = [int64]$_.asset_id } }
$pal = Get-Content "$base\library\palette.json" -Raw | ConvertFrom-Json
$tpl = [IO.File]::ReadAllText("$dir\build\place.luau")
$pl = @($plan.placements)
$last = [Math]::Min($pl.Count - 1, $from + $count - 1)
$waiting = 0
$skippedTown = 0
for ($s = $from; $s -le $last; $s += $batch) {
  $items = @(); $keys = @{}
  for ($i = $s; $i -le [Math]::Min($last, $s + $batch - 1); $i++) {
    $p = $pl[$i]
    if ($p.skip) { continue }
    if ($area -notlike 'town1*' -and $p.x -ge -318 -and $p.x -le 318 -and $p.z -ge -545 -and $p.z -le 311) { $skippedTown++; continue }
    if (-not $ids.ContainsKey($p.model)) { $waiting++; continue }
    $it = [ordered]@{ key = "$area#$i"; m = $p.model; id = $ids[$p.model]; x = $p.x; z = $p.z; rot = $(if ($p.rot) { $p.rot } else { 0 }); g = $(if ($p.group) { $p.group } else { 'Misc' }) }
    if ($p.scale) { $it.s = $p.scale }
    if ($p.y_offset) { $it.yo = $p.y_offset }
    $items += $it
  }
  if ($items.Count -eq 0) { continue }
  $palSub = @{}
  foreach ($prop in $pal.PSObject.Properties) { $palSub[$prop.Name] = $prop.Value }
  $data = @{ area = $area; items = $items; pal = $palSub } | ConvertTo-Json -Compress -Depth 6
  $r = Send-Luau ($tpl.Replace('__DATA__', $data))
  L ("items {0}-{1}: {2}" -f $s, [Math]::Min($last, $s + $batch - 1), $r)
  if ($r -like 'FAILED*') { L "STOPPING at item $s"; exit 1 }
}
L "done; waiting for upload: $waiting; skipped in protected zones: $skippedTown"
