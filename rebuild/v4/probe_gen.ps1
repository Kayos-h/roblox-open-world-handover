param([string]$pts = '[[3002,-1698],[3006,-1698],[3042,-1698],[302,2302],[302,2502]]')
# runs rebuild\v4\_probe_gen.luau with the real world.json and the given column list; read-only (no terrain writes)
$rb = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
& python "$rb\v4\_make_probe_gen.py" | Out-Null
$world = [IO.File]::ReadAllText("$rb\world.json")
$data = '{"world":' + $world + ',"opt":{"pts":' + $pts + '}}'
$code = [IO.File]::ReadAllText("$rb\v4\_probe_gen.luau").Replace('__DATA__', $data)
$f = "$rb\v4\_probe_gen.call.json"
[IO.File]::WriteAllText($f, (@{ code = $code } | ConvertTo-Json -Compress -Depth 3))
& powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile $f
