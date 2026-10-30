$os = Get-CimInstance Win32_OperatingSystem
$ramTot = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$ramFree = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$vTot = [math]::Round($os.TotalVirtualMemorySize / 1MB, 1)
$vFree = [math]::Round($os.FreeVirtualMemory / 1MB, 2)
Write-Output ("RAM total " + $ramTot + " GB, free " + $ramFree + " GB")
Write-Output ("Virtual memory (RAM + pagefile = the commit limit) total " + $vTot + " GB, still available " + $vFree + " GB, used " + [math]::Round($vTot - $vFree, 1) + " GB")
$pf = Get-CimInstance Win32_PageFileUsage
foreach ($p in $pf) { Write-Output ("pagefile " + $p.Name + " size " + $p.AllocatedBaseSize + " MB, in use " + $p.CurrentUsage + " MB, peak " + $p.PeakUsage + " MB") }
Write-Output '--- processes by count (helper programs of worker sessions) ---'
Get-Process | Group-Object ProcessName | Where-Object { $_.Count -ge 5 } | Sort-Object Count -Descending | Select-Object -First 8 | ForEach-Object { Write-Output ($_.Name + ": " + $_.Count + " processes, " + [math]::Round(($_.Group | Measure-Object WorkingSet64 -Sum).Sum / 1MB) + " MB") }
