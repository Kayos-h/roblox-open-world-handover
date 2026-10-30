$base = 'http://localhost:58741/mcp'
$headers = @{ 'Accept' = 'application/json, text/event-stream'; 'Content-Type' = 'application/json' }
function SendMcp($bodyObj) {
    $json = $bodyObj | ConvertTo-Json -Depth 25 -Compress
    $resp = Invoke-WebRequest -Uri $base -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -TimeoutSec 30 -UseBasicParsing
    $m = [regex]::Match($resp.Content, 'data:\s*(\{.*\})', 'Singleline')
    if ($m.Success) { return $m.Groups[1].Value } else { return $resp.Content }
}
SendMcp @{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='kiro'; version='1.0' } } } | Out-Null
$r = SendMcp @{ jsonrpc='2.0'; id=2; method='tools/list'; params=@{} } | ConvertFrom-Json
foreach ($t in $r.result.tools) { Write-Output ($t.name + ' :: ' + ($t.description -replace "`n",' ').Substring(0, [Math]::Min(160, $t.description.Length))) }
