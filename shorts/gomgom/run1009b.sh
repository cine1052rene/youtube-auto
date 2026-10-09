#!/usr/bin/env bash
cd "$(dirname "$0")"; source env.sh
until grep -q "그림 끝" /tmp/run1009.log; do sleep 10; done
PYTHONIOENCODING=utf-8 python tts_redo.py 07:04 07:06 08:02 08:05 08:11 2>&1 | grep -v Warning
echo "녹음 끝"
