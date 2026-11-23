# hall-of-fame 열고 최신으로 이동 후 위로 k번(1800) 스크롤해 캡처: hof.ps1 -k 4 -out path
param([int]$k=0,[string]$out)
$t="C:\project\youtube\challenges\daily_soul\tools"
& "$t\win.ps1" -title "Higgsfield AI - Discord" -max -x 173 -y 497 -out $out -wait 2000 | Out-Null
& "$t\dc.ps1" -x 900 -y 500 -key "{ESC}" -out $out -wait 1500 | Out-Null
& "$t\win.ps1" -title "Higgsfield AI - Discord" -x 900 -y 500 -scroll -60000 -out $out -wait 1200 | Out-Null
for($i=0;$i -lt $k;$i++){ & "$t\win.ps1" -title "Higgsfield AI - Discord" -x 900 -y 500 -scroll 1800 -out $out -wait 700 | Out-Null }
& "$t\win.ps1" -title "Higgsfield AI - Discord" -out $out -wait 800 | Out-Null
