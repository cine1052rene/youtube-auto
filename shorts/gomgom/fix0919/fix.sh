#!/usr/bin/env bash
# 9/19 1·2화 보정: 입 벌림/캐릭터 변형 컷 재생성 (원본은 clips/NN_old.mp4 로 백업)
# 1화 04(그림+영상) 05 10 13 / 2화 09 12 — 전부 Seedance 1.5 (10·13은 Wan 얼굴 변형 문제로 모델 교체, 8초)
# 이미 끝난 컷(NN_old 있고 NN.mp4 새로 있음)은 건너뜀 → 다시 실행해도 이어서 진행
set -u
cd "$(dirname "$0")"
LOG=fix.log
REF=../ref/gomgom_master.png
E1=../ep01/v3; E2=../ep02/prod
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
balance(){ higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('credits',0))"; }

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle closed-mouth smile with the mouth always closed; Kong, a tiny round yellow felt baby chick with a small orange beak"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, no text, no letters"
VTAIL="Gomgom keeps its mouth gently closed in a soft closed-mouth smile the whole time and never opens its mouth, Kong stays a tiny yellow baby chick, both characters keep exactly the same appearance and stay cute with bright open eyes, no close-up on the faces, smooth gentle camera motion, soft warm light, no text"

# 무료 플랜 동시 1개 — Daily Soul과 겹치면 30초 간격 최대 20회 재시도(실패 호출은 미차감)
create_job(){
  local out id
  for t in $(seq 1 20); do
    out=$(higgsfield generate create "$@" --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
    [ -n "$id" ] && { echo "$id"; return 0; }
    if echo "$out" | grep -qiE "rate_limit|concurrent"; then log "busy — 30초 대기 $t/20"; sleep 30; continue; fi
    log "생성 오류: $(echo "$out" | tr -d '\n' | head -c 250)"; return 1
  done; return 1
}
fetch(){ local url; url=$(higgsfield generate wait "$1" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))"); [ -n "$url" ] && curl -s -o "$2" "$url" && [ -s "$2" ]; }

# ---- 1화 04 시작 그림 교체 (하품 → 졸린 듯 입 다문 미소) ----
if [ ! -s "$E1/img_reject/04_old.png" ]; then
  mkdir -p "$E1/img_reject"; cp "$E1/img/04.png" "$E1/img_reject/04_old.png"
  log "1화 그림 04 재생성"
  id=$(create_job seedream_v5_lite --prompt "side profile medium shot of Gomgom sitting on the sofa at sunset, sleepily rubbing its head with one paw, eyes softly half closed and mouth closed in a drowsy closed-mouth smile, Kong standing on top of Gomgom's head gently patting it with one tiny wing, warm orange light streaming through the window, felt town rooftops outside, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) \
    && fetch "$id" "$E1/img/04.png" && log "완료 1화 그림 04" || log "실패 1화 그림 04"
fi

# 영상: 에피소드폴더 컷번호 길이 프롬프트
run(){
  local dir=$1 k=$2 dur=$3 prompt=$4 f="$1/clips/$2.mp4" old="$1/clips/$2_old.mp4"
  if [ -s "$old" ] && [ -s "$f" ] && [ "$f" -nt "$old" ] && [ "$(stat -c %s "$f")" != "$(stat -c %s "$old")" ]; then log "건너뜀 $f (이미 교체됨)"; return; fi
  [ -s "$old" ] || cp "$f" "$old"
  log "영상 $dir $k (Seedance ${dur}초)"
  id=$(create_job seedance1_5 --prompt "$prompt, $VTAIL" --start-image "$dir/img/$k.png" --aspect_ratio 9:16 --duration $dur --generate_audio false --resolution 720p) || { log "실패 $dir $k"; return; }
  fetch "$id" "$dir/clips/${k}_new.mp4" && mv -f "$dir/clips/${k}_new.mp4" "$f" && log "완료 $f" || log "다운로드 실패 $dir $k ($id)"
}

run $E1 04 4 "the camera slowly arcs around to the front, Gomgom sleepily rubs its head and blinks slowly, Kong pats Gomgom's head with its tiny wing and does a small happy hop"
run $E1 05 4 "Gomgom stays sitting on the rug the whole time and only looks up at the glowing orbs with wonder, Gomgom never rises or floats, Kong the tiny yellow baby chick flutters up and circles playfully around the glowing orbs, only Kong and the orbs move in the air, the camera slowly rises upward"
run $E1 10 8 "Gomgom puts the smartphone down on the cushion and sits up, Kong flies across the cozy room toward Gomgom and lands softly on top of Gomgom's head, Gomgom looks up happily with a gentle closed-mouth smile, the camera calmly follows Kong at a comfortable distance"
run $E1 13 8 "Gomgom and Kong stay sitting side by side on the wooden window ledge seen from behind, Kong snuggles against Gomgom's shoulder, Gomgom tilts its head gently toward Kong, the camera slowly rises and pulls back to reveal the glowing felt town under the pink and orange sunset sky, the characters stay small in the frame"
run $E2 09 4 "Gomgom puffs up its chest proudly with a gentle closed-mouth smile, Kong mimics and puffs up its feathers, both nod together, the camera slowly rises"
run $E2 12 4 "the scale gently wobbles and settles perfectly level, Gomgom claps its paws happily with a gentle closed-mouth smile, Kong does a little dance beside the scale, slow camera pull back"

log "보정 끝 잔액=$(balance)"
