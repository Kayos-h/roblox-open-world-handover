# Background job: four-angle sheets (2 x 2, 3/4 front, 3/4 back, close-up, elevation) of every rebuilt model, from the fix modules (same geometry as the library).
# Output: library\v5_work\fix_scratch\rev\<id>.png . Runs through the serialized scratch queue. Writes a log and a DONE line.
$T = 'C:\Users\Nitro\.kiro\crew\workspace\town'
New-Item -ItemType Directory -Force -Path "$T\library\v5_work\r2" | Out-Null
$log = "$T\library\v5_work\r2\rev_quads.log"
"start " + (Get-Date -Format 'HH:mm:ss') | Out-File $log
$mods = 'v5_fx_vi_a', 'v5_fx_vi_b', 'v5_fx_vh', 'v5_fx_vg', 'v5_fx_vc', 'v5_fx_vd', 'v5_fx_ve', 'v5_fx_vf', 'v5_fx_va', 'v5_fx_vb', 'v5_fx_vj'
foreach ($m in $mods) {
    $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$T\scratch.ps1" -Module $m -Ids ALL -Tag rev -Views 4 -Res 400 -Samples 8 -TimeoutSec 1500
    $n = @($r | Where-Object { $_ -match '^SCRATCH [A-Z]' }).Count
    "$m built $n  " + (Get-Date -Format 'HH:mm:ss') | Out-File $log -Append
}
"DONE " + (Get-Date -Format 'HH:mm:ss') | Out-File $log -Append
