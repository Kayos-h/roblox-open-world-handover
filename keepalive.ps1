$log = 'C:\Users\Nitro\.kiro\crew\workspace\town\keepalive_log.txt'
$args1 = 'C:\Users\Nitro\.kiro\crew\workspace\town\_keepalive_args.json'
'{"code":"return 1"}' | Out-File $args1 -Encoding ascii
$stop = (Get-Date).AddHours(11)
while ((Get-Date) -lt $stop) {
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\mcp_call.ps1' -tool execute_luau -argsFile $args1 2>&1 | Out-String
  $ok = $r -match 'success'
  ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $(if ($ok) { 'OK' } else { 'FAIL ' + $r.Trim().Substring(0, [Math]::Min(160, $r.Trim().Length)) })) | Out-File $log -Append -Encoding utf8
  Start-Sleep -Seconds 60
}
