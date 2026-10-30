param([Parameter(Mandatory=$true)][string]$Mode, [string]$Tag = 'plan', [int]$Render = 0, [int]$Res = 760, [int]$TimeoutSec = 1500, [int]$WaitSec = 2400)
# Tower assembly check in a headless Blender, one at a time (same mutex as scratch.ps1). Writes only to library\v5_work\tower_check\<Tag>\.
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$py = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_tower_assembly.py'
$out = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\tower_check\' + $Tag
New-Item -ItemType Directory -Force -Path $out | Out-Null
$mutex = New-Object System.Threading.Mutex($false, 'Global\v5_scratch_blender')
$got = $false
try { $got = $mutex.WaitOne($WaitSec * 1000) } catch [System.Threading.AbandonedMutexException] { $got = $true }
if (-not $got) { Write-Output "TOWER_BUSY"; exit 2 }
try {
    $log = Join-Path $env:TEMP ('tower_' + $Tag + '_' + (Get-Date -Format 'HHmmss') + '.log')
    $p = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', $py, '--', $Mode, $out, $Render, $Res) -PassThru -NoNewWindow -RedirectStandardOutput $log -RedirectStandardError ($log + '.err')
    if (-not $p.WaitForExit($TimeoutSec * 1000)) { try { $p.Kill() } catch {}; Write-Output "TOWER_TIMEOUT after $TimeoutSec s" }
} finally { $mutex.ReleaseMutex() }
Get-Content $log -ErrorAction SilentlyContinue | Where-Object { $_ -match '^(TOWER|STAIR|FLOOR|INNER|RENDER|SOLVE)|Traceback|Error|File "' } | ForEach-Object { $_.TrimEnd() }
Get-Content ($log + '.err') -ErrorAction SilentlyContinue | Select-Object -Last 4
