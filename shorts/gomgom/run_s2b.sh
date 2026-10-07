#!/usr/bin/env bash
cd "$(dirname "$0")"; source env.sh
until grep -q "파생 TTS·그림 끝" /tmp/run_s2.log; do sleep 15; done
bash ep08/prod/generate.sh img 08
bash ep07/prod/generate.sh img 05
bash ep08/prod/generate.sh img 08
echo "[$(date +%H:%M:%S)] 그림 전부 끝 — 영상 시작"
bash ep07/prod/generate.sh vid
bash ep08/prod/generate.sh vid
bash epd01/prod/generate.sh vid
bash epd02/prod/generate.sh vid
echo "[$(date +%H:%M:%S)] 영상 전부 끝"
