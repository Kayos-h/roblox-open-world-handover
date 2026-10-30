param([string[]]$steps)
$dir = 'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\build'
$state = "$dir\steps_done.txt"
if (-not (Test-Path $state)) { '' | Out-File $state -Encoding utf8 }
$steps = @($steps | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
"RUNNER started $(Get-Date -Format 'HH:mm:ss') steps: $($steps -join ' ')" | Out-File "$dir\build_log.txt" -Append -Encoding utf8
foreach ($s in $steps) {
  if ((Get-Content $state) -contains $s) { continue }
  $a, $k = $s.Split(':')
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$dir\build.ps1" -area $a -kind $k
  if ($LASTEXITCODE -ne 0) { "RUNNER stopped at $s (exit $LASTEXITCODE) $(Get-Date -Format 'HH:mm:ss')" | Out-File "$dir\build_log.txt" -Append -Encoding utf8; exit 1 }
  if ($k -eq 'terrain') { $s | Out-File $state -Append -Encoding utf8 }
}
"RUNNER finished $(Get-Date -Format 'HH:mm:ss')" | Out-File "$dir\build_log.txt" -Append -Encoding utf8
