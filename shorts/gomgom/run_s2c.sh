#!/usr/bin/env bash
cd "$(dirname "$0")"; source env.sh
until grep -q "영상 전부 끝" /tmp/run_s2b.log; do sleep 15; done
bash ep07/prod/generate.sh vid 06 10
echo "[$(date +%H:%M:%S)] 7화 재생성 끝"
