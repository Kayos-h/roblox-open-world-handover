$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
$out = @()
foreach ($r in Get-ChildItem "$lib\_export_v2\*.json") {
  foreach ($m in (Get-Content $r.FullName -Raw | ConvertFrom-Json)) {
    # Blender (x, y, z) -> Roblox (X = x, Y = z, Z = y): size_x, size_y(height), size_z(depth)
    $out += [ordered]@{ id = $m.id; folder = $r.BaseName; size_x = $m.size[0]; height = $m.size[2]; size_z = $m.size[1]; pieces = $m.names }
  }
}
$out | ConvertTo-Json -Depth 4 | Out-File "C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json" -Encoding utf8
"catalog entries: $($out.Count)"
