$c = Get-Content 'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json' -Raw | ConvertFrom-Json
$list = if ($c.models) { $c.models } else { $c }
$list | Group-Object folder | ForEach-Object {
  "## $($_.Name) ($($_.Count))"
  ($_.Group | ForEach-Object { '{0} {1}x{2}x{3}' -f $_.id, [math]::Round($_.size_x), [math]::Round($_.height), [math]::Round($_.size_z) }) -join ' | '
}
