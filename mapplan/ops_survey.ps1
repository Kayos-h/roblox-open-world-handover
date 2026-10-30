$d = 'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
$ops = @{}; $pk = @{}; $mats = @{}
foreach ($a in 'roads','town1','capital','harbour','elf','alpine','rusty') {
  $j = Get-Content "$d\$a.json" -Raw | ConvertFrom-Json
  foreach ($t in @($j.terrain)) {
    $keys = ($t.PSObject.Properties.Name | Sort-Object) -join ','
    $k = "$($t.op) [$keys]"
    if (-not $ops[$k]) { $ops[$k] = @() }; $ops[$k] += $a
    if ($t.material) { $mats[$t.material] = 1 }
  }
  foreach ($p in @($j.placements)) { foreach ($n in $p.PSObject.Properties.Name) { $pk[$n] = 1 } }
}
$ops.Keys | Sort-Object | ForEach-Object { "{0}  <- {1}" -f $_, (($ops[$_] | Sort-Object -Unique) -join ' ') }
'placement keys: ' + (($pk.Keys | Sort-Object) -join ', ')
'materials: ' + (($mats.Keys | Sort-Object) -join ', ')
$t1 = Get-Content "$d\town1.json" -Raw | ConvertFrom-Json
'town1 spawn: ' + ($t1.spawn | ConvertTo-Json -Compress)
'town1 skull: ' + ($t1.skull | ConvertTo-Json -Compress)
'town1 archive: ' + (($t1.archive | ForEach-Object { if ($_ -is [string]) { $_ } else { $_ | ConvertTo-Json -Compress } }) -join ' | ')
