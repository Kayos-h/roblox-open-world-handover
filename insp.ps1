param([string]$code)
# usage: insp.ps1 -code "return describe(loadAsset(123), 3)"  (prepends assets.lua, no lib)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tmp = Join-Path $here '_insp_run.lua'
Set-Content -Path $tmp -Value ((Get-Content (Join-Path $here 'assets.lua') -Raw) + "`n" + $code) -NoNewline
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here 'run_batch.ps1') -batch $tmp -nolib
