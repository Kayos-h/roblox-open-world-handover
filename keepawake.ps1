# Keeps Windows from going to sleep for 10 hours (system stays awake; the screen may still turn off). Changes no settings; ends by itself.
Add-Type -Namespace Win32 -Name Power2 -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
[Win32.Power2]::SetThreadExecutionState([uint32]2147483649) | Out-Null   # ES_CONTINUOUS + ES_SYSTEM_REQUIRED
$stop = (Get-Date).AddHours(10)
while ((Get-Date) -lt $stop) {
  Start-Sleep -Seconds 60
  [Win32.Power2]::SetThreadExecutionState([uint32]2147483649) | Out-Null
}
[Win32.Power2]::SetThreadExecutionState([uint32]2147483648) | Out-Null   # ES_CONTINUOUS only = release
