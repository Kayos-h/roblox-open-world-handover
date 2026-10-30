param(
  [Parameter(Mandatory=$true)][string]$Module,
  [Parameter(Mandatory=$true)][string]$Worker,
  [string]$Batch = '',
  [string]$Only = '',
  [int]$Res = 420,
  [int]$Chunk = 12,
  [switch]$Quad,
  [int]$TimeoutSec = 900,
  [int]$Slots = 2
)
# At most $Slots headless Blender processes run at the same time across ALL workers (host memory is tight).
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$src = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src'
$logDir = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_work'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stamp = Get-Date -Format 'HHmmss'
$log = Join-Path $logDir ("run_" + $Worker + "_" + $stamp + ".log")
$err = Join-Path $logDir ("run_" + $Worker + "_" + $stamp + ".err")
$a = @('-b', '--factory-startup', '--python', (Join-Path $src 'v4worker.py'), '--', $Module, $Worker, '--res', "$Res", '--chunk', "$Chunk")
if ($Batch) { $a += @('--batch', $Batch) }
if ($Only) { $a += @('--only', $Only) }
if ($Quad) { $a += '--quad' }

$sem = New-Object System.Threading.Semaphore($Slots, $Slots, 'v4blender_slots')
$t0 = Get-Date
$got = $sem.WaitOne(20 * 60 * 1000)
$waited = [math]::Round(((Get-Date) - $t0).TotalSeconds)
if ($waited -gt 2) { Write-Output ("waited $waited s for a free Blender slot") }
try {
  $p = Start-Process -FilePath $exe -ArgumentList $a -PassThru -NoNewWindow -RedirectStandardOutput $log -RedirectStandardError $err
  try { $p.PriorityClass = 'BelowNormal' } catch {}
  $null = $p.Handle
  $ok = $p.WaitForExit($TimeoutSec * 1000)
  if (-not $ok) { try { $p.Kill() } catch {}; Write-Output "TIMEOUT after $TimeoutSec s (killed). Split the batch into smaller chunks. Log: $log" }
  $p.WaitForExit()
  Write-Output ("exit code: " + $p.ExitCode + "   log: " + $log)
}
finally {
  if ($got) { [void]$sem.Release() }
}
$txt = Get-Content $log -ErrorAction SilentlyContinue | Where-Object { $_ -match '^(CHUNK|WORKER_DONE|IMPORT_ERROR|NO_SUCH_BATCH|  |Traceback|\w*Error)' }
$txt | Select-Object -First 140
$e = Get-Content $err -ErrorAction SilentlyContinue | Select-Object -Last 12
if ($e) { Write-Output '--- stderr tail ---'; $e }
