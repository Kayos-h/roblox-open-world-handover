param([Parameter(Mandatory=$true)][string]$Module, [Parameter(Mandatory=$true)][string]$Worker, [string]$Batch = '', [string]$Only = '', [int]$TimeoutSec = 600)
# Builds a v5 module's batches inside the OPEN Blender (the add-on socket on port 9876), exactly like run 1. Prints Blender's own result lines.
$b = 'None'
if ($Batch) { $b = "['" + ($Batch -replace ',', "','") + "']" }
$o = 'None'
if ($Only) { $o = "['" + ($Only -replace ',', "','") + "']" }
$py = "import sys`nimport importlib`nSRC = r'C:\Users\Nitro\.kiro\crew\workspace\town\library\src'`nif SRC not in sys.path: sys.path.insert(0, SRC)`nimport v5liverun`nimportlib.reload(v5liverun)`nv5liverun.run('$Module', '$Worker', batches=$b, only=$o)`n"
$f = Join-Path $env:TEMP 'v5_live_job.py'
[IO.File]::WriteAllText($f, $py)
$out = & 'C:\Users\Nitro\.kiro\crew\workspace\town\blender_exec.ps1' -py $f -timeoutSec $TimeoutSec
($out -split "`n") | Where-Object { $_ -match '^(CHUNK|LIVE_DONE|NO_SUCH|PREVIEW|BLENDER ERROR|error:|Traceback|   \(|\s+File |\w+Error)' } | ForEach-Object { $_.TrimEnd() }
