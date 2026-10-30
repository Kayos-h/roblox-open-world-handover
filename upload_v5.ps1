param([string]$only = '', [int]$limit = 0, [switch]$dry)
# Uploads the V5 Blender models to Roblox via Open Cloud and records asset IDs in asset_ids.csv (same table the V4 models use).
# DRAFT, not yet run: Blender is parked, so no V5 FBX files exist yet.
#   Preview only (no key, no network):   .\upload_v5.ps1 -dry
#   Upload everything not yet uploaded:  .\upload_v5.ps1
#   One folder:                          .\upload_v5.ps1 -only v5_wizard
#   One model:                           .\upload_v5.ps1 -only WT01_01_wizard_tower_shell
# Which models: the ids in plan_v5\V5_MANIFEST.csv (reworks excluded) that are built (listed in library\v4_meta.json after `python library\src\v4_merge.py`
# and with an .fbx on disk) and not yet in asset_ids.csv. Safe to run again after a failure. The key is read from the environment and never printed.
# Reworks (RW01, RW02) replace existing models: remove the old row from asset_ids.csv first, upload the new FBX under the OLD id.
$ErrorActionPreference = 'Stop'
$base = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$lib = "$base\library"
$csv = "$base\asset_ids.csv"
if (-not $dry) {
  try { Start-Transcript -Path "$base\upload_v5_log.txt" -Append | Out-Null } catch {}
  try {
    Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);' -ErrorAction Stop
    [Win32.Power]::SetThreadExecutionState([uint32]2147483649) | Out-Null   # ES_CONTINUOUS + ES_SYSTEM_REQUIRED
  } catch {}
}
Add-Type -AssemblyName System.Net.Http

$v5 = @{}
Import-Csv "$base\plan_v5\V5_MANIFEST.csv" | ForEach-Object { if ($_.rework -ne 'True' -and $_.rework -ne 'true' -and $_.row -notlike 'RW*') { $v5[$_.id] = 1 } }
$done = @{}
if (Test-Path $csv) { Import-Csv $csv | ForEach-Object { if ($_.asset_id) { $done[$_.name] = $_.asset_id } } }
else { 'folder,name,asset_id,moderation' | Out-File $csv -Encoding utf8 }

$meta = Get-Content "$lib\v4_meta.json" -Raw | ConvertFrom-Json
$files = @()
$notBuilt = 0
foreach ($id in $v5.Keys) {
  $m = $meta.PSObject.Properties[$id]
  if (-not $m) { $notBuilt++; continue }
  $fbx = Join-Path (Join-Path $lib $m.Value.category) ($id + '.fbx')
  if (Test-Path $fbx) { $files += Get-Item $fbx } else { $notBuilt++ }
}
if ($only) { $files = $files | Where-Object { $_.BaseName -eq $only -or $_.Directory.Name -eq $only } }
$files = @($files | Where-Object { -not $done.ContainsKey($_.BaseName) } | Sort-Object Name)
if ($limit -gt 0) { $files = @($files | Select-Object -First $limit) }
$mb = [math]::Round((($files | Measure-Object Length -Sum).Sum) / 1MB, 1)
Write-Host "$($files.Count) V5 model(s) to upload ($mb MB); $notBuilt V5 ids not built yet; $($done.Count) assets already listed."
if ($dry) { $files | Select-Object -First 12 | ForEach-Object { Write-Host ('  ' + $_.Directory.Name + '/' + $_.Name + '  ' + [math]::Round($_.Length / 1KB) + ' KB') }; exit 0 }

$key = ([Environment]::GetEnvironmentVariable('ROBLOX_OPEN_CLOUD_API_KEY', 'User')).Trim()
$uid = [Environment]::GetEnvironmentVariable('ROBLOX_CREATOR_USER_ID', 'User')
if (-not $key -or -not $uid) { Write-Host 'Key or user ID not set.' -ForegroundColor Red; exit 1 }
$client = New-Object System.Net.Http.HttpClient
$client.Timeout = [TimeSpan]::FromMinutes(5)
$client.DefaultRequestHeaders.Add('x-api-key', $key)
$n = 0; $ok = 0; $bad = 0
foreach ($file in $files) {
  $n++
  $name = $file.BaseName
  Write-Host "[$n/$($files.Count)] $name ... " -NoNewline
  $req = @{ assetType = 'Model'; displayName = $name.Substring(0, [Math]::Min(50, $name.Length)); description = 'Phase 1 map model (v5)'; creationContext = @{ creator = @{ userId = "$uid" } } } | ConvertTo-Json -Depth 5 -Compress
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
