$os = Get-CimInstance Win32_OperatingSystem
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
Write-Output ("Total RAM GB: " + $totalGB + "  Free GB: " + $freeGB)
Get-Process | Group-Object ProcessName | ForEach-Object {
  $sum = ($_.Group | Measure-Object WorkingSet64 -Sum).Sum
  [pscustomobject]@{ Name = $_.Name; Count = $_.Count; MB = [math]::Round($sum / 1MB) }
} | Sort-Object MB -Descending | Select-Object -First 14 | Format-Table -AutoSize | Out-String -Width 120
