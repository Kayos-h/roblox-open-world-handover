param([Parameter(Mandatory=$true)][string]$A, [Parameter(Mandatory=$true)][string]$Modules, [int]$SkipScratch = 0)
# Integrate one builder's finished fix modules. $Modules = "module:worker,module:worker".
# Per module: (1) independent numbers pass through the serialized scratch queue (small renders), (2) LIVE build in the open Blender into the library
# (round 1 was archived first), (3) afterwards the file / budget / palette verification for the whole assignment. Prints compact lines only.
$T = 'C:\Users\Nitro\.kiro\crew\workspace\town'
foreach ($mw in ($Modules -split ',')) {
    $mod, $w = $mw -split ':'
    "=== $A  $mod  (worker $w)"
    if (-not $SkipScratch) {
        $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$T\scratch.ps1" -Module $mod -Ids 'ALL' -Tag ("lead_" + $A) -Views 1 -Res 200 -Samples 4 -TimeoutSec 1200
        $s = @($r | Where-Object { $_ -match '^SCRATCH [A-Z]' })
        if ($s.Count -eq 0) { "SCRATCH CHECK DID NOT RUN (0 models built): stop and investigate"; $r | Select-Object -First 5 }
        $bad = @($r | Where-Object { $_ -match 'NOT_FOUND|SCRATCH_ERROR|TIMEOUT|BUSY|Traceback' })
        $fl = @($s | Where-Object { $_ -notmatch 'FLOAT 0' }).Count
        $inv = @($s | Where-Object { $_ -notmatch 'INV 0' }).Count
        $sz = @($s | Where-Object { $_ -match '\| [^|]*SIZE' }).Count
        $tr = @($s | Where-Object { $_ -match '\| [^|]*TRIS' }).Count
        $lo = @($s | Where-Object { $_ -match '\| [^|]*LOW' }).Count
        "scratch: built $($s.Count)  errors/missing $($bad.Count)  INV>0 $inv  over-budget $tr  size-flag $sz  low-tris $lo  float>0 $fl"
        $bad | ForEach-Object { $_.Substring(0, [Math]::Min(300, $_.Length)) }
        $s | Where-Object { $_ -notmatch 'INV 0' -or $_ -match '\| [^|]*TRIS' } | ForEach-Object { 'PROBLEM ' + $_.Substring(0, [Math]::Min(240, $_.Length)) }
    }
    $o = & powershell -NoProfile -ExecutionPolicy Bypass -File "$T\live_batch.ps1" -Module $mod -Worker $w -TimeoutSec 1200
    $o | Where-Object { $_ -match '^(CHUNK|LIVE_DONE|NO_SUCH|BLENDER ERROR|Traceback|error:)|ERROR' } | ForEach-Object { $_.TrimEnd() }
}
python "$T\library\src\v5_fix_verify.py" $A
