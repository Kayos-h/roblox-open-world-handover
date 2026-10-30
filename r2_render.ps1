# Background job for the second review: (1) a back view of every pack model, (2) four-angle sheets for the 89 big/complex changed models.
# Serialized with the scratch queue mutex. Log: library\v5_work\r2\render.log
$T = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$L = "$T\library"
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$log = "$L\v5_work\r2\render.log"
"start " + (Get-Date -Format 'HH:mm:ss') | Out-File $log
$mutex = New-Object System.Threading.Mutex($false, 'Global\v5_scratch_blender')
try { $null = $mutex.WaitOne(3600000) } catch [System.Threading.AbandonedMutexException] {}
try {
    $p1 = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', "$L\src\v5_backview.py", '--', "$L\v5_work\r2\pack_ids.json", "$L\v5_work\r2\back") -PassThru -NoNewWindow -RedirectStandardOutput "$L\v5_work\r2\back.out" -RedirectStandardError "$L\v5_work\r2\back.err"
    $null = $p1.WaitForExit(3000000)
    "back views finished " + (Get-Date -Format 'HH:mm:ss') + "  " + ((Get-Content "$L\v5_work\r2\back.out" | Where-Object { $_ -match 'BACK_DONE|BACK_FAIL' }) -join ' ') | Out-File $log -Append
    $ids = (Get-Content "$L\v5_work\r2\quad_ids.json" | ConvertFrom-Json | ForEach-Object { $_.id }) -join ','
    $p2 = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', "$L\src\v5_quad.py", '--', $ids, "$L\v5_work\r2\quad") -PassThru -NoNewWindow -RedirectStandardOutput "$L\v5_work\r2\quad.out" -RedirectStandardError "$L\v5_work\r2\quad.err"
    $null = $p2.WaitForExit(3000000)
    "four-angle finished " + (Get-Date -Format 'HH:mm:ss') + "  OK " + @(Get-Content "$L\v5_work\r2\quad.out" | Where-Object { $_ -match 'QUAD_OK' }).Count + "  FAIL " + @(Get-Content "$L\v5_work\r2\quad.out" | Where-Object { $_ -match 'QUAD_FAIL' }).Count | Out-File $log -Append
} finally { $mutex.ReleaseMutex() }
"DONE " + (Get-Date -Format 'HH:mm:ss') | Out-File $log -Append
