$d = 'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
$cat = @{}; (Get-Content "$d\catalog.json" -Raw | ConvertFrom-Json) | ForEach-Object { $cat[$_.id] = $_ }
$rects = @{
  town1 = @(-450, 450, -560, 345); capital = @(-800, 800, -3300, -1700); alpine = @(2150, 2850, -850, -150)
  elf = @(-2850, -1950, -1050, -150); harbour = @(-1000, -200, 2300, 3100); rusty = @(1600, 2200, 1400, 2000)
}
$keep = @(1700, 3300, -2700, -1050)
function inR($x, $z, $r) { return ($x -ge $r[0] -and $x -le $r[1] -and $z -ge $r[2] -and $z -le $r[3]) }
$total = 0; $used = @{}
foreach ($a in 'roads','town1','capital','harbour','elf','alpine','rusty') {
  $j = Get-Content "$d\$a.json" -Raw | ConvertFrom-Json
  $pl = @($j.placements); $total += $pl.Count
  $unknown = @($pl | Where-Object { -not $cat.ContainsKey($_.model) } | ForEach-Object { $_.model } | Sort-Object -Unique)
  $out = 0; $intr = 0; $keepHit = 0
  foreach ($p in $pl) {
    $used[$p.model] = 1
    if ($a -eq 'roads') { foreach ($k in $rects.Keys) { if (inR $p.x $p.z $rects[$k]) { $intr++; break } } }
    elseif (-not (inR $p.x $p.z $rects[$a])) { $out++ }
    if (inR $p.x $p.z $keep) { $keepHit++ }
  }
  $extra = ($j.PSObject.Properties.Name | Where-Object { $_ -notin 'area','terrain','placements' }) -join ','
  "{0,-8} terrain={1,3} placements={2,5} unknownIds={3} outsideRect={4} insideOtherArea={5} inMountainKeepOut={6} extraKeys=[{7}]" -f $a, @($j.terrain).Count, $pl.Count, ($unknown -join ' '), $out, $intr, $keepHit, $extra
}
"TOTAL placements: $total"
"catalog models used at least once: $($used.Count) of $($cat.Count)"
$unused = $cat.Keys | Where-Object { -not $used.ContainsKey($_) } | Sort-Object
"unused models: " + ($unused -join ' ')
