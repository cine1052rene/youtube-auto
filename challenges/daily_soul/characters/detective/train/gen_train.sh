#!/usr/bin/env bash
# 학습용 사진 생성: seedream_v5_lite + 기준 이미지 참조. 이미 받은 파일은 건너뜀
export PATH="$PATH:/c/Users/cine1/AppData/Roaming/npm:/c/Users/cine1/AppData/Local/Programs/Python/Python312"
cd "$(dirname "$0")"; R=../sd/ch01.png; LOG=gen.log
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
n=0
tr -d '\r' < prompts.txt | while IFS='|' read -r ar line; do
  [ -z "$line" ] && continue; n=$((n+1)); f=$(printf "t%02d.png" $n); [ -s "$f" ] && { log "skip $f"; continue; }
  for try in $(seq 1 10); do
    out=$(higgsfield generate create seedream_v5_lite --prompt "$line" --aspect_ratio "$ar" --quality high --image-references "$R" --json </dev/null 2>&1)
    echo "$out" | grep -qiE "rate_limit|concurrent" || break; log "busy $f retry $try"; sleep 60; done
  id=$(echo "$out" | python -c "import sys,json
try: d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except: print('')")
  [ -z "$id" ] && { log "FAIL create $f: $(echo "$out"|tr -d '\n'|head -c 150)"; continue; }
  for i in $(seq 1 50); do r=$(higgsfield generate get "$id" --json </dev/null 2>/dev/null); st=$(echo "$r" | python -c "import sys,json;print(json.load(sys.stdin).get('status',''))" 2>/dev/null); [ "$st" = completed -o "$st" = failed ] && break; sleep 6; done
  url=$(echo "$r" | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))" 2>/dev/null)
  if [ -n "$url" ] && curl -s -o "$f" "$url" && [ -s "$f" ]; then log "done $f id=$id"; else log "FAIL $f id=$id st=$st"; fi
done
log "ALL DONE balance=$(higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin)['credits'])")"
