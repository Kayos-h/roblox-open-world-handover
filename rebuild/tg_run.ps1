param([int]$x0, [int]$x1, [int]$z0, [int]$z1, [string]$tag = 'run', [int]$pollSecs = 10, [int]$maxMinutes = 90)
$dir = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$world = [IO.File]::ReadAllText("$dir\world.json")
$opt = @{ x0 = $x0; x1 = $x1; z0 = $z0; z1 = $z1; tag = $tag } | ConvertTo-Json -Compress
$data = '{"world":' + $world + ',"opt":' + $opt + '}'
$code = [IO.File]::ReadAllText("$dir\terrain_gen.luau").Replace('__DATA__', $data)
$args = @{ code = $code } | ConvertTo-Json -Compress -Depth 3
[IO.File]::WriteAllText("$dir\_tg_start.json", $args)
$r = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile "$dir\_tg_start.json"
"start: $r"
[IO.File]::WriteAllText("$dir\_tg_poll.json", '{"code":"local g=_G.TG if not g then return \"none\" end return string.format(\"%s %d/%d done=%s secs=%.0f errs=%d %s\", tostring(g.tag), g.i, g.n, tostring(g.done), g.secs or (os.clock()-g.started), #g.errs, table.concat(g.errs, \" | \"):sub(1,600))"}')
$t0 = Get-Date
while ($true) {
  Start-Sleep -Seconds $pollSecs
  $p = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile "$dir\_tg_poll.json"
  "$(Get-Date -Format HH:mm:ss) $p"
  if ($p -match 'done=true') { break }
  if (((Get-Date) - $t0).TotalMinutes -gt $maxMinutes) { 'timeout'; break }
}
