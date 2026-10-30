param([int]$x0, [int]$x1, [int]$z0, [int]$z1, [string]$tag = 'clip', [int]$pollSecs = 10, [int]$maxMinutes = 20)
$dir = 'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
$world = [IO.File]::ReadAllText("$dir\world.json")
$opt = @{ x0 = $x0; x1 = $x1; z0 = $z0; z1 = $z1; tag = $tag } | ConvertTo-Json -Compress
$data = '{"world":' + $world + ',"opt":' + $opt + '}'
$code = [IO.File]::ReadAllText("$dir\terrain_clip.luau").Replace('__DATA__', $data)
$args = @{ code = $code } | ConvertTo-Json -Compress -Depth 3
[IO.File]::WriteAllText("$dir\_clip_start.json", $args)
$r = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile "$dir\_clip_start.json"
"start: $r"
$poll = 'local g=_G.CLIP if not g then return "none" end return string.format("%s %d/%d done=%s secs=%.0f clearedVox=%d cols=%d chunksWritten=%d maxcut=%d errs=%d %s", tostring(g.tag), g.i, g.n or 0, tostring(g.done), g.secs or (os.clock()-g.started), g.cleared, g.cols, g.chunks, g.maxcut, #g.errs, table.concat(g.errs, " | "):sub(1,500))'
[IO.File]::WriteAllText("$dir\_clip_poll.json", (@{ code = $poll } | ConvertTo-Json -Compress))
$t0 = Get-Date
while ($true) {
  Start-Sleep -Seconds $pollSecs
  $p = & powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile "$dir\_clip_poll.json"
  "$(Get-Date -Format HH:mm:ss) $p"
  if ($p -match 'done=true') { break }
  if (((Get-Date) - $t0).TotalMinutes -gt $maxMinutes) { 'timeout'; break }
}
