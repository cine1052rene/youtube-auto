#!/usr/bin/env bash
# 곰곰한 마음 공용 효과음 7개(mirelo, 0.5cr) + 배경음악 후보 2개(sonilo, 약 2.5~3cr) — 이어서 실행 가능
set -u
cd "$(dirname "$0")"
LOG=gen.log
mkdir -p sfx bgm
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

declare -A SFX=(
  [pop]="1.5|a clear bright magical sparkle sound effect, a short shimmering twinkle with a cute pop at the start, clearly audible, no voice, no music"
  [hop]="1|a cute cartoon boing hop sound effect, short springy bounce, clearly audible, playful, no voice, no music"
  [whoosh]="1.2|a soft airy whoosh of a little bird fluttering past, gentle feather wings, light and cute, no voice"
  [chime]="2|a single warm soft wind chime ding with a gentle fade, calm and cozy, no voice"
  [drizzle]="2|a tiny gentle rain drizzle pattering softly on a small felt cloud, cozy and quiet, no thunder, no voice"
  [clink]="1|two small ceramic teacups gently clinking together once, warm and cozy, no voice"
  [twinkle]="2|a clear music box melody of three gentle descending notes, warm and peaceful ending jingle, clearly audible, no voice"
)
for k in pop hop whoosh chime drizzle clink twinkle; do
  ls sfx/$k.* >/dev/null 2>&1 && { log "건너뜀 sfx/$k"; continue; }
  d="${SFX[$k]%%|*}"; p="${SFX[$k]#*|}"
  id=$(create_job mirelo_text_to_audio --prompt "$p" --duration "$d") || continue
  fetch "$id" "sfx/$k" && log "완료 sfx/$k" || log "실패 sfx/$k"
done

declare -A BGM=(
  [bgm_a]="a warm cozy instrumental for a cute needle-felted bear story, soft ukulele and glockenspiel with light pizzicato strings, gentle and slightly bouncy, about 92 bpm, hopeful and tender, no vocals, seamless steady mood without big drops"
  [bgm_b]="a soft music box and felt piano lullaby with light brushed percussion, warm and calm but gently moving, about 84 bpm, cozy storybook feeling, no vocals, steady mood without big changes"
)
for k in bgm_a bgm_b; do
  ls bgm/$k.* >/dev/null 2>&1 && { log "건너뜀 bgm/$k"; continue; }
  id=$(create_job sonilo_music --prompt "${BGM[$k]}" --duration 45) || continue
  fetch "$id" "bgm/$k" && log "완료 bgm/$k" || log "실패 bgm/$k"
done
log "끝"
