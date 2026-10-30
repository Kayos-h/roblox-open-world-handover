param([string]$argsFile)
for ($t = 1; $t -le 12; $t++) {
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\mcp_call.ps1' -tool execute_luau -argsFile $argsFile 2>&1 | Out-String
  $m = [regex]::Match($r, '"returnValue":"((?:[^"\\]|\\.)*)"')
  if ($m.Success) { ($m.Groups[1].Value -replace '\\n', "`n" -replace '\\"', '"'); exit 0 }
  if ($r -match '"success":false') { 'LUAU ERROR: ' + [regex]::Match($r, '"error":"((?:[^"\\]|\\.)*)"').Groups[1].Value; exit 1 }
  Start-Sleep -Seconds 4
}
'FAILED after 12 tries'
