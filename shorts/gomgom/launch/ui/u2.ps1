# 전체 화면(1920x1080) 기준 조작 헬퍼. 매 동작 후 전체 캡처를 full.png로 저장
# 사용: u2.ps1 -act shot|click|dbl|key|paste|scroll|front -x -y -text -keys -wait
param([string]$act="shot",[int]$x=0,[int]$y=0,[string]$text="",[string]$keys="",[int]$wait=2,[int]$procid=0)
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
Add-Type @"
using System;using System.Runtime.InteropServices;
public class U2{[DllImport("user32.dll")]public static extern bool SetCursorPos(int x,int y);[DllImport("user32.dll")]public static extern void mouse_event(int f,int x,int y,int d,int e);
[DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);[DllImport("user32.dll")]public static extern bool ShowWindow(IntPtr h,int c);}
"@
function C($x,$y){[U2]::SetCursorPos($x,$y);[U2]::mouse_event(2,0,0,0,0);[U2]::mouse_event(4,0,0,0,0)}
switch($act){
 "click"{C $x $y}
 "dbl"{C $x $y;Start-Sleep -Milliseconds 120;C $x $y}
 "key"{[System.Windows.Forms.SendKeys]::SendWait($keys)}
 "paste"{[System.Windows.Forms.Clipboard]::SetText($text);[System.Windows.Forms.SendKeys]::SendWait("^v")}
 "scroll"{[U2]::SetCursorPos($x,$y);[U2]::mouse_event(0x800,0,0,[int]$text,0)}
 "front"{$h=(Get-Process -Id $procid).MainWindowHandle;(New-Object -ComObject WScript.Shell).SendKeys('%');[U2]::ShowWindow($h,3)|Out-Null;[U2]::SetForegroundWindow($h)|Out-Null}
}
Start-Sleep -Seconds $wait
$b=New-Object System.Drawing.Bitmap 1920,1080;$g=[System.Drawing.Graphics]::FromImage($b);$g.CopyFromScreen(0,0,0,0,$b.Size);$b.Save("C:\project\youtube\shorts\gomgom\launch\ui\full.png")
