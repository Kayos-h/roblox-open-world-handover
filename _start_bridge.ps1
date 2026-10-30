Start-Process cmd.exe -ArgumentList '/k','npx -y robloxstudio-mcp' -WindowStyle Normal
foreach ($i in 1..12) {
  Start-Sleep -Seconds 5
  $c = Get-NetTCPConnection -LocalPort 58741 -State Listen -ErrorAction SilentlyContinue
  "t=$($i*5)s listening=" + [bool]$c + " node=" + ((Get-Process node -ErrorAction SilentlyContinue | Measure-Object).Count)
}
try { (Invoke-WebRequest -Uri http://localhost:58741/health -UseBasicParsing -TimeoutSec 5).Content } catch { "health failed: $_" }
