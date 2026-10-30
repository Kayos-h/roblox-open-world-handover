$c = New-Object System.Net.Sockets.TcpClient
try {
  $t = $c.ConnectAsync('127.0.0.1', 9876)
  if (-not $t.Wait(3000)) { 'port 9876: connect timed out'; exit }
  $s = $c.GetStream(); $s.ReadTimeout = 8000
  $msg = [Text.Encoding]::UTF8.GetBytes('{"type":"execute_code","params":{"code":"import bpy; print(bpy.app.version_string, len(bpy.data.objects))"}}')
  $s.Write($msg, 0, $msg.Length)
  $buf = New-Object byte[] 8192
  $n = $s.Read($buf, 0, $buf.Length)
  'reply: ' + [Text.Encoding]::UTF8.GetString($buf, 0, $n)
} catch { 'error: ' + $_.Exception.InnerException.Message + ' ' + $_.Exception.Message } finally { $c.Close() }
