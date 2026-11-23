#!/usr/bin/env bash
O=C:/project/youtube/challenges/daily_soul/tmp/hof
for t in "$@"; do IFS=, read k x y <<<"$t"
  powershell -NoProfile -File hof.ps1 -k $k -out $O/z.png >/dev/null 2>&1
  powershell -NoProfile -File win.ps1 -title "Higgsfield AI - Discord" -x $x -y $y -out $O/z.png -wait 3000 >/dev/null 2>&1
  powershell -NoProfile -File win.ps1 -title "Higgsfield AI - Discord" -x 1200 -y 500 -scroll -360 -out $O/t_${k}_${y}.png -wait 1200 >/dev/null 2>&1
  echo "done $t"
done
