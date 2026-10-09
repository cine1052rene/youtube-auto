#!/bin/bash
# 10/9 자막 위치 수정(높이 1200·폭 740·오디오 48kHz) — 4~8화 마스터 재생성. 이전 파일은 *_oldsub.mp4로 보관
source /c/project/youtube/shorts/gomgom/env.sh
cd /c/project/youtube/shorts/gomgom/speed_test
for ep in 04 05 06 07 08; do
  if [ $ep = 07 ] || [ $ep = 08 ]; then tag=MASTER; dst=../ep$ep/prod/out/ep${ep}_master.mp4; else tag=MASTER_S1; dst=../ep$ep/prod/out/ep${ep}_master_s1.mp4; fi
  [ -f ${dst%.mp4}_oldsub.mp4 ] || cp $dst ${dst%.mp4}_oldsub.mp4
  for i in 1 2 3; do
    python make_sample.py $ep 1.15 $tag --lead 0.15 --tail 0.45 --hook --hookdur 3.0 --end 1.2 --loop --full && break
    echo "재시도 $ep $i"
  done
  cp out/ep${ep}_${tag}.mp4 $dst && echo "[$(date +%H:%M:%S)] 완료 $dst"
done
echo 전부끝
