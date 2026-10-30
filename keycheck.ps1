$ErrorActionPreference = 'Stop'
$key = [Environment]::GetEnvironmentVariable('ROBLOX_OPEN_CLOUD_API_KEY', 'User')
$uid = [Environment]::GetEnvironmentVariable('ROBLOX_CREATOR_USER_ID', 'User')
$gid = [Environment]::GetEnvironmentVariable('ROBLOX_CREATOR_GROUP_ID', 'User')
if (-not $key) { "KEY: not found in user environment"; exit }
$key = $key.Trim()
"KEY: present (length $($key.Length), value hidden)"
"USER ID set: $([bool]$uid) value: $uid   GROUP ID set: $([bool]$gid) value: $gid"

function Call($method, $url, $headers, $body) {
  try {
    $p = @{ Uri = $url; Method = $method; Headers = $headers; UseBasicParsing = $true; TimeoutSec = 20 }
    if ($body) { $p.Body = $body; $p.ContentType = 'application/json' }
    $r = Invoke-WebRequest @p
    return @($r.StatusCode, $r.Content)
  } catch {
    $code = 0; $txt = $_.Exception.Message
    if ($_.Exception.Response) {
      $code = [int]$_.Exception.Response.StatusCode
      try { $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream()); $txt = $sr.ReadToEnd() } catch {}
    }
    return @($code, $txt)
  }
}

$body = @{ apiKey = $key } | ConvertTo-Json
$r = Call 'POST' 'https://apis.roblox.com/api-keys/v1/introspect' @{} $body
"introspect: HTTP $($r[0])"
if ($r[0] -eq 200) {
  $i = $r[1] | ConvertFrom-Json
  "  name: $($i.name)"
  "  owner user id: $($i.authorizedUserId)"
  "  enabled: $($i.enabled)  expired: $($i.expired)  expires: $($i.expirationTime)"
  foreach ($s in $i.scopes) { "  scope: $($s.name) -> $(($s.operations) -join ',')" }
} else { "  body: $($r[1].Substring(0, [Math]::Min(300, $r[1].Length)))" }

$r2 = Call 'GET' 'https://apis.roblox.com/assets/v1/operations/00000000-0000-0000-0000-000000000000' @{ 'x-api-key' = $key } $null
"assets api: HTTP $($r2[0])"
if ($r2[0] -ne 404 -and $r2[0] -ne 400) { "  body: $($r2[1].Substring(0, [Math]::Min(300, $r2[1].Length)))" }
