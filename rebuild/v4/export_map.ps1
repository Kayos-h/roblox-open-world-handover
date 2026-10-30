param([int]$x0 = -3360, [int]$x1 = 3360, [int]$z0 = -3360, [int]$z1 = 2400, [int]$step = 24, [int]$band = 40)
# Exports the real terrain surface to rebuild\v4\terrain_map.json in z bands (each band is one Studio call).
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$tpl = [IO.File]::ReadAllText("$rb\v4\export_map.luau")
$all = New-Object System.Collections.Generic.List[string]
$z = $z0
$tmp = "$rb\v4\_export_args.json"
while ($z -le $z1) {
  $zEnd = [Math]::Min($z1, $z + ($band - 1) * $step)
  $data = @{ x0 = $x0; x1 = $x1; z0 = $z; z1 = $zEnd; step = $step } | ConvertTo-Json -Compress
  $code = $tpl.Replace('__DATA__', $data)
  [IO.File]::WriteAllText($tmp, (@{ code = $code } | ConvertTo-Json -Compress -Depth 3))
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\studio.ps1" -argsFile $tmp | Out-String
  $r = $r.Trim()
  if (-not $r.StartsWith('[')) { Write-Output ("band z=$z failed: " + $r.Substring(0, [Math]::Min(200, $r.Length))); exit 1 }
  $rows = $r | ConvertFrom-Json
  foreach ($row in $rows) { $all.Add($row) }
  Write-Output ("band z=$z..$zEnd rows=" + @($rows).Count)
  $z = $zEnd + $step
}
$out = @{ x0 = $x0; x1 = $x1; z0 = $z0; z1 = $z1; step = $step; rows = $all } | ConvertTo-Json -Compress -Depth 4
[IO.File]::WriteAllText("$rb\v4\terrain_map.json", $out)
Write-Output ("wrote terrain_map.json rows=" + $all.Count)
