param([string]$mode, [string]$csv, [string]$dir)
# photo run: photo mode on/off + tour + camera restore + numeric blank check (no human or model looks at the pictures here)
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$rb = "$town\rebuild"
$pm = [IO.File]::ReadAllText("$rb\v4\photo_mode.luau").Replace('__MODE__', $mode)
$pf = "$rb\v4\_photo_mode.luau"
[IO.File]::WriteAllText($pf, $pm)
Write-Output (& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\runluau.ps1" -file $pf | Out-String).Trim()
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\tour.ps1" -views $csv -dir $dir | ForEach-Object { Write-Output $_ }
# restore the game atmosphere and the camera
$pm2 = [IO.File]::ReadAllText("$rb\v4\photo_mode.luau").Replace('__MODE__', 'off')
[IO.File]::WriteAllText($pf, $pm2)
Write-Output (& powershell -NoProfile -ExecutionPolicy Bypass -File "$rb\runluau.ps1" -file $pf | Out-String).Trim()
& powershell -NoProfile -ExecutionPolicy Bypass -File "$town\mcp_call.ps1" -tool execute_luau -argsFile "$town\_cam_restore.json" | Out-Null
Add-Type -AssemblyName System.Drawing
Get-ChildItem $dir -Filter '*.jpg' | ForEach-Object {
  $im = [System.Drawing.Bitmap]::FromFile($_.FullName)
  $sm = New-Object System.Drawing.Bitmap 48, 30
  $g = [System.Drawing.Graphics]::FromImage($sm); $g.DrawImage($im, 0, 0, 48, 30); $g.Dispose()
  $vals = New-Object System.Collections.Generic.List[double]
  for ($y = 0; $y -lt 30; $y++) { for ($x = 0; $x -lt 48; $x++) { $c = $sm.GetPixel($x, $y); $vals.Add(($c.R + $c.G + $c.B) / 3.0) } }
  $mean = ($vals | Measure-Object -Average).Average
  $var = ($vals | ForEach-Object { ($_ - $mean) * ($_ - $mean) } | Measure-Object -Average).Average
  $sm.Dispose(); $im.Dispose()
  Write-Output ('{0}  {1} KB  mean {2:N0}  std {3:N0}' -f $_.Name, [math]::Round($_.Length / 1KB), $mean, [math]::Sqrt($var))
}

