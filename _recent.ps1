$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$since = (Get-Date).AddMinutes(-150)
Write-Output ("now: " + (Get-Date).ToString('HH:mm:ss'))
Write-Output '--- worker meta files (mtime) ---'
Get-ChildItem -Path $lib -Filter 'v4_meta_*.json' | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Name }
Write-Output '--- model fbx written since -150 min (time, folder, name) ---'
Get-ChildItem -Path $lib -Recurse -Filter '*.fbx' -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $since -and $_.DirectoryName -like '*\v4_*' } | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}  {2}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Directory.Name, $_.BaseName }
Write-Output '--- new src modules since -150 min ---'
Get-ChildItem -Path (Join-Path $lib 'src') -Filter 'v4_*.py' | Where-Object { $_.LastWriteTime -gt $since } | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Name }
Write-Output '--- progress files ---'
Get-ChildItem -Path (Join-Path $lib 'v4_work') -Filter 'progress_*.md' | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Name }
