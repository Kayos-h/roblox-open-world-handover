param([string]$areas)
$tpl = [IO.File]::ReadAllText('C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\build\fixpass.luau')
foreach ($a in ($areas -split ',')) {
  $code = $tpl.Replace('__DATA__', (@{ area = $a } | ConvertTo-Json -Compress))
  $f = "C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\_fix_$a.json"
  [IO.File]::WriteAllText($f, (@{ code = $code } | ConvertTo-Json -Compress))
  powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\Nitro\.kiro\crew\workspace\town\studio.ps1' -argsFile $f
}
