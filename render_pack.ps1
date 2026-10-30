param([Parameter(Mandatory=$true)][string]$Tag)
# Background job: back view of every pack model and four-angle sheets for the big ones, from the SAVED library files, into library\v5_work\<Tag>\back and \quad.
# Serialized with the scratch queue mutex. Log: library\v5_work\<Tag>\render.log
$L = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$W = "$L\v5_work\$Tag"
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$log = "$W\render.log"
"start " + (Get-Date -Format 'HH:mm:ss') | Out-File $log
Remove-Item "$W\back" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$W\quad" -Recurse -Force -ErrorAction SilentlyContinue
$mutex = New-Object System.Threading.Mutex($false, 'Global\v5_scratch_blender')
try { $null = $mutex.WaitOne(3600000) } catch [System.Threading.AbandonedMutexException] {}
try {
    $p1 = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', "$L\src\v5_backview.py", '--', "$W\pack_ids.json", "$W\back") -PassThru -NoNewWindow -RedirectStandardOutput "$W\back.out" -RedirectStandardError "$W\back.err"
    $null = $p1.WaitForExit(2400000)
    "back views finished " + (Get-Date -Format 'HH:mm:ss') + "  " + ((Get-Content "$W\back.out" | Where-Object { $_ -match 'BACK_DONE|BACK_FAIL' }) -join ' ') | Out-File $log -Append
    $ids = (Get-Content "$W\quad_ids.json" | ConvertFrom-Json) -join ','
    $p2 = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', "$L\src\v5_quad.py", '--', $ids, "$W\quad") -PassThru -NoNewWindow -RedirectStandardOutput "$W\quad.out" -RedirectStandardError "$W\quad.err"
    $null = $p2.WaitForExit(2400000)
    "four-angle finished " + (Get-Date -Format 'HH:mm:ss') + "  OK " + @(Get-Content "$W\quad.out" | Where-Object { $_ -match 'QUAD_OK' }).Count + "  FAIL " + @(Get-Content "$W\quad.out" | Where-Object { $_ -match 'QUAD_FAIL' }).Count | Out-File $log -Append
} finally { $mutex.ReleaseMutex() }
"DONE " + (Get-Date -Format 'HH:mm:ss') | Out-File $log -Append
