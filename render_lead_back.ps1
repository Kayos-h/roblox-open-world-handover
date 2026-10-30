param([string]$Ids = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\lead\pack_ids.json', [string]$Out = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\lead_back')
# Back view of every model in the id file, rendered from the SAVED library files, into a NEW folder (the renderer skips existing pictures). Serialized with the scratch queue.
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$py = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_backview.py'
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$mutex = New-Object System.Threading.Mutex($false, 'Global\v5_scratch_blender')
try { $null = $mutex.WaitOne(1800000) } catch [System.Threading.AbandonedMutexException] {}
try {
    $log = Join-Path $env:TEMP ('lead_back_' + (Get-Date -Format 'HHmmss') + '.log')
    $p = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', $py, '--', $Ids, $Out) -PassThru -NoNewWindow -RedirectStandardOutput $log -RedirectStandardError ($log + '.err')
    $null = $p.WaitForExit(1500000)
} finally { $mutex.ReleaseMutex() }
Get-Content $log | Where-Object { $_ -match 'BACK_DONE|BACK_FAIL|Traceback' } | Select-Object -Last 3
"pictures: " + @(Get-ChildItem $Out -Filter *.png).Count
