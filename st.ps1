param([string]$file = '', [string]$data = '', [string]$json = '')
# one entry point for Studio calls. -file x.luau [-data x.json]  or  -json call.json (a prepared {"code":...} file)
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
if ($json) { & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\studio.ps1" -argsFile $json; exit }
if ($data) { & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\rebuild\runluau.ps1" -file $file -data $data } else { & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\rebuild\runluau.ps1" -file $file }
