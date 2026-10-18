param([string]$file,[int]$ms=130)
Add-Type -AssemblyName System.Windows.Forms
$keys = Get-Content $file -Raw -Encoding UTF8
$i=0
while($i -lt $keys.Length){
  $c=$keys[$i]
  if($c -eq '{'){ $j=$keys.IndexOf('}',$i+1); if($j -eq $i+1){$j=$keys.IndexOf('}',$i+2)}; $tok=$keys.Substring($i,$j-$i+1); $i=$j+1 }
  else { $tok=[string]$c; $i++ }
  [System.Windows.Forms.SendKeys]::SendWait($tok); Start-Sleep -Milliseconds $ms
}
