# 창 제목으로 찾기/앞으로: win.ps1 -list  |  win.ps1 -title "YouTube"
param([string]$title="",[switch]$list)
Add-Type @"
using System;using System.Text;using System.Collections.Generic;using System.Runtime.InteropServices;
public class W{public delegate bool CB(IntPtr h,IntPtr l);
[DllImport("user32.dll")]public static extern bool EnumWindows(CB c,IntPtr l);
[DllImport("user32.dll",CharSet=CharSet.Unicode)]public static extern int GetWindowText(IntPtr h,StringBuilder s,int n);
[DllImport("user32.dll")]public static extern bool IsWindowVisible(IntPtr h);
[DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")]public static extern bool ShowWindow(IntPtr h,int c);
public static List<KeyValuePair<IntPtr,string>> All(){var r=new List<KeyValuePair<IntPtr,string>>();EnumWindows((h,l)=>{if(IsWindowVisible(h)){var s=new StringBuilder(512);GetWindowText(h,s,512);if(s.Length>0)r.Add(new KeyValuePair<IntPtr,string>(h,s.ToString()));}return true;},IntPtr.Zero);return r;}}
"@
$all=[W]::All()
if($list){$all|%{"$($_.Key) | $($_.Value)"};exit}
$m=$all|?{$_.Value -like "*$title*"}|select -First 1
if(!$m){"NOTFOUND";exit 1}
(New-Object -ComObject WScript.Shell).SendKeys('%')
[W]::ShowWindow($m.Key,3)|Out-Null;[W]::SetForegroundWindow($m.Key)|Out-Null
"FRONT: $($m.Value)"
