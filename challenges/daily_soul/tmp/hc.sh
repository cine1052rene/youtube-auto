#!/usr/bin/env bash
# heart current detail, crop, close, then open next X Y name
cd /c/project/youtube/challenges/daily_soul/tools; O=C:/project/youtube/challenges/daily_soul/tmp; PY=/c/Users/cine1/AppData/Local/Programs/Python/Python312/python.exe
powershell -NoProfile -File win.ps1 -title "Higgsfield - Assets" -x 1747 -y 983 -out "$O/hk_$1.png" -wait 1800 >/dev/null 2>&1
$PY -c "from PIL import Image; Image.open('$O/hk_$1.png').crop((1540,940,1900,1030)).save('$O/hk_$1c.png')"
cd ..; bash tools/heart_step.sh close c_$1
[ -n "$2" ] && bash tools/heart_step.sh open $2 $3 $4
