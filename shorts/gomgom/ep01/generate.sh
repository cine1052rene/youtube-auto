#!/usr/bin/env bash
# 곰곰한 마음 1화 — 남은 그림 10장 + 영상 5개 순차 생성
# 이미 있는 파일은 건너뜀 (중단 후 다시 실행해도 이어서 진행)
set -u
cd "$(dirname "$0")"
REF=../ref/gomgom_master.png
LOG=gen.log
MIN_BALANCE=10

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile; Kong, a tiny round yellow felt bird with a small orange beak"
STYLE="soft warm golden light, dreamy bokeh with gentle floating sparkles, cozy warm pastel palette, handmade felt and knit textures, high quality 3D render, vertical composition, no text, no letters"
MOTION_TAIL="gentle natural motion, the characters keep exactly the same appearance, only a few subtle sparkles, soft warm light"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

balance() {
  higgsfield account status --json </dev/null 2>/dev/null \
    | python -c "import sys,json;print(json.load(sys.stdin).get('credits',0))" 2>/dev/null
}

# create with retry on rate limit; prints job id or empty
create_job() {
  local tries=0 out id
  while [ $tries -lt 6 ]; do
    out=$(higgsfield generate create "$@" --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')" 2>/dev/null)
    if [ -n "$id" ]; then echo "$id"; return 0; fi
    if echo "$out" | grep -q rate_limit; then
      tries=$((tries+1)); sleep 20; continue
    fi
    log "생성 오류: $(echo "$out" | head -c 250)"
    echo ""; return 1
  done
  echo ""; return 1
}

fetch() { # job_id out_file
  local url
  url=$(higgsfield generate wait "$1" --json </dev/null 2>/dev/null \
        | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))" 2>/dev/null)
  [ -n "$url" ] && curl -s -o "$2" "$url" && [ -s "$2" ]
}

guard() {
  local bal; bal=$(balance)
  python -c "import sys; sys.exit(0 if float('${bal:-0}') >= $MIN_BALANCE else 1)" \
    || { log "잔액 부족(${bal}) — 중단"; exit 1; }
}

mkdir -p img clips

# ---------- 그림 ----------
declare -A IMG
IMG[s02]="Gomgom curled up under a soft knit blanket on a cozy sofa with only the face peeking out, a bright sunny day visible through the window behind, lazy and snug"
IMG[s03]="close up of Gomgom lying on the sofa with a sleepy blank expression, face softly lit from below by the glow of a smartphone held just out of frame, the phone itself not visible, cozy afternoon room"
IMG[v04_start]="Gomgom sitting on the sofa at sunset in the middle of a big yawn with one paw resting on its head, looking tired, Kong perched on the sofa arm tilting its head with a worried look, warm orange evening light"
IMG[s05]="Gomgom sitting on a round rug looking up in wonder at four small warm glowing orbs of light floating in the air in front of it, Kong sitting beside Gomgom, cozy living room"
IMG[s06]="Gomgom gently closing a small closed laptop and sliding it aside on a low wooden table with a relieved little smile, the laptop lid shut, cozy room"
IMG[s07]="Gomgom stretching both arms high above its head in a big relaxing stretch with eyes happily closed, Kong on the floor spreading its tiny wings in the same pose, bright cozy room"
IMG[s09]="Gomgom standing and cheerfully choosing between a small straw sun hat held in one paw and a plain cloth-covered book with a blank cover held in the other paw, thoughtful happy expression"
IMG[v10_start]="Gomgom sitting up on the sofa and placing a smartphone face down on a soft cushion, Kong flying toward Gomgom's shoulder with its tiny wings spread, afternoon light"
IMG[s11]="Gomgom walking along a small winding path through a warm park at golden sunset with Kong perched on its shoulder, soft blossoming trees and little flowers along the path"
IMG[v13_start]="Gomgom and Kong sitting side by side on a wooden windowsill looking at each other and smiling, warm pink and orange sunset sky outside the window"

ORDER_IMG="s02 s03 v04_start s05 s06 s07 s09 v10_start s11 v13_start"
for k in $ORDER_IMG; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard
  log "그림 생성 $k"
  id=$(create_job seedream_v5_lite --prompt "${IMG[$k]}, $CHAR, $STYLE" \
        --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 $k ($id)"
done

# ---------- 영상 ----------
declare -A VID
VID[v01]="Gomgom slowly scrolls the smartphone and lets out a small sigh, its body sinking a little deeper into the sofa, camera almost still"
VID[v04]="Gomgom finishes a big yawn and rubs its head with one paw, Kong tilts its head curiously, camera still"
VID[v10]="Gomgom puts the smartphone down and sits up, Kong flies in and lands softly on Gomgom's shoulder, camera still"
VID[v12]="Gomgom lifts the mug and takes a slow sip as steam rises, very slow push in"
VID[v13]="Gomgom and Kong turn to each other and smile, the sunset light outside grows warmer, slow pull back"

ORDER_VID="v01 v04 v10 v12 v13"
for k in $ORDER_VID; do
  f="clips/$k.mp4"; start="img/${k}_start.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "$start" ] || { log "시작 그림 없음 $start — 건너뜀"; continue; }
  guard
  log "영상 생성 $k"
  id=$(create_job veo3_1_lite --prompt "${VID[$k]}, $MOTION_TAIL" \
        --start-image "$start" --aspect_ratio 9:16 --duration 4 --generate_audio false) || true
  [ -z "$id" ] && { log "실패 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 $k ($id)"
done

log "잔액 $(balance)"
missing=0
for k in $ORDER_IMG v01_start s08 v12_start; do [ -s "img/$k.png" ] || { log "누락 img/$k.png"; missing=1; }; done
for k in $ORDER_VID; do [ -s "clips/$k.mp4" ] || { log "누락 clips/$k.mp4"; missing=1; }; done
[ $missing -eq 0 ] && log "ALL DONE" || log "FINISHED WITH MISSING"
