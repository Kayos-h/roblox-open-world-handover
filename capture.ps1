param([string]$out = "$PSScriptRoot\shots\shot.png")
# Captures ONLY the Roblox Studio window via PrintWindow (no focus change, no other screen content).
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32b {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  public struct RECT { public int L; public int T; public int R; public int B; }
}
"@
[W32b]::SetProcessDPIAware() | Out-Null
$p = Get-Process | Where-Object { $_.ProcessName -like 'RobloxStudio*' -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $p) { Write-Output 'Studio window not found'; exit 1 }
$h = $p.MainWindowHandle
if ([W32b]::IsIconic($h)) { [W32b]::ShowWindow($h, 4) | Out-Null; Start-Sleep -Milliseconds 800 }
$r = New-Object W32b+RECT
[W32b]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R - $r.L; $hh = $r.B - $r.T
$bmp = New-Object System.Drawing.Bitmap $w, $hh
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
[W32b]::PrintWindow($h, $hdc, 2) | Out-Null
$g.ReleaseHdc($hdc)
New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output "saved $out ($w x $hh)"
