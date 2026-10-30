param([int]$x, [int]$y)
# Clicks at (x,y) in Studio window pixel coordinates (as in capture.ps1 output).
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32c {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  public struct RECT { public int L; public int T; public int R; public int B; }
}
"@
[W32c]::SetProcessDPIAware() | Out-Null
$p = Get-Process | Where-Object { $_.ProcessName -like 'RobloxStudio*' -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = $p.MainWindowHandle
[W32c]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 400
$r = New-Object W32c+RECT
[W32c]::GetWindowRect($h, [ref]$r) | Out-Null
[W32c]::SetCursorPos($r.L + $x, $r.T + $y) | Out-Null
Start-Sleep -Milliseconds 150
[W32c]::mouse_event(2, 0, 0, 0, [IntPtr]::Zero)
[W32c]::mouse_event(4, 0, 0, 0, [IntPtr]::Zero)
Write-Output "clicked $x,$y"
