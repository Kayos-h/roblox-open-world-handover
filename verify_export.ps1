$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$cut = (Get-Date).AddHours(-1)
$all = @(); $issues = @()
foreach ($r in Get-ChildItem "$lib\_export_v2\*.json") {
  $folder = $r.BaseName
  foreach ($m in (Get-Content $r.FullName -Raw | ConvertFrom-Json)) {
    $all += $m
    $tag = "$folder/$($m.id)"
    if ($m.error) { $issues += "$tag ERROR"; continue }
    $big = ($m.size | Measure-Object -Maximum).Maximum
    if ($big -gt 700 -or $big -lt 0.2) { $issues += "$tag odd size $($m.size -join 'x')" }
    if ([Math]::Abs($m.min_z) -gt 0.6) { $issues += "$tag base not at ground: min_z $($m.min_z)" }
    if ($m.names -contains 'default') { $issues += "$tag has unnamed material" }
    $fbx = Join-Path "$lib\$folder" ($m.id + '.fbx')
    if (-not (Test-Path $fbx)) { $issues += "$tag fbx missing" } elseif ((Get-Item $fbx).LastWriteTime -lt $cut) { $issues += "$tag fbx is old" }
  }
}
"models checked: $($all.Count)"
"total colour pieces: $(($all | Measure-Object pieces -Sum).Sum)"
"largest model: " + (($all | Sort-Object { ($_.size | Measure-Object -Maximum).Maximum } -Descending | Select-Object -First 3 | ForEach-Object { "$($_.id) $($_.size -join 'x')" }) -join '; ')
"issues: $($issues.Count)"
$issues
