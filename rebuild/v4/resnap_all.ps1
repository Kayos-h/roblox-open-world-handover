param([string]$areas = 'v3_country,v3f_country,v3f_se,v3_capital,v3f_castle,v3_rusty,v3f_rusty,v3_harbour,v3f_harbour,v3_alpine,v3f_alpine')
# Re-snaps kept areas to the regenerated terrain (fixpass.luau through resnap.ps1). Log: rebuild\v4\resnap_log.txt
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$log = "$rb\v4\resnap_log.txt"
foreach ($a in ($areas -split ',')) {
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\resnap.ps1" -areas $a | Out-String
  ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $r.Trim()) | Out-File $log -Append -Encoding utf8
}
('{0} resnap END' -f (Get-Date -Format 'HH:mm:ss')) | Out-File $log -Append -Encoding utf8
