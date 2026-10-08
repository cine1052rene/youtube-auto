param([int]$x1,[int]$y1,[int]$x2,[int]$y2)
Add-Type @"
using System;using System.Runtime.InteropServices;
public class S{[DllImport("user32.dll")]public static extern bool SetCursorPos(int x,int y);[DllImport("user32.dll")]public static extern void mouse_event(int f,int x,int y,int d,int e);}
"@
[S]::SetCursorPos($x1,$y1)|Out-Null;[S]::mouse_event(2,0,0,0,0)
for($i=1;$i -le 10;$i++){[S]::SetCursorPos([int]($x1+($x2-$x1)*$i/10),[int]($y1+($y2-$y1)*$i/10))|Out-Null;Start-Sleep -Milliseconds 15}
[S]::mouse_event(4,0,0,0,0)
