param([string]$views = "$PSScriptRoot\tour_views.csv", [string]$dir = "$PSScriptRoot\shots\tour")
Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$rows = Import-Csv $views
foreach ($v in $rows) {
  $code = "local c=workspace.CurrentCamera c.CameraType=Enum.CameraType.Scriptable c.FieldOfView=70 c.CFrame=CFrame.lookAt(Vector3.new($($v.pos)),Vector3.new($($v.look))) return 'ok'"
  $json = @{ code = $code } | ConvertTo-Json -Compress
  $af = Join-Path $dir '_cam.json'
  Set-Content -Path $af -Value $json -Encoding UTF8
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot\mcp_call.ps1" -tool execute_luau -argsFile $af
  Start-Sleep -Seconds 3
  $raw = Join-Path $dir "_raw.png"
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$PSScriptRoot\capture.ps1" -out $raw | Out-Null
  # crop to the viewport (approx) and shrink
  $src = [System.Drawing.Image]::FromFile($raw)
  $crop = New-Object System.Drawing.Rectangle 10, 175, 1530, 960
  $w = 960; $h = 602
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = 'HighQualityBicubic'
  $g.DrawImage($src, (New-Object System.Drawing.Rectangle 0,0,$w,$h), $crop, [System.Drawing.GraphicsUnit]::Pixel)
  $out = Join-Path $dir "$($v.name).jpg"
  $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $g.Dispose(); $bmp.Dispose(); $src.Dispose()
  "$($v.name): $r -> $out"
}
