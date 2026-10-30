param([Parameter(Mandatory=$true)][string]$Module, [string]$Batch = '-', [string]$Only = '-', [int]$TimeoutSec = 300)
# Runs v5check.py in a headless Blender and prints only the useful lines (numbers, errors).
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$py = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5check.py'
$log = Join-Path $env:TEMP ('v5check_' + (Get-Date -Format 'HHmmss') + '.log')
$p = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', $py, '--', $Module, $Batch, $Only) -PassThru -NoNewWindow -RedirectStandardOutput $log -RedirectStandardError ($log + '.err')
if (-not $p.WaitForExit($TimeoutSec * 1000)) { try { $p.Kill() } catch {}; Write-Output "TIMEOUT after $TimeoutSec s (killed)" }
Get-Content $log -ErrorAction SilentlyContinue | Where-Object { $_ -match '^(CHECKED|ERROR)|tris,|Traceback|Error|File "|line [0-9]+' } | Select-Object -First 60
Get-Content ($log + '.err') -ErrorAction SilentlyContinue | Select-Object -Last 6
