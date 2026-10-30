$s = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_sheets'
Get-ChildItem $s -File | Where-Object { $_.Name -like '*zz*' -or $_.Name -like 'ZZ_*' -or $_.Name -like '_q_zz_*' } | ForEach-Object { Write-Output ('removing ' + $_.Name); Remove-Item -Force $_.FullName }
Get-ChildItem 'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_work' -File | Where-Object { $_.Name -like '*zz*' } | Remove-Item -Force
Write-Output 'done'
