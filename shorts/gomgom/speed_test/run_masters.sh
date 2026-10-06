#!/bin/bash
# 시즌1 마스터: 1.15배 · 간격 K(앞0.15/뒤0.45) · 제목 카드 3초 · 루프 · 효과음 없음 · 1080x1920
source /c/project/youtube/shorts/gomgom/env.sh
cd /c/project/youtube/shorts/gomgom/speed_test
for ep in 01 02 03 04 05 06; do
  for i in 1 2 3; do
    python make_sample.py $ep 1.15 MASTER_S1 --lead 0.15 --tail 0.45 --hook --hookdur 3.0 --end 1.2 --loop --full && break
    echo "재시도 $ep $i"
  done
  d=../ep$ep/prod/out; [ $ep = 01 ] && d=../ep01/v3/out
  cp out/ep${ep}_MASTER_S1.mp4 $d/ep${ep}_master_s1.mp4 && echo "복사 $d/ep${ep}_master_s1.mp4"
done
echo 전부끝
