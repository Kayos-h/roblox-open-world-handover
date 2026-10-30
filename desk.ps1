param([string]$name = 'desk')
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$out = Join-Path $here ('shots\' + $name + '.png')
$small = New-Object System.Drawing.Bitmap $bmp, ([int]($b.Width/2)), ([int]($b.Height/2))
$small.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output "saved $out ($($b.Width)x$($b.Height), half-size)"
