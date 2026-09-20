#!/usr/bin/env bash
# TTS가 끝나면 5화 → 6화 순서로 생성
set -u
cd "$(dirname "$0")"
for i in $(seq 1 120); do
  grep -q "ep06 내레이션 합계" /tmp/gomgom_tts56.log 2>/dev/null && break
  sleep 15
done
echo "[$(date +%H:%M:%S)] TTS 끝 — 5화 생성 시작"
bash ep05/prod/generate.sh
echo "[$(date +%H:%M:%S)] 5화 생성 끝 — 6화 생성 시작"
bash ep06/prod/generate.sh
echo "[$(date +%H:%M:%S)] 5·6화 생성 전부 끝"
