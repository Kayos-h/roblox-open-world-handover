# Renders the four-angle review sheets of the big landmark pieces in two headless Blenders at once (the open Blender is not touched).
$exe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$py = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_quad.py'
$all = @(& python 'C:\Users\Nitro\.kiro\crew\workspace\town\_ids.py' WT01 WT02 WT05 WT12 CP07 CP09 CP15 LM03 LM22 LM25 LM30 LM09 LM15 VC02 RW02 LM01 LM02 FL01 CP19 BR01)
$half = [math]::Ceiling($all.Count / 2)
$a = ($all[0..($half - 1)]) -join ','
$b = ($all[$half..($all.Count - 1)]) -join ','
$l1 = Join-Path $env:TEMP 'quad1.log'
$l2 = Join-Path $env:TEMP 'quad2.log'
$p1 = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', $py, '--', $a) -PassThru -NoNewWindow -RedirectStandardOutput $l1 -RedirectStandardError ($l1 + '.err')
$p2 = Start-Process -FilePath $exe -ArgumentList @('-b', '--factory-startup', '--python', $py, '--', $b) -PassThru -NoNewWindow -RedirectStandardOutput $l2 -RedirectStandardError ($l2 + '.err')
$null = $p1.WaitForExit(900000)
$null = $p2.WaitForExit(900000)
Write-Output ('models: ' + $all.Count)
Get-Content $l1, $l2 | Where-Object { $_ -match 'QUAD_' } | Group-Object { $_.Split(' ')[0] } | ForEach-Object { $_.Name + ' x' + $_.Count }
Get-Content $l1, $l2 | Where-Object { $_ -match 'QUAD_FAIL' }
