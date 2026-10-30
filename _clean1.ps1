$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
Remove-Item -Recurse -Force (Join-Path $lib 'v4_test') -ErrorAction SilentlyContinue
foreach ($f in @('palette_zz.json', 'v4_meta_zz.json', 'v4_sheets\zz_selftest_1.png', 'v4_sheets\_t_ZZ_01_toy.png')) {
  Remove-Item -Force (Join-Path $lib $f) -ErrorAction SilentlyContinue
}
Get-ChildItem (Join-Path $lib 'v4_work') -Filter '*zz*' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Output 'cleaned test artifacts'
$os = Get-CimInstance Win32_OperatingSystem
Write-Output ('Free GB now: ' + [math]::Round($os.FreePhysicalMemory / 1MB, 2))
