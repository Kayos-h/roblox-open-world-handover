param([string]$pos, [string]$look, [string]$name = 'shot')
# usage: cam.ps1 -pos "x,y,z" -look "x,y,z" -name foo
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tpl = Get-Content (Join-Path $here 'cam_template.lua') -Raw
$tpl = $tpl.Replace('CAMX', $pos).Replace('LOOKX', $look)
$tmp = Join-Path $here 'shots\_cam.lua'
New-Item -ItemType Directory -Force -Path (Join-Path $here 'shots') | Out-Null
Set-Content -Path $tmp -Value $tpl -Encoding UTF8
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here 'run_batch.ps1') -batch $tmp -nolib | Out-Null
Start-Sleep -Milliseconds 800
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here 'capture.ps1') -out (Join-Path $here "shots\$name.png")
