param([string]$py, [int]$timeoutSec = 600)
$code = [IO.File]::ReadAllText($py)
$payload = @{ type = 'execute_code'; params = @{ code = $code } } | ConvertTo-Json -Compress -Depth 4
$c = New-Object System.Net.Sockets.TcpClient
try {
  $c.Connect('127.0.0.1', 9876)
  $s = $c.GetStream(); $s.ReadTimeout = $timeoutSec * 1000
  $b = [Text.Encoding]::UTF8.GetBytes($payload); $s.Write($b, 0, $b.Length)
  $ms = New-Object IO.MemoryStream; $buf = New-Object byte[] 65536
  while ($true) {
    $n = $s.Read($buf, 0, $buf.Length)
    if ($n -le 0) { break }
    $ms.Write($buf, 0, $n)
    $txt = [Text.Encoding]::UTF8.GetString($ms.ToArray())
    try { $j = $txt | ConvertFrom-Json; break } catch { }
  }
  if ($j) { if ($j.status -eq 'success') { $j.result.result } else { 'BLENDER ERROR: ' + $j.message } } else { $txt }
} catch { 'error: ' + $_.Exception.Message } finally { $c.Close() }
