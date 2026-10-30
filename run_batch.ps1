param(
    [string]$batch,
    [switch]$nolib
)
# Runs a Luau batch file in Roblox Studio via robloxstudio-mcp execute_luau.
# Prepends town\lib.lua (shared builders) unless -nolib is passed.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$base = 'http://localhost:58741/mcp'
$headers = @{
    'Accept'       = 'application/json, text/event-stream'
    'Content-Type' = 'application/json'
}
$code = ''
if (-not $nolib) { $code = (Get-Content (Join-Path $here 'lib.lua') -Raw) + "`n" + (Get-Content (Join-Path $here 'assets.lua') -Raw) + "`n" }
$code += (Get-Content $batch -Raw)

function ParseSse($content) {
    $m = [regex]::Match($content, 'data:\s*(\{.*\})', 'Singleline')
    if ($m.Success) { return $m.Groups[1].Value }
    return $content
}
function SendMcp($bodyObj, $timeout) {
    $json = $bodyObj | ConvertTo-Json -Depth 25 -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $resp = Invoke-WebRequest -Uri $base -Method POST -Headers $headers -Body $bytes -TimeoutSec $timeout -UseBasicParsing
    return (ParseSse $resp.Content)
}
SendMcp @{ jsonrpc='2.0'; id=1; method='initialize'; params=@{ protocolVersion='2024-11-05'; capabilities=@{}; clientInfo=@{ name='kiro'; version='1.0' } } } 30 | Out-Null
$callJson = SendMcp @{ jsonrpc='2.0'; id=2; method='tools/call'; params=@{ name='execute_luau'; arguments=@{ code=$code } } } 600
$parsed = $callJson | ConvertFrom-Json
if ($parsed.result.content) {
    foreach ($block in $parsed.result.content) { Write-Output $block.text }
} elseif ($parsed.error) {
    Write-Output ('MCP ERROR: ' + ($parsed.error | ConvertTo-Json -Compress))
} else {
    Write-Output $callJson
}
