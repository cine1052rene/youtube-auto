param([int]$x = -1, [int]$y = -1, [string]$out, [int]$scroll = 0, [int]$wait = 1500, [string]$key = "")
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
if (-not ("DC" -as [type])) {
Add-Type @"
using System; using System.Runtime.InteropServices;
public class DC {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, int d, UIntPtr e);
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@ }
[DC]::SetProcessDPIAware() | Out-Null
$p = Get-Process -Name Discord | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
[DC]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 400
if ($x -ge 0) {
  [DC]::SetCursorPos($x, $y) | Out-Null; Start-Sleep -Milliseconds 150
  if ($scroll -ne 0) { [DC]::mouse_event(0x0800, 0, 0, $scroll, [UIntPtr]::Zero) }
  else { [DC]::mouse_event(0x0002,0,0,0,[UIntPtr]::Zero); Start-Sleep -Milliseconds 60; [DC]::mouse_event(0x0004,0,0,0,[UIntPtr]::Zero) }
}
if ($key) { [System.Windows.Forms.SendKeys]::SendWait($key) }
Start-Sleep -Milliseconds $wait
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose()
"saved $out ($($b.Width)x$($b.Height))"
