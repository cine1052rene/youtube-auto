#!/usr/bin/env bash
# fix_owl.sh가 "보정 그림 끝"을 남길 때까지 기다렸다가 generate.sh 실행 (동시 작업 1개 제한 때문)
cd "$(dirname "$0")"
for i in $(seq 1 60); do
  grep -q "보정 그림 끝" fix.log 2>/dev/null && break
  sleep 10
done
echo "[$(date +%H:%M:%S)] 보정 끝 확인 → generate.sh 시작" >> gen.log
bash ./generate.sh
