# 창 제목으로 앞으로 가져와(최대화) 클릭/스크롤 후 화면 캡처
# 사용: win.ps1 -title "Higgsfield AI - Discord" [-x X -y Y] [-scroll N] [-hover] -out cap.png
param([string]$title,[int]$x=-1,[int]$y=-1,[int]$scroll=0,[switch]$hover,[switch]$max,[string]$out,[int]$wait=1500)
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
if (-not ("WW" -as [type])) {
Add-Type @"
using System; using System.Runtime.InteropServices;
public class WW {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
 [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
 [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, UIntPtr e);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, int d, UIntPtr e);
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
"@ }
[WW]::SetProcessDPIAware()|Out-Null
$p = Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -like "*$title*" } | Select-Object -First 1
if (-not $p) { "NO WINDOW: $title"; exit 1 }
$h=$p.MainWindowHandle
if ([WW]::IsIconic($h)) { [WW]::ShowWindow($h,9)|Out-Null }
[WW]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [WW]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
[WW]::SetForegroundWindow($h)|Out-Null; Start-Sleep -Milliseconds 500
if ($max) { [WW]::ShowWindow($h,3)|Out-Null; Start-Sleep -Milliseconds 800 }
if ($x -ge 0) {
  if ($hover) { [WW]::SetCursorPos($x+100,$y-100)|Out-Null; Start-Sleep -Milliseconds 500 }
  [WW]::SetCursorPos($x,$y)|Out-Null; Start-Sleep -Milliseconds 300
  if ($scroll -ne 0) { [WW]::mouse_event(0x0800,0,0,$scroll,[UIntPtr]::Zero) }
  else { [WW]::mouse_event(2,0,0,0,[UIntPtr]::Zero); Start-Sleep -Milliseconds 60; [WW]::mouse_event(4,0,0,0,[UIntPtr]::Zero) }
}
Start-Sleep -Milliseconds $wait
if ($out) { $b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bmp=New-Object System.Drawing.Bitmap $b.Width,$b.Height; $g=[System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($b.Location,[System.Drawing.Point]::Empty,$b.Size); $bmp.Save($out); $g.Dispose(); $bmp.Dispose() }
"ok: $($p.MainWindowTitle)"
