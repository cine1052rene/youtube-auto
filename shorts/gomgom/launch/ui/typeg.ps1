param([string]$file,[int]$ms=140)
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;using System.Text;using System.Runtime.InteropServices;
public class G{[DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();[DllImport("user32.dll",CharSet=CharSet.Unicode)]public static extern int GetWindowText(IntPtr h,StringBuilder s,int n);}
"@
function FG(){$s=New-Object Text.StringBuilder 256;[G]::GetWindowText([G]::GetForegroundWindow(),$s,256)|Out-Null;$s.ToString()}
$keys = Get-Content $file -Raw -Encoding UTF8; $keys=$keys.TrimEnd("`r","`n")
$i=0
while($i -lt $keys.Length){
  $f=FG; if(($f -notlike "*휴대폰*" -and $f -notlike "*S23*")){ "ABORT at $i fg=$f"; exit 1 }
  $c=$keys[$i]
  if($c -eq '{'){ $j=$keys.IndexOf('}',$i+1); if($j -eq $i+1){$j=$keys.IndexOf('}',$i+2)}; $tok=$keys.Substring($i,$j-$i+1); $i=$j+1 }
  else { $tok=[string]$c; $i++ }
  [System.Windows.Forms.SendKeys]::SendWait($tok); Start-Sleep -Milliseconds $ms
}
"DONE"

