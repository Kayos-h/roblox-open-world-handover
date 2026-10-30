$src = [IO.File]::ReadAllText('C:\Users\Nitro\.kiro\crew\workspace\town\devtools\DevFlyMode.lua')
if ($src.Contains(']==]')) { throw 'source contains ]==]' }
$code = "local sps=game:GetService('StarterPlayer'):WaitForChild('StarterPlayerScripts') local old=sps:FindFirstChild('DevFlyMode') if old then old:Destroy() end local s=Instance.new('LocalScript') s.Name='DevFlyMode' s.Source=[==[" + $src + "]==] s.Parent=sps return 'installed '..#s.Source..' chars in '..s:GetFullName()"
$f = 'C:\Users\Nitro\.kiro\crew\workspace\town\devtools\_install.json'
[IO.File]::WriteAllText($f, (@{ code = $code } | ConvertTo-Json -Compress))
powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile $f
