$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = 'node'
$psi.Arguments = '-e "require(''http'').createServer((q,r)=>r.end(''ok'')).listen(58999,''127.0.0.1'');setInterval(()=>{},1000)"'
$psi.UseShellExecute = $false
$p1 = [System.Diagnostics.Process]::Start($psi)
$psi2 = New-Object System.Diagnostics.ProcessStartInfo
$psi2.FileName = 'node'
$psi2.Arguments = '-e "setInterval(()=>{},1000)"'
$psi2.UseShellExecute = $false
$p2 = [System.Diagnostics.Process]::Start($psi2)
Start-Sleep -Seconds 8
foreach ($x in @(@('listener', $p1), @('idle', $p2))) {
  if ($x[1].HasExited) { "$($x[0]): EXITED code=$($x[1].ExitCode)" } else { "$($x[0]): alive after 8s"; $x[1].Kill() }
}
