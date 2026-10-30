param([string]$file, [string]$data = '')
$code = [IO.File]::ReadAllText($file)
if ($data) { $code = $code.Replace('__DATA__', [IO.File]::ReadAllText($data)) }
$f = [IO.Path]::ChangeExtension($file, '.call.json')
[IO.File]::WriteAllText($f, (@{ code = $code } | ConvertTo-Json -Compress -Depth 3))
powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile $f
