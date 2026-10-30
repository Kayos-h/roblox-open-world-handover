# places the dressing plans one after the other (log: rebuild\v4\dress_place_log.txt)
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
$log = "$rb\dress_place_log.txt"
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
$nc = 'CastleBeds,CastleOuterTufts,CastleOuterBushes,CapitalBeds,CapitalWallTufts,CapitalWallBushes,HarbourBeds,HarbourBeach,ElfRim,ElfLily,ElfClearing,T1ApronRing,T1GraveyardEdge,IceRim'
foreach ($p in 'v4_dress_castle','v4_dress_capital','v4_dress_harbour','v4_dress_rusty','v4_dress_alpine','v4_dress_elf','town1_dress') {
  Log "== $p begin"
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\build_v4.ps1" -area $p -batch 60 -nocollide $nc | ForEach-Object { Log ("  " + $_) }
  Log "== $p end"
}
Log 'dress place END'
