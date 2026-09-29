#!/usr/bin/env bash
# 사용: heart_step.sh open X Y name  |  heart_step.sh click name  |  heart_step.sh close name
T=/c/project/youtube/challenges/daily_soul/tools; O=C:/project/youtube/challenges/daily_soul/tmp
PY=/c/Users/cine1/AppData/Local/Programs/Python/Python312/python.exe
cd $T
case $1 in
 open) powershell -NoProfile -File win.ps1 -title "Higgsfield - Assets" -x $2 -y $3 -out "$O/$4.png" -wait 2500 >/dev/null 2>&1
       $PY -c "from PIL import Image; im=Image.open('$O/$4.png'); im.resize((640,360)).save('$O/$4s.png')";;
 click) powershell -NoProfile -File win.ps1 -title "Higgsfield - Assets" -x 1762 -y 986 -hover -out "$O/$2.png" -wait 1800 >/dev/null 2>&1
       $PY -c "from PIL import Image; Image.open('$O/$2.png').crop((1560,940,1920,1030)).save('$O/$2c.png')";;
 close) powershell -NoProfile -File win.ps1 -title "Higgsfield - Assets" -x 1883 -y 63 -out "$O/$2.png" -wait 2500 >/dev/null 2>&1
       $PY -c "from PIL import Image; im=Image.open('$O/$2.png'); im.resize((960,540)).save('$O/$2s.png')";;
esac
