$repo = 'Kayos-h/roblox-map-models-gallery'
$n = (& gh api ('repos/' + $repo + '/contents/images/thumbs?ref=gallery') --jq 'length')
Write-Output ("thumbs on branch: " + $n)
$n2 = (& gh api ('repos/' + $repo + '/contents/images/sheets?ref=gallery') --jq 'length')
Write-Output ("sheets on branch: " + $n2)
$n3 = (& gh api ('repos/' + $repo + '/contents/sections?ref=gallery') --jq 'length')
Write-Output ("section pages on branch: " + $n3)
# take the first image path from the B page and check that exact file exists in the repo
$b = & gh api ('repos/' + $repo + '/contents/sections/B_key_set_pieces.md?ref=gallery') -H 'Accept: application/vnd.github.raw'
$m = [regex]::Match(($b | Out-String), 'src="\.\./(images/thumbs/[^"]+)"')
if ($m.Success) {
  $p = $m.Groups[1].Value
  $null = & gh api ('repos/' + $repo + '/contents/' + $p + '?ref=gallery') --jq '.size' 2>&1
  if ($LASTEXITCODE -eq 0) { Write-Output ("first image link in B page resolves: " + $p) } else { Write-Output ("BROKEN link: " + $p) }
} else { Write-Output 'no img tag found in B page' }
