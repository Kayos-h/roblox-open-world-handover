param([string]$plans = 'v4_forest,v4_rocks,v4_shore,v4_pieces,v4_under')
# Places the environment plans one after the other (log: mapplan\build\build_log.txt and rebuild\v4\place_all_log.txt)
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
$log = "$rb\place_all_log.txt"
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
$nc = @{ v4_under = 'Under'; v4_shore = 'Beach,Riverbank,Lakeside,LilyPads' }
foreach ($p in ($plans -split ',')) {
  Log "== $p begin"
  $args2 = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "$rb\build_v4.ps1", '-area', $p, '-batch', '120')
  if ($nc.ContainsKey($p)) { $args2 += @('-nocollide', $nc[$p]) }
  & powershell @args2 | ForEach-Object { Log ("  " + $_) }
  Log "== $p end"
}
Log 'place_all END'
