param([string]$q = 'black clover black bulls hideout', [int]$n = 6, [string]$name = 'ref')
# fetch Bing image results, download the first N full images into shots\ref\
$dir = Join-Path $PSScriptRoot 'shots\ref'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$h = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
$u = 'https://www.bing.com/images/search?q=' + [uri]::EscapeDataString($q)
$r = Invoke-WebRequest -UseBasicParsing -Headers $h $u
$ms = [regex]::Matches($r.Content, 'murl&quot;:&quot;(.*?)&quot;')
if ($ms.Count -eq 0) { $ms = [regex]::Matches($r.Content, '"murl":"(.*?)"') }
if ($ms.Count -eq 0) { $ms = [regex]::Matches($r.Content, 'mediaurl=(http[^&"]+)') ; $dec = $true }
if ($ms.Count -eq 0) { $ms = [regex]::Matches($r.Content, '(https://[^"''\s]+?\.(?:jpg|jpeg|png))') }
if ($ms.Count -eq 0) { $ms = [regex]::Matches($r.Content, '(https://tse\d\.mm\.bing\.net/th[^"''\s&]*(?:&amp;[^"''\s]*)?)') ; $amp = $true }
Write-Output ('len=' + $r.Content.Length + ' hits=' + $ms.Count)
$i = 0
foreach ($m in $ms) {
  if ($i -ge $n) { break }
  $url = $m.Groups[1].Value
  if ($dec) { $url = [uri]::UnescapeDataString($url) }
  if ($amp) { $url = $url -replace '&amp;', '&' }
  $ext = [IO.Path]::GetExtension(($url -split '\?')[0]); if ($ext -notmatch '^\.(jpg|jpeg|png|webp)$') { $ext = '.jpg' }
  $out = Join-Path $dir ($name + '_' + $i + $ext)
  try { Invoke-WebRequest -UseBasicParsing -Headers $h -TimeoutSec 15 $url -OutFile $out; Write-Output ($out + ' <- ' + $url); $i++ } catch { }
}
