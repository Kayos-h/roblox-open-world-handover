param([Parameter(Mandatory=$true)][string]$Module, [string]$Ids = 'ALL', [string]$Tag = 'tmp', [int]$Res = 360, [int]$Views = 4, [int]$Samples = 10, [int]$TimeoutSec = 900, [int]$WaitSec = 2400)
# SCRATCH build + four-angle sheets of v5 models in a headless Blender. One at a time (named mutex) so parallel builders never overload the PC.
# Writes ONLY to library\v5_work\fix_scratch\<Tag>\. Never touches the model library, the metas, the palettes or the open Blender.
# Example: scratch.ps1 -Module v5_vh -Ids VC04_01_skull_city_building_01,VC04_02_skull_city_building_02 -Tag vh
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$py = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5scratch.py'
$out = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\fix_scratch\' + $Tag
New-Item -ItemType Directory -Force -Path $out | Out-Null
$mutex = New-Object System.Threading.Mutex($false, 'Global\v5_scratch_blender')
$got = $false
try { $got = $mutex.WaitOne($WaitSec * 1000) } catch [System.Threading.AbandonedMutexException] { $got = $true }
if (-not $got) { Write-Output "SCRATCH_BUSY: waited $WaitSec s, another build is still running. Try again."; exit 2 }
try {
    $log = Join-Path $env:TEMP ('v5scratch_' + $Tag + '_' + (Get-Date -Format 'HHmmss') + '.log')
    $p = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', $py, '--', $Module, $Ids, $out, $Res, $Views, $Samples) -PassThru -NoNewWindow -RedirectStandardOutput $log -RedirectStandardError ($log + '.err')
    if (-not $p.WaitForExit($TimeoutSec * 1000)) { try { $p.Kill() } catch {}; Write-Output "SCRATCH_TIMEOUT after $TimeoutSec s (Blender killed). Build fewer ids per call." }
} finally { $mutex.ReleaseMutex() }
Get-Content $log -ErrorAction SilentlyContinue | Where-Object { $_ -match '^(SCRATCH|Traceback|\w+Error)|File "' } | ForEach-Object { $_.TrimEnd() }
Get-Content ($log + '.err') -ErrorAction SilentlyContinue | Select-Object -Last 4
Write-Output ("SHEETS in " + $out)
