$l = Get-NetTCPConnection -LocalPort 58741 -State Listen -ErrorAction SilentlyContinue
if (-not $l) { 'nothing listening on 58741' }
foreach ($c in $l) {
  $p = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
  "{0} pid={1} cpuSec={2} memMB={3} started={4}" -f $p.ProcessName, $p.Id, [int]$p.CPU, [int]($p.WorkingSet64/1MB), $p.StartTime
}
$e = Get-NetTCPConnection -LocalPort 58741 -State Established -ErrorAction SilentlyContinue
"established connections: " + @($e).Count
