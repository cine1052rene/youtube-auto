param([int]$n=24)
$t="C:\project\youtube\challenges\daily_soul\tools"; $o="C:\project\youtube\challenges\daily_soul\tmp\hof"
New-Item -ItemType Directory -Force -Path $o | Out-Null
& "$t\win.ps1" -title "Higgsfield AI - Discord" -max -x 173 -y 497 -out "$o\z.png" -wait 2000 | Out-Null
& "$t\dc.ps1" -x 900 -y 500 -key "{ESC}" -out "$o\z.png" -wait 1500 | Out-Null
& "$t\win.ps1" -title "Higgsfield AI - Discord" -x 900 -y 500 -scroll -60000 -out ("$o\p00.png") -wait 1500 | Out-Null
for($i=1;$i -le $n;$i++){ & "$t\win.ps1" -title "Higgsfield AI - Discord" -x 900 -y 500 -scroll 1800 -out ("$o\p{0:D2}.png" -f $i) -wait 900 | Out-Null }
