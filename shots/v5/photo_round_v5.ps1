param([string]$round = 'r1', [string[]]$only = @())
# v5 photo round: high views with photo mode ON (fog off), everything else with the game atmosphere. Output shots\v5\<round>\*.jpg and log.txt
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$out = "$town\shots\v5\$round"
$log = "$out\log.txt"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
$lists = @(@('views_v5_high.csv', 'on'), @('views_v5_tower.csv', 'off'), @('views_v5_roads.csv', 'off'), @('views_v5_capital.csv', 'off'), @('views_v5_elf.csv', 'off'), @('views_v5_town1.csv', 'off'), @('views_v5_entrances.csv', 'off'))
foreach ($l in $lists) {
  if ($only.Count -gt 0 -and $only -notcontains $l[0]) { continue }
  Log ('start ' + $l[0])
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode $l[1] -csv "$town\shots\v5\$($l[0])" -dir $out | ForEach-Object { Log $_ }
}
Log 'ROUND END'
