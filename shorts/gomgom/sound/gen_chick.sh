#!/usr/bin/env bash
# 곰곰한 마음 공용 병아리(갓 부화한 아기 병아리) 소리 후보 6종
set -u
cd "$(dirname "$0")"
LOG=gen.log

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
mkdir -p chick
declare -A P=(
  [c1]="1.2|a newborn fluffy yellow baby chick cheeping piyo piyo, very high pitched tiny soft cheeps of a hatchling chick, not an adult bird, not a songbird, no bird song, no tweeting, close and clear, no other sounds"
  [c2]="1.5|a tiny baby chick going peep peep peep, high thin repeated cheeps of a just hatched chicken chick on a farm, not a wild bird, no birdsong, close microphone, no other sounds"
  [c3]="1|one single short high pitched cheep of a cute little hatchling chick, like a fluffy baby chicken, not a sparrow, not a songbird, close and clear, no other sounds"
  [c4]="2|a small group of baby chicks cheeping softly in a box, high pitched piyo piyo cheeps of newborn chickens, cozy and cute, not wild birds, no birdsong, no other sounds"
  [c5]="1.2|a happy excited baby chick cheeping quickly three times, high pitched newborn chicken chick, cartoonishly cute, not a songbird, close and clear, no other sounds"
  [c6]="1.5|a sleepy baby chick making a soft drowsy cheep then a tiny sigh, newborn chicken hatchling, very cute, not an adult bird, close and clear, no other sounds"
)
for k in c1 c2 c3 c4 c5 c6; do
  ls chick/$k.* >/dev/null 2>&1 && continue
  d="${P[$k]%%|*}"; p="${P[$k]#*|}"
  id=$(create_job mirelo_text_to_audio --prompt "$p" --duration "$d") || continue
  fetch "$id" "chick/$k" && log "완료 chick/$k" || log "실패 chick/$k"
done
