# Backup of the whole Roblox map project to the Desktop folder roblox_backup (incremental, safe to re-run).
# Source: C:\Users\Nitro\.kiro\crew\workspace\town  (models, scripts, plans, photos, handoffs, asset ids)
param([string]$Dest = 'C:\Users\Nitro\Desktop\roblox_backup')
$src = 'C:\Users\Nitro\.kiro\crew\workspace\town'
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
$log = Join-Path $Dest '_backup_log.txt'
"backup start " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Out-File $log -Encoding utf8
robocopy $src (Join-Path $Dest 'town') /E /XO /XD '__pycache__' '.git' /R:1 /W:1 /MT:2 /NFL /NDL /NP /NJH /LOG+:$log | Out-Null
$extra = Join-Path $Dest 'desktop_launchers'
New-Item -ItemType Directory -Force -Path $extra | Out-Null
Get-ChildItem 'C:\Users\Nitro\Desktop' -Filter '*.bat' -File -ErrorAction SilentlyContinue | ForEach-Object { Copy-Item $_.FullName $extra -Force }
$ref = 'C:\Users\Nitro\.kiro\crew\uploads\943989c5b0354ac5b891320284412c60_pasted-image-20261029-081421324.png'
if (Test-Path $ref) { Copy-Item $ref (Join-Path $Dest 'REFERENCE_top_down_map.png') -Force }
$h = Join-Path $src 'HANDOFF_FINAL.md'
if (Test-Path $h) { Copy-Item $h (Join-Path $Dest 'HANDOFF_FINAL.md') -Force }
$files = Get-ChildItem $Dest -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum
"backup done " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + " files " + $files.Count + " GB " + [math]::Round($files.Sum / 1GB, 2) | Out-File $log -Append -Encoding utf8
Write-Output ("files " + $files.Count + " GB " + [math]::Round($files.Sum / 1GB, 2))
