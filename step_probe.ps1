$log = 'C:\Users\Nitro\.kiro\crew\workspace\town\step_log.txt'
'start' | Out-File $log -Encoding utf8
Add-Type -AssemblyName System.Net.Http
'addtype ok' | Out-File $log -Append -Encoding utf8
$b = [IO.File]::ReadAllBytes('C:\Users\Nitro\.kiro\crew\workspace\town\library\lighting\A15_lamp_iron_city.fbx')
"read ok $($b.Length)" | Out-File $log -Append -Encoding utf8
$c = New-Object System.Net.Http.HttpClient
$r = $c.GetAsync('https://apis.roblox.com/assets/v1/operations/00000000-0000-0000-0000-000000000000').Result
"get ok $([int]$r.StatusCode)" | Out-File $log -Append -Encoding utf8
