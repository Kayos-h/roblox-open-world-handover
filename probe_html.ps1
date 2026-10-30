$t = Get-Content -Raw (Join-Path $PSScriptRoot 'shots\ref\bing.html')
$i = $t.IndexOf('murl')
if ($i -ge 0) { Write-Output $t.Substring([Math]::Max(0, $i - 40), 300) }
$j = $t.IndexOf('mm.bing.net')
if ($j -ge 0) { Write-Output '---'; Write-Output $t.Substring([Math]::Max(0, $j - 60), 300) }
