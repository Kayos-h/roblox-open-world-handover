$all = Get-CimInstance Win32_Process
$loops = $all | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -match 'bridge' }
foreach ($l in $loops) {
  "loop cmd pid=$($l.ProcessId) started=$($l.CreationDate) cmd=$($l.CommandLine)"
  $p = $l; for ($i = 0; $i -lt 6; $i++) {
    $p = $all | Where-Object { $_.ProcessId -eq $p.ParentProcessId }
    if (-not $p) { '   parent: (gone)'; break }
    "   parent: $($p.Name) pid=$($p.ProcessId)"
  }
}
if (-not $loops) { 'no bridge loop running' }
