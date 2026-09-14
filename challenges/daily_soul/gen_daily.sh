#!/usr/bin/env bash
# Daily Soul 후보 생성: challenges/daily_soul/<날짜>/prompts.txt 의 각 줄을 Soul 2.0(3:2, 2k)으로 1장씩 생성
# 사용: bash challenges/daily_soul/gen_daily.sh 2026-09-16
# 이미 받은 파일은 건너뛰므로 다시 실행해도 이어서 진행
set -u
DAY="${1:?날짜(YYYY-MM-DD)를 넣어주세요}"
DIR="$(cd "$(dirname "$0")" && pwd)/$DAY"
cd "$DIR" || { echo "폴더 없음: $DIR"; exit 1; }
[ -s prompts.txt ] || { echo "prompts.txt 없음"; exit 1; }
LOG=gen.log
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
balance(){ higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin)['credits'])"; }

BAL=$(balance)
python -c "import sys; sys.exit(0 if float('${BAL:-0}') >= 20 else 1)" || { log "잔액 부족(${BAL}) — 중단"; exit 1; }

n=0
tr -d '\r' < prompts.txt | while IFS= read -r line; do
  [ -z "$line" ] && continue
  n=$((n+1)); f=$(printf "cand_%02d.png" $n)
  [ -s "$f" ] && { log "skip $f"; continue; }
  out=$(higgsfield generate create text2image_soul_v2 --prompt "$line" --aspect_ratio 3:2 --quality 2k --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { log "FAIL create $f: $(echo "$out" | tr -d '\n' | head -c 200)"; sleep 5; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  if [ -n "$url" ] && curl -s -o "$f" "$url" && [ -s "$f" ]; then log "done $f id=$id"; else log "FAIL $f id=$id (서버 실패 시 크레딧 미차감)"; fi
done
log "ALL DONE balance=$(balance)"
