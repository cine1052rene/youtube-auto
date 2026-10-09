#!/usr/bin/env bash
# 10/10 (축소) 7화 01·03·08·12(콩이 1/3 기준 s2c) + 8화 06(토끼 크기)·10(입 이중) → 마스터 재조립
cd "$(dirname "$0")"; source env.sh
(cd ep07/prod && bash generate.sh img 01 03 08 12)
(cd ep08/prod && bash generate.sh img 06 10)
echo "그림 끝"
(cd ep07/prod && bash generate.sh vid 01 03 08 12)
(cd ep08/prod && bash generate.sh vid 06 10)
echo "영상 끝"
cd speed_test
for ep in 07 08; do python make_sample.py $ep 1.15 MASTER --lead 0.15 --tail 0.45 --hook --hookdur 3.0 --end 1.2 --loop --full && cp out/ep${ep}_MASTER.mp4 ../ep$ep/prod/out/ep${ep}_master.mp4 && echo "마스터 $ep"; done
echo "전부 끝"
