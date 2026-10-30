$d = 'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
$cat = @{}; (Get-Content "$d\catalog.json" -Raw | ConvertFrom-Json) | ForEach-Object { $cat[$_.id] = $_ }
$linear = @{}
foreach ($c in $cat.Values) { if ($c.size_x -ge 2.5 * $c.size_z -and $c.size_x -ge 6 -and $c.id -match '(?i)wall|fence|hedge|curb|seawall|breakwater|railing|terrace_wall') { $linear[$c.id] = $c } }
"linear models: " + (($linear.Keys | Sort-Object) -join ' ')
$centres = @{ capital = @(0, -2500); alpine = @(2500, -500); elf = @(-2400, -600); harbour = @(-600, 2700); rusty = @(1900, 1700); roads = @(0, 0); town1 = @(0, -108) }
$changed = @()
foreach ($a in $centres.Keys) {
  $f = "$d\$a.json"; $j = Get-Content $f -Raw | ConvertFrom-Json
  $pl = @($j.placements); $n = 0
  for ($i = 0; $i -lt $pl.Count; $i++) {
    $p = $pl[$i]
    if (-not $linear.ContainsKey($p.model)) { continue }
    $L = $linear[$p.model].size_x
    $best = $null; $bd = 1e9
    for ($k = 0; $k -lt $pl.Count; $k++) {
      if ($k -eq $i) { continue }
      $q = $pl[$k]
      if (-not $linear.ContainsKey($q.model)) { continue }
      $dd = [Math]::Sqrt(($q.x - $p.x) * ($q.x - $p.x) + ($q.z - $p.z) * ($q.z - $p.z))
      if ($dd -lt $bd) { $bd = $dd; $best = $q }
    }
    if (-not $best -or $bd -gt 2.2 * $L) { continue }
    $dx = $best.x - $p.x; $dz = $best.z - $p.z
    $ang = [Math]::Atan2($dx, $dz) * 180 / [Math]::PI
    $lineRot = (($ang + 90) % 180 + 180) % 180
    $c = $centres[$a]
    $ox = $p.x - $c[0]; $oz = $p.z - $c[1]
    $r1 = $lineRot; $r2 = ($lineRot + 180) % 360
    $f1x = [Math]::Sin($r1 * [Math]::PI / 180); $f1z = [Math]::Cos($r1 * [Math]::PI / 180)
    $want = if (($f1x * $ox + $f1z * $oz) -ge 0) { $r1 } else { $r2 }
    $cur = ((([double]$(if ($p.rot) { $p.rot } else { 0 })) % 360) + 360) % 360
    $diff = [Math]::Abs((($cur - $want) % 180 + 180) % 180)
    if ($diff -gt 20 -and $diff -lt 160) {
      $p.rot = [Math]::Round($want)
      $changed += "$a#$i"; $n++
    }
  }
  if ($n -gt 0) { $j | ConvertTo-Json -Depth 8 | Out-File $f -Encoding utf8 }
  "{0}: fixed {1} linear pieces" -f $a, $n
}
$changed -join ',' | Out-File "$d\build\_rotfix_keys.txt" -Encoding utf8
