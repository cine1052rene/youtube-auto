#!/usr/bin/env bash
# 7·8화 그림이 끝나면 → 파생 TTS → 파생 그림 (영상은 그림 점검 뒤 따로)
cd "$(dirname "$0")"; source env.sh
while kill -0 379 2>/dev/null; do sleep 15; done
echo "[$(date +%H:%M:%S)] 7·8화 그림 끝"
bash ep07/prod/generate.sh img 05
python tts_verify.py epd01; python tts_verify.py epd02
bash epd01/prod/generate.sh img; bash epd02/prod/generate.sh img
echo "[$(date +%H:%M:%S)] 파생 TTS·그림 끝"
