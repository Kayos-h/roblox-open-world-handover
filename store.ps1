param([string]$q, [int]$n = 12, [string]$name = 'sheet', [switch]$all)
# Public toolbox search (verified creators by default) -> prints id | name | creator, and saves a labeled
# thumbnail contact sheet to shots\store\<name>.png
Add-Type -AssemblyName System.Drawing
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$dir = Join-Path $here 'shots\store'; New-Item -ItemType Directory -Force -Path $dir | Out-Null
$ver = if ($all) { 'false' } else { 'true' }
$url = 'https://apis.roblox.com/toolbox-service/v1/marketplace/10?keyword=' + [uri]::EscapeDataString($q) + '&limit=' + $n + '&includeOnlyVerifiedCreators=' + $ver
$s = (Invoke-WebRequest -UseBasicParsing -TimeoutSec 30 -Uri $url).Content | ConvertFrom-Json
$ids = @($s.data | ForEach-Object { $_.id })
if ($ids.Count -eq 0) { Write-Output 'no results'; exit }
$det = (Invoke-WebRequest -UseBasicParsing -TimeoutSec 30 -Uri ('https://apis.roblox.com/toolbox-service/v1/items/details?assetIds=' + ($ids -join ','))).Content | ConvertFrom-Json
# keep only free assets (paid ones cannot be loaded)
$free = @($det.data | Where-Object { (-not $_.fiatProduct) -or $_.fiatProduct.isFree } | ForEach-Object { $_.asset.id })
$ids = @($free | Select-Object -First 18)
if ($ids.Count -eq 0) { Write-Output 'no free results'; exit }
$idList = ($ids -join ',')
$th = (Invoke-WebRequest -UseBasicParsing -TimeoutSec 30 -Uri ('https://thumbnails.roblox.com/v1/assets?assetIds=' + $idList + '&size=150x150&format=Png')).Content | ConvertFrom-Json
$thumb = @{}; foreach ($t in $th.data) { $thumb[[string]$t.targetId] = $t.imageUrl }
$cols = 6; $cell = 150; $rows = [Math]::Ceiling($ids.Count / $cols)
$bmp = New-Object System.Drawing.Bitmap ($cols*$cell), ($rows*($cell+16))
$g = [System.Drawing.Graphics]::FromImage($bmp); $g.Clear([System.Drawing.Color]::FromArgb(40,40,40))
$font = New-Object System.Drawing.Font 'Arial', 9
$i = 0
foreach ($id in $ids) {
    $d = $det.data | Where-Object { $_.asset.id -eq $id } | Select-Object -First 1
    $nm = if ($d) { $d.asset.name } else { '?' }
    $cr = if ($d) { $d.creator.name } else { '?' }
    $tri = if ($d) { $d.asset.modelTechnicalDetails.objectMeshSummary.triangles } else { '?' }
    $sc = if ($d) { $d.asset.hasScripts } else { '?' }
    Write-Output ("[$i] $id | $nm | $cr | tris=$tri scripts=$sc")
    $x = ($i % $cols) * $cell; $y = [Math]::Floor($i / $cols) * ($cell + 16)
    $u = $thumb[[string]$id]
    if ($u) {
        try {
            $bytes = (New-Object System.Net.WebClient).DownloadData($u)
            $ms = New-Object System.IO.MemoryStream(,$bytes)
            $img = [System.Drawing.Image]::FromStream($ms)
            $g.DrawImage($img, $x, $y, $cell, $cell)
        } catch {}
    }
    $g.DrawString("[$i]", $font, [System.Drawing.Brushes]::Yellow, $x + 2, $y + $cell + 1)
    $i++
}
$out = Join-Path $dir ($name + '.png'); $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output "sheet $out"
