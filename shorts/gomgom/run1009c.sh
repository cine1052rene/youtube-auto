#!/usr/bin/env bash
cd "$(dirname "$0")"; source env.sh
until grep -q "녹음 끝" /tmp/run1009b.log; do sleep 10; done
(cd ep07/prod && bash generate.sh vid 02 08 12)
(cd ep08/prod && bash generate.sh vid 07 08 10)
echo "영상 끝"
cd speed_test
for ep in 07 08; do python make_sample.py $ep 1.15 MASTER --lead 0.15 --tail 0.45 --hook --hookdur 3.0 --end 1.2 --loop --full && cp out/ep${ep}_MASTER.mp4 ../ep$ep/prod/out/ep${ep}_master.mp4 && echo "마스터 $ep"; done
echo "전부 끝"
