# usage: ui.ps1 -act click -x 1 -y 2 | -act paste -text "..." | -act key -keys "{ENTER}" ; always saves shot
param([string]$act="shot",[int]$x=0,[int]$y=0,[string]$text="",[string]$keys="",[string]$out="C:\project\youtube\shorts\gomgom\launch\ui\s.png",[int]$wait=2)
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
Add-Type @"
using System;using System.Runtime.InteropServices;
public class MU{[DllImport("user32.dll")]public static extern bool SetCursorPos(int x,int y);[DllImport("user32.dll")]public static extern void mouse_event(int f,int x,int y,int d,int e);}
"@
if($act -eq "click"){[MU]::SetCursorPos($x,$y);[MU]::mouse_event(2,0,0,0,0);[MU]::mouse_event(4,0,0,0,0)}
if($act -eq "paste"){[System.Windows.Forms.Clipboard]::SetText($text);[System.Windows.Forms.SendKeys]::SendWait("^v")}
if($act -eq "key"){[System.Windows.Forms.SendKeys]::SendWait($keys)}
if($act -eq "scroll"){[MU]::SetCursorPos($x,$y);[MU]::mouse_event(0x800,0,0,-360,0)}
Start-Sleep -Seconds $wait
$bmp=New-Object System.Drawing.Bitmap 960,1080
$g=[System.Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen(0,0,0,0,$bmp.Size);$bmp.Save($out)
