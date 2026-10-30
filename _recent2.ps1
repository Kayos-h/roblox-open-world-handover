param([int]$Minutes = 8)
$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$since = (Get-Date).AddMinutes(-$Minutes)
Write-Output ("now: " + (Get-Date).ToString('HH:mm:ss') + "  window: last $Minutes min")
Write-Output '--- worker meta files changed ---'
Get-ChildItem -Path $lib -Filter 'v4_meta_*.json' | Where-Object { $_.LastWriteTime -gt $since } | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Name }
Write-Output '--- model fbx written ---'
Get-ChildItem -Path $lib -Recurse -Filter '*.fbx' -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $since -and $_.DirectoryName -like '*\v4_*' -and $_.DirectoryName -notlike '*backup_pre_fix*' } | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}  {2}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Directory.Name, $_.BaseName }
Write-Output '--- source modules and progress files changed ---'
Get-ChildItem -Path (Join-Path $lib 'src') -Filter 'v4_*.py' | Where-Object { $_.LastWriteTime -gt $since } | Sort-Object LastWriteTime | ForEach-Object { '{0}  src\{1}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Name }
Get-ChildItem -Path (Join-Path $lib 'v4_work') -Filter 'progress_*.md' | Where-Object { $_.LastWriteTime -gt $since } | Sort-Object LastWriteTime | ForEach-Object { '{0}  {1}' -f $_.LastWriteTime.ToString('HH:mm:ss'), $_.Name }
