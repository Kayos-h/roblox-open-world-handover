param([string]$ids)
# usage: probe_assets.ps1 -ids "123,456"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tmp = Join-Path $here '_probe_run.lua'
$body = '_G.__probeIds = {' + $ids + '}' + "`n" + (Get-Content (Join-Path $here 'probe_assets.lua') -Raw)
Set-Content -Path $tmp -Value $body -NoNewline
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here 'run_batch.ps1') -batch $tmp -nolib
