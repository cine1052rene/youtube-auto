#!/usr/bin/env bash
cd "$(dirname "$0")"; source env.sh
until grep -q "전부 끝" /tmp/run1009c.log; do sleep 15; done
PYTHONIOENCODING=utf-8 python tts_redo.py 07:04 07:06 --keep 2>&1 | grep -v Warning
cd speed_test && python make_sample.py 07 1.15 MASTER --lead 0.15 --tail 0.45 --hook --hookdur 3.0 --end 1.2 --loop --full && cp out/ep07_MASTER.mp4 ../ep07/prod/out/ep07_master.mp4 && echo "마스터 07 다시"
echo "최종 끝"
