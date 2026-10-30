param([string]$tool, [string]$argsFile, [switch]$schema)
# Calls any robloxstudio-mcp tool. -schema prints the tool's description + input schema.
$base = 'http://localhost:58741/mcp'
$headers = @{ 'Accept' = 'application/json, text/event-stream'; 'Content-Type' = 'application/json' }
function SendMcp($json, $timeout) {
    $resp = Invoke-WebRequest -Uri $base -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -TimeoutSec $timeout -UseBasicParsing
    $m = [regex]::Match($resp.Content, 'data:\s*(\{.*\})', 'Singleline')
    if ($m.Success) { return $m.Groups[1].Value } else { return $resp.Content }
}
SendMcp '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"kiro","version":"1.0"}}}' 30 | Out-Null
if ($schema) {
    $r = SendMcp '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' 30 | ConvertFrom-Json
    foreach ($t in $r.result.tools) { if ($t.name -eq $tool) { Write-Output $t.description; Write-Output ($t.inputSchema | ConvertTo-Json -Depth 10) } }
    exit
}
$argJson = Get-Content $argsFile -Raw
$body = '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"' + $tool + '","arguments":' + $argJson + '}}'
$res = SendMcp $body 600 | ConvertFrom-Json
if ($res.result.content) { foreach ($b in $res.result.content) { if ($b.type -eq 'text') { Write-Output $b.text } else { Write-Output ('[' + $b.type + ' block]') } } }
else { Write-Output ($res | ConvertTo-Json -Depth 8 -Compress) }
