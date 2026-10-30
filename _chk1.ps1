$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
Get-ChildItem $lib -File | Where-Object { $_.Name -match '^(v4_meta|palette)' } | ForEach-Object { Write-Output ($_.Name + "  " + $_.Length + "  " + $_.LastWriteTime.ToString('HH:mm:ss')) }
Write-Output '--- v4_test folder ---'
Get-ChildItem (Join-Path $lib 'v4_test') -ErrorAction SilentlyContinue | ForEach-Object { Write-Output ($_.Name + "  " + $_.Length) }
Write-Output '--- sheet ---'
Get-ChildItem (Join-Path $lib 'v4_sheets') | Where-Object { $_.Name -like 'zz_*' -or $_.Name -like '_t_ZZ*' } | ForEach-Object { Write-Output ($_.Name + "  " + $_.Length) }
Write-Output '--- palette_zz.json ---'
Get-Content (Join-Path $lib 'palette_zz.json') -ErrorAction SilentlyContinue
Write-Output '--- main palette untouched? ---'
(Get-Item (Join-Path $lib 'palette.json')).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')
