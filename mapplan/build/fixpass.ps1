param([string]$area)
$dir = 'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\build'
$code = [IO.File]::ReadAllText("$dir\fixpass.luau").Replace('__DATA__', (@{ area = $area } | ConvertTo-Json -Compress))
$f = "$dir\_fix_$area.json"
[IO.File]::WriteAllText($f, (@{ code = $code } | ConvertTo-Json -Compress -Depth 3))
$r = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile $f
('{0} [fixpass] {1}' -f (Get-Date -Format 'HH:mm:ss'), $r) | Out-File "$dir\build_log.txt" -Append -Encoding utf8
$r
