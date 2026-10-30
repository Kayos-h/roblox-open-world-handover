param([string]$only = '', [int]$limit = 0)
# Uploads the V4 Blender models (the ones listed in library\v4_meta.json) to Roblox via Open Cloud and records asset IDs in asset_ids.csv.
#   Upload everything not yet uploaded:  (no arguments)
#   One folder:                          -only v4_castle
#   One model:                           -only B02_01_keep
# Models already listed in asset_ids.csv are skipped, so it is safe to run again after a failure.
$ErrorActionPreference = 'Stop'
# log everything to a file so progress can be checked, and keep the PC awake while this runs
try { Start-Transcript -Path 'C:\Users\Nitro\.kiro\crew\workspace\town\upload_v4_log.txt' -Append | Out-Null } catch {}
try {
  Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);' -ErrorAction Stop
  [Win32.Power]::SetThreadExecutionState([uint32]2147483649) | Out-Null   # ES_CONTINUOUS + ES_SYSTEM_REQUIRED
} catch {}
Add-Type -AssemblyName System.Net.Http
$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$csv = 'C:\Users\Nitro\.kiro\crew\workspace\town\asset_ids.csv'
$key = ([Environment]::GetEnvironmentVariable('ROBLOX_OPEN_CLOUD_API_KEY', 'User')).Trim()
$uid = [Environment]::GetEnvironmentVariable('ROBLOX_CREATOR_USER_ID', 'User')
if (-not $key -or -not $uid) { Write-Host 'Key or user ID not set.' -ForegroundColor Red; exit 1 }

$done = @{}
if (Test-Path $csv) { Import-Csv $csv | ForEach-Object { if ($_.asset_id) { $done[$_.name] = $_.asset_id } } }
else { 'folder,name,asset_id,moderation' | Out-File $csv -Encoding utf8 }

$meta = Get-Content (Join-Path $lib 'v4_meta.json') -Raw | ConvertFrom-Json
$files = @()
foreach ($p in $meta.PSObject.Properties) {
  $id = $p.Name; $cat = $p.Value.category
  if ($id -like 'ZZ_*' -or $id -eq 'EV01_treehouse_a' -or $cat -eq 'v4_test') { continue }
  $fbx = Join-Path (Join-Path $lib $cat) ($id + '.fbx')
  if (Test-Path $fbx) { $files += Get-Item $fbx }
}
if ($only) { $files = $files | Where-Object { $_.BaseName -eq $only -or $_.Directory.Name -eq $only } }
$files = @($files | Where-Object { -not $done.ContainsKey($_.BaseName) })
if ($limit -gt 0) { $files = @($files | Select-Object -First $limit) }
Write-Host "$($files.Count) model(s) to upload."

$client = New-Object System.Net.Http.HttpClient
$client.Timeout = [TimeSpan]::FromMinutes(5)
$client.DefaultRequestHeaders.Add('x-api-key', $key)
$n = 0; $ok = 0; $bad = 0
foreach ($file in $files) {
  $n++
  $name = $file.BaseName
  Write-Host "[$n/$($files.Count)] $name ... " -NoNewline
  $req = @{ assetType = 'Model'; displayName = $name.Substring(0, [Math]::Min(50, $name.Length)); description = 'Phase 1 map model (v4)'; creationContext = @{ creator = @{ userId = "$uid" } } } | ConvertTo-Json -Depth 5 -Compress
  $attempt = 0
  while ($true) {
    $attempt++
    $form = New-Object System.Net.Http.MultipartFormDataContent
    $form.Add((New-Object System.Net.Http.StringContent($req)), 'request')
    $fc = New-Object System.Net.Http.ByteArrayContent(, [IO.File]::ReadAllBytes($file.FullName))
    $fc.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('model/fbx')
    $form.Add($fc, 'fileContent', $file.Name)
    try { $resp = $client.PostAsync('https://apis.roblox.com/assets/v1/assets', $form).Result } catch { Write-Host "network error, retrying in 20s ... " -NoNewline; Start-Sleep 20; if ($attempt -lt 6) { continue } else { $resp = $null; break } }
    $txt = $resp.Content.ReadAsStringAsync().Result
    if ([int]$resp.StatusCode -eq 429 -and $attempt -lt 6) { Write-Host 'rate limited, waiting 30s ... ' -NoNewline; Start-Sleep 30; continue }
    break
  }
  if (-not $resp -or -not $resp.IsSuccessStatusCode) { $bad++; Write-Host "FAILED $txt" -ForegroundColor Red; continue }
  $opPath = ($txt | ConvertFrom-Json).path
  $id = ''; $mod = ''
  for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 3
    $j = $client.GetAsync("https://apis.roblox.com/assets/v1/$opPath").Result.Content.ReadAsStringAsync().Result | ConvertFrom-Json
    if ($j.done) { if ($j.response) { $id = $j.response.assetId; $mod = $j.response.moderationResult.moderationState }; break }
  }
  if ($id) {
    $ok++
    "$($file.Directory.Name),$name,$id,$mod" | Out-File $csv -Append -Encoding utf8
    Write-Host "OK $id ($mod)" -ForegroundColor Green
  } else { $bad++; Write-Host "processing did not finish: $opPath" -ForegroundColor Yellow }
  Start-Sleep -Milliseconds 500
}
Write-Host "Done: $ok uploaded, $bad not finished (run again to retry). Asset IDs are in $csv"
try { Stop-Transcript | Out-Null } catch {}
