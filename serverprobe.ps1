$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = 'C:\Program Files\nodejs\node.exe'
$psi.Arguments = '"C:\Users\Nitro\AppData\Local\npm-cache\_npx\2dca8ffe7201fd5b\node_modules\robloxstudio-mcp\dist\index.js"'
$psi.UseShellExecute = $false
$psi.EnvironmentVariables['ROBLOX_STUDIO_HOST'] = '127.0.0.1'
$psi.RedirectStandardInput = $true
$psi.RedirectStandardError = $true
$psi.RedirectStandardOutput = $true
$p = [System.Diagnostics.Process]::Start($psi)
$errTask = $p.StandardError.ReadToEndAsync()
Start-Sleep -Seconds 8
if ($p.HasExited) { "EXITED code=$($p.ExitCode)" } else { 'still running after 8s'; $p.Kill() }
Start-Sleep -Milliseconds 500
'--- stderr ---'
$errTask.Result
