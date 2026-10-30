$log = 'C:\Users\Nitro\.kiro\crew\workspace\town\upload_log.txt'
try { & 'C:\Users\Nitro\.kiro\crew\workspace\town\upload_fbx.ps1' -file 'C:\Users\Nitro\.kiro\crew\workspace\town\library\lighting\A15_lamp_iron_city.fbx' -name 'A15_lamp_iron_city' *>&1 | Out-File $log -Encoding utf8 }
catch { ('ERR: ' + $_.Exception.ToString() + ' @ line ' + $_.InvocationInfo.ScriptLineNumber) | Out-File $log -Append -Encoding utf8 }
Get-Content $log
