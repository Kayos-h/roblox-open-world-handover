$repo = 'Kayos-h/roblox-map-models-gallery'
$raw = & gh repo view $repo --json url,visibility,defaultBranchRef
Write-Output $raw
$o = $raw | ConvertFrom-Json
if ($o.defaultBranchRef.name -ne 'gallery') {
  Write-Output ('default branch is ' + $o.defaultBranchRef.name + ', switching to gallery')
  & gh repo edit $repo --default-branch gallery
  & gh repo view $repo --json defaultBranchRef
}
Write-Output '--- files on the gallery branch (top level) ---'
& gh api ('repos/' + $repo + '/contents?ref=gallery') --jq '.[].name'
