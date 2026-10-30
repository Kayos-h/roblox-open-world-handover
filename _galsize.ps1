$g = 'C:\Users\Nitro\.kiro\crew\workspace\town\gallery_repo'
$files = Get-ChildItem $g -Recurse -File
$mb = [math]::Round(($files | Measure-Object Length -Sum).Sum / 1MB, 1)
Write-Output ("files: " + $files.Count + "   total MB: " + $mb)
Get-ChildItem (Join-Path $g 'images') -Directory | ForEach-Object { $s = (Get-ChildItem $_.FullName -File | Measure-Object Length -Sum); Write-Output ($_.Name + ": " + $s.Count + " files, " + [math]::Round($s.Sum / 1MB, 1) + " MB") }
Write-Output '--- README.md ---'
Get-Content (Join-Path $g 'README.md') -Raw
Write-Output '--- sections ---'
Get-ChildItem (Join-Path $g 'sections') | ForEach-Object { $_.Name }
