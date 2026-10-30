# Publish / refresh the private GitHub photo gallery. Safe to re-run. Photos only (no model files).
$repo = 'Kayos-h/roblox-map-models-gallery'
$g = 'C:\Users\Nitro\.kiro\crew\workspace\town\gallery_repo'
$py = 'C:\Users\Nitro\.kiro\crew\workspace\town\library\src\gallery.py'

Write-Output '== 1. rebuild gallery files'
& python $py
if ($LASTEXITCODE -ne 0) { Write-Output 'gallery.py failed'; exit 1 }

Write-Output '== 2. repo exists?'
$null = & gh repo view $repo --json url 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Output 'creating PRIVATE repo'
  & gh repo create $repo --private --description 'Photo gallery of the Blender models for the Roblox map (V4). Photos only, no model files.'
  if ($LASTEXITCODE -ne 0) { Write-Output 'repo create failed'; exit 2 }
} else { Write-Output 'repo already exists' }

Write-Output '== 3. local git repo'
$login = (& gh api user --jq '.login').Trim()
$uid = (& gh api user --jq '.id').Trim()
if (-not (Test-Path (Join-Path $g '.git'))) { & git -C $g init -b gallery | Out-Null }
& git -C $g config user.name $login
& git -C $g config user.email ($uid + '+' + $login + '@users.noreply.github.com')
$remotes = & git -C $g remote
if ($remotes -notcontains 'origin') { & git -C $g remote add origin ('https://github.com/' + $repo + '.git') }
& git -C $g add -A
$readme = Get-Content (Join-Path $g 'README.md') -TotalCount 4 | Out-String
$m = [regex]::Match($readme, '\*\*(\d+) of (\d+) models built')
$label = 'Gallery update'
if ($m.Success) { $label = 'Gallery: ' + $m.Groups[1].Value + ' of ' + $m.Groups[2].Value + ' models built' }
& git -C $g commit -m $label 2>&1 | Select-Object -Last 2

Write-Output '== 4. push branch gallery'
& git -C $g -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u origin gallery 2>&1 | Select-Object -Last 4

Write-Output '== 5. result'
$o = (& gh repo view $repo --json url,visibility,defaultBranchRef) | ConvertFrom-Json
Write-Output ($o.url + '  visibility=' + $o.visibility + '  default branch=' + $o.defaultBranchRef.name)
