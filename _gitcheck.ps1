$gh = Get-Command gh -ErrorAction SilentlyContinue
if ($gh) { Write-Output ("gh: " + $gh.Source); try { & gh auth status 2>&1 | Out-String } catch { Write-Output ("gh auth error: " + $_) } } else { Write-Output "gh CLI: not installed" }
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
  Write-Output ("git: " + (& git --version))
  Write-Output "--- global git config (name/email/credential only) ---"
  & git config --global --list 2>$null | Where-Object { $_ -match '^(user\.name|user\.email|credential\.helper|credential\..*)=' }
} else { Write-Output "git: not installed" }
Write-Output "--- is town folder a git repo? ---"
Push-Location 'C:\Users\Nitro\.kiro\crew\workspace\town'
& git rev-parse --show-toplevel 2>&1 | Out-String
Pop-Location
Write-Output "--- is workspace a git repo? ---"
Push-Location 'C:\Users\Nitro\.kiro\crew\workspace'
& git rev-parse --show-toplevel 2>&1 | Out-String
& git remote -v 2>&1 | Out-String
Pop-Location
Write-Output "--- BUILD//IT repo remote (read only) ---"
Push-Location 'C:\Users\Nitro\Desktop\build it\build_it-main'
& git remote -v 2>&1 | Out-String
Pop-Location
Write-Output "--- GH token env present? (names only) ---"
Get-ChildItem Env: | Where-Object { $_.Name -match '^(GH_TOKEN|GITHUB_TOKEN)$' } | ForEach-Object { $_.Name + " is set" }
