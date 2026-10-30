param([string]$file, [string]$name)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$key = ([Environment]::GetEnvironmentVariable('ROBLOX_OPEN_CLOUD_API_KEY', 'User')).Trim()
$uid = [Environment]::GetEnvironmentVariable('ROBLOX_CREATOR_USER_ID', 'User')
$req = @{ assetType = 'Model'; displayName = $name; description = 'BUILD map model'; creationContext = @{ creator = @{ userId = "$uid" } } } | ConvertTo-Json -Depth 5 -Compress

$client = New-Object System.Net.Http.HttpClient
$client.DefaultRequestHeaders.Add('x-api-key', $key)
$form = New-Object System.Net.Http.MultipartFormDataContent
$form.Add((New-Object System.Net.Http.StringContent($req)), 'request')
$bytes = [IO.File]::ReadAllBytes($file)
$fc = New-Object System.Net.Http.ByteArrayContent(,$bytes)
$fc.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('model/fbx')
$form.Add($fc, 'fileContent', [IO.Path]::GetFileName($file))
$resp = $client.PostAsync('https://apis.roblox.com/assets/v1/assets', $form).Result
$txt = $resp.Content.ReadAsStringAsync().Result
"upload: HTTP $([int]$resp.StatusCode)"
if (-not $resp.IsSuccessStatusCode) { "  body: $txt"; exit }
$op = $txt | ConvertFrom-Json
$opPath = $op.path
"operation: $opPath"
for ($i = 0; $i -lt 30; $i++) {
  Start-Sleep -Seconds 3
  $r = $client.GetAsync("https://apis.roblox.com/assets/v1/$opPath").Result
  $j = $r.Content.ReadAsStringAsync().Result | ConvertFrom-Json
  if ($j.done) {
    if ($j.response) { "ASSET_ID: $($j.response.assetId)"; "moderation: $($j.response.moderationResult.moderationState)" }
    else { "failed: $(($j | ConvertTo-Json -Depth 6 -Compress))" }
    exit
  }
}
"timed out waiting; operation still running: $opPath"
