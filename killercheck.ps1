$all = Get-CimInstance Win32_Process
$hits = $all | Where-Object { $_.CommandLine -match 'memory freeer|memory_freeer|ramopt|optimi|freeer|cleaner' -or $_.Name -match 'optimi|clean|freeer' }
if ($hits) { $hits | ForEach-Object { "{0} pid={1} started={2}`n   {3}" -f $_.Name, $_.ProcessId, $_.CreationDate, $_.CommandLine } } else { 'no optimizer-like process found' }
'--- recent node processes ---'
$all | Where-Object { $_.Name -eq 'node.exe' } | ForEach-Object { "node pid={0} parent={1} {2}" -f $_.ProcessId, $_.ParentProcessId, $_.CommandLine }
