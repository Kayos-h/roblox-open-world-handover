param([string]$areas = 'v3_capital,v3_rusty,v3_harbour,v3_alpine,v3_elf,Enterable,v3_interiors,town1_graveyard,town1_gy2,v3f_castle,v3f_se,v3f_alpine,v3f_harbour,v3f_rusty,v3f_elf,v3f_country,v3_country,PartBuilt,town1_extra,town1_yard')
# Exports footprints of placed models per area to rebuild\v4\occ_<area>.json (used by env_plan.py to keep trees out of buildings).
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$tpl = [IO.File]::ReadAllText("$rb\v4\export_occupancy.luau")
$tmp = "$rb\v4\_occ_args.json"
foreach ($a in ($areas -split ',')) {
  $code = $tpl.Replace('__DATA__', (@{ area = $a } | ConvertTo-Json -Compress))
  [IO.File]::WriteAllText($tmp, (@{ code = $code } | ConvertTo-Json -Compress -Depth 3))
  $r = (& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\studio.ps1" -argsFile $tmp | Out-String).Trim()
  if (-not $r.StartsWith('[')) { Write-Output ("$a FAILED: " + $r.Substring(0, [Math]::Min(160, $r.Length))); continue }
  [IO.File]::WriteAllText("$rb\v4\occ_$a.json", $r)
  $n = ([regex]::Matches($r, '\],\[')).Count + 1
  if ($r -eq '[]') { $n = 0 }
  Write-Output ("$a footprints=$n")
}
