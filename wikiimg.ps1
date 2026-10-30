param([string]$q = 'Black Bulls', [int]$n = 8)
# search the Black Clover fandom wiki image list via its public MediaWiki API, download matching images
$dir = Join-Path $PSScriptRoot 'shots\ref'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
$api = 'https://blackclover.fandom.com/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=' + $n + '&prop=imageinfo&iiprop=url&iiurlwidth=800&gsrsearch=' + [uri]::EscapeDataString($q)
try { $r = Invoke-RestMethod -UserAgent $ua $api } catch { Write-Output ('api fail ' + $_.Exception.Message); exit }
$i = 0
foreach ($p in $r.query.pages.PSObject.Properties.Value) {
  $u = $p.imageinfo[0].thumburl; if (-not $u) { $u = $p.imageinfo[0].url }
  $out = Join-Path $dir ('wiki_' + $i + '.png')
  try { Invoke-WebRequest -UseBasicParsing -UserAgent $ua -TimeoutSec 20 $u -OutFile $out; Write-Output ($out + ' | ' + $p.title); $i++ } catch { Write-Output ('dl fail ' + $p.title) }
}
