param([string]$only = '', [int]$limit = 0)
# Uploads library FBX files to Roblox via Open Cloud and records asset IDs.
#   Test one model:   -only A15_lamp_iron_city
#   Upload a folder:  -only harbour
#   Upload all:       (no arguments)
# Already-uploaded models (listed in asset_ids.csv) are skipped, so it is safe to re-run.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$csv = 'C:\Users\Nitro\.kiro\crew\workspace\town\asset_ids.csv'
$key = ([Environment]::GetEnvironmentVariable('ROBLOX_OPEN_CLOUD_API_KEY', 'User')).Trim()
$uid = [Environment]::GetEnvironmentVariable('ROBLOX_CREATOR_USER_ID', 'User')
if (-not $key -or -not $uid) { Write-Host 'Key or user ID not set.' -ForegroundColor Red; exit 1 }

$done = @{}
if (Test-Path $csv) { Import-Csv $csv | ForEach-Object { if ($_.asset_id) { $done[$_.name] = $_.asset_id } } }
else { 'folder,name,asset_id,moderation' | Out-File $csv -Encoding utf8 }

$folders = 'roads','lighting','nature','props','capital','castle','rusty','alpine','elf','harbour','between','town1'
$files = foreach ($f in $folders) { Get-ChildItem (Join-Path $lib $f) -Filter *.fbx -ErrorAction SilentlyContinue }
if ($only) { $files = $files | Where-Object { $_.BaseName -eq $only -or $_.Directory.Name -eq $only } }
$files = @($files | Where-Object { -not $done.ContainsKey($_.BaseName) })
if ($limit -gt 0) { $files = @($files | Select-Object -First $limit) }
Write-Host "$($files.Count) model(s) to upload."

$client = New-Object System.Net.Http.HttpClient
$client.Timeout = [TimeSpan]::FromMinutes(5)
$client.DefaultRequestHeaders.Add('x-api-key', $key)
$n = 0
foreach ($file in $files) {
  $n++
  $name = $file.BaseName
  Write-Host "[$n/$($files.Count)] $name ... " -NoNewline
  $req = @{ assetType = 'Model'; displayName = $name.Substring(0, [Math]::Min(50, $name.Length)); description = 'Phase 1 map model'; creationContext = @{ creator = @{ userId = "$uid" } } } | ConvertTo-Json -Depth 5 -Compress
  $attempt = 0
  while ($true) {
    $attempt++
    $form = New-Object System.Net.Http.MultipartFormDataContent
    $form.Add((New-Object System.Net.Http.StringContent($req)), 'request')
    $fc = New-Object System.Net.Http.ByteArrayContent(, [IO.File]::ReadAllBytes($file.FullName))
    $fc.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('model/fbx')
    $form.Add($fc, 'fileContent', $file.Name)
    $resp = $client.PostAsync('https://apis.roblox.com/assets/v1/assets', $form).Result
    $txt = $resp.Content.ReadAsStringAsync().Result
    if ([int]$resp.StatusCode -eq 429 -and $attempt -lt 6) { Write-Host 'rate limited, waiting 30s ... ' -NoNewline; Start-Sleep 30; continue }
    break
  }
  if (-not $resp.IsSuccessStatusCode) { Write-Host "FAILED HTTP $([int]$resp.StatusCode): $txt" -ForegroundColor Red; continue }
  $opPath = ($txt | ConvertFrom-Json).path
  $id = ''; $mod = ''
  for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 3
    $j = $client.GetAsync("https://apis.roblox.com/assets/v1/$opPath").Result.Content.ReadAsStringAsync().Result | ConvertFrom-Json
    if ($j.done) { if ($j.response) { $id = $j.response.assetId; $mod = $j.response.moderationResult.moderationState }; break }
  }
  if ($id) {
    "$($file.Directory.Name),$name,$id,$mod" | Out-File $csv -Append -Encoding utf8
    Write-Host "OK $id ($mod)" -ForegroundColor Green
  } else { Write-Host "processing did not finish: $opPath" -ForegroundColor Yellow }
  Start-Sleep -Milliseconds 500
}
Write-Host "Done. Asset IDs are in $csv"
