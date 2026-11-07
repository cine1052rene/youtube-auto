# 크롬 창 중 제목에 키워드가 든 창을 찾아 최대화·앞으로 (EnumWindows)
param([string]$kw="Higgsfield", [string]$not="Discord")
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class EW {
 public delegate bool P(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumWindows(P f, IntPtr l);
 [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, UIntPtr e);
 public static List<KeyValuePair<IntPtr,string>> All(){ var r=new List<KeyValuePair<IntPtr,string>>(); EnumWindows((h,l)=>{ if(IsWindowVisible(h)){var sb=new StringBuilder(512); GetWindowText(h,sb,512); if(sb.Length>0) r.Add(new KeyValuePair<IntPtr,string>(h,sb.ToString()));} return true;}, IntPtr.Zero); return r; }
}
"@
$w = [EW]::All() | Where-Object { $_.Value -like "*$kw*" -and $_.Value -notlike "*$not*" } | Select-Object -First 1
if (-not $w) { "NONE"; [EW]::All() | ForEach-Object { $_.Value } ; exit 1 }
[EW]::ShowWindow($w.Key,9)|Out-Null; [EW]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [EW]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
[EW]::SetForegroundWindow($w.Key)|Out-Null; Start-Sleep -Milliseconds 400; [EW]::ShowWindow($w.Key,3)|Out-Null
"FRONT: " + $w.Value
