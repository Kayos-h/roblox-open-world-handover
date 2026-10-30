$lib = 'C:\Users\Nitro\.kiro\crew\workspace\town\library'
Write-Output ("now " + (Get-Date).ToString('HH:mm:ss'))
foreach ($w in @('wd','we','wf','wg','wh','wk')) {
  $log = Get-ChildItem (Join-Path $lib 'v4_work') -Filter ("run_" + $w + "_*.log") -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  $prog = Get-Item (Join-Path $lib ("v4_work\progress_" + $w + ".md")) -ErrorAction SilentlyContinue
  $mod = Get-ChildItem (Join-Path $lib 'src') -Filter ("v4_" + $w + "_*.py") -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  $meta = Get-Item (Join-Path $lib ("v4_meta_" + $w + ".json")) -ErrorAction SilentlyContinue
  $l = '-'; if ($log) { $l = $log.LastWriteTime.ToString('HH:mm:ss') + ' ' + $log.Name }
  $p = '-'; if ($prog) { $p = $prog.LastWriteTime.ToString('HH:mm:ss') }
  $m = '-'; if ($mod) { $m = $mod.LastWriteTime.ToString('HH:mm:ss') + ' ' + $mod.Name }
  $t = '-'; if ($meta) { $t = $meta.LastWriteTime.ToString('HH:mm:ss') }
  Write-Output ($w + ":  last run log " + $l + "   | progress " + $p + "   | newest module " + $m + "   | meta " + $t)
}
Write-Output '--- tail of the last log of wd and wh ---'
foreach ($w in @('wd','wh')) {
  $log = Get-ChildItem (Join-Path $lib 'v4_work') -Filter ("run_" + $w + "_*.log") -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($log) { Write-Output ("== " + $log.Name); Get-Content $log.FullName -Tail 6 }
}
