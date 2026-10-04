#!/usr/bin/env bash
# 곰곰한 마음 공용 콩이 삐약 효과음 5종 (mirelo 0.5cr씩)
set -u
cd "$(dirname "$0")"
LOG=gen.log
mkdir -p sfx
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
create_job() {
  local tries=0 out id
  while [ $tries -lt 10 ]; do
    out=$(higgsfield generate create "$@" --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')" 2>/dev/null)
    if [ -n "$id" ]; then echo "$id"; return 0; fi
    if echo "$out" | grep -qi "rate_limit\|concurrent"; then tries=$((tries+1)); sleep 30; continue; fi
    log "생성 오류: $(echo "$out" | tr -d '\n' | head -c 250)"; echo ""; return 1
  done
  echo ""; return 1
}
fetch() {
  local url
  url=$(higgsfield generate wait "$1" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))" 2>/dev/null)
  [ -n "$url" ] || return 1
  local ext="${url##*.}"; ext="${ext%%\?*}"; [ ${#ext} -le 4 ] || ext=mp3
  curl -s -o "$2.$ext" "$url" && [ -s "$2.$ext" ]
}
declare -A P=(
  [peep1]="1|a single tiny cute baby chick peep, loud and clear, recorded close to the microphone, no other sounds, no music"
  [peep2]="1.2|two quick happy baby chick peeps, cheerful and cute, close and clear, no other sounds, no music"
  [peep_happy]="2|a little baby chick chirping happily three or four times, excited and bouncy, cute, close and clear, no other sounds, no music"
  [peep_q]="1|a single curious baby chick peep rising in pitch like a question, loud and clear, recorded close to the microphone, no other sounds, no music"
  [peep_sleepy]="1.5|a sleepy little baby chick peep, cute, loud and clear, recorded close to the microphone, no other sounds, no music"
)
for k in peep1 peep2 peep_happy peep_q peep_sleepy; do
  ls sfx/$k.* >/dev/null 2>&1 && continue
  d="${P[$k]%%|*}"; p="${P[$k]#*|}"
  id=$(create_job mirelo_text_to_audio --prompt "$p" --duration "$d") || continue
  fetch "$id" "sfx/$k" && log "완료 sfx/$k" || log "실패 sfx/$k"
done
