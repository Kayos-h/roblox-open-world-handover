$all = Get-CimInstance Win32_Process
$all | Where-Object { $_.CommandLine -match '(?i)taskkill|stop-process|kill|terminate|memory|ram|clean|watchdog|guard' -and $_.Name -notmatch '^(svchost|RuntimeBroker)\.exe$' } |
  ForEach-Object { "{0} pid={1} started={2}`n   {3}" -f $_.Name, $_.ProcessId, $_.CreationDate, ($_.CommandLine.Substring(0, [Math]::Min(220, $_.CommandLine.Length))) }
'--- processes started in the last 3 hours (non-system) ---'
$cut = (Get-Date).AddHours(-3)
$all | Where-Object { $_.CreationDate -gt $cut -and $_.Name -notmatch '^(svchost|conhost|RuntimeBroker|backgroundTaskHost|dllhost|WmiPrvSE|SearchProtocolHost|SearchFilterHost|smartscreen|audiodg)\.exe$' } |
  Sort-Object CreationDate | ForEach-Object { "{0:HH:mm} {1} pid={2} parent={3}" -f $_.CreationDate, $_.Name, $_.ProcessId, $_.ParentProcessId } | Select-Object -Last 40
