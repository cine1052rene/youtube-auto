#!/usr/bin/env bash
# 4화 반려 2컷 재생성 (01 소품 소개 / 03 비교의 탑)
# 01: 배지가 형광 핑크 플라스틱으로 나오고 가방을 끝까지 안 멤 → 펠트 하트 + 가방 착용 상태로
# 03: 액자 속이 실제 사람 사진 + 끝에 곰곰이가 화면 밖으로 사라짐 → 펠트 동물 사진 + 곰곰이 항상 화면 안
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master_s1.png
LOG=fix.log
MIN_BALANCE=12

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small coral pink felt heart badge on its chest and a tiny brown felt satchel bag across its body; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
VTAIL="Kong is lively and expressive, the bear mouth may open softly but no teeth are ever visible, every character keeps exactly the same needle-felted wool texture, proportions, colors and accessories from the first frame to the last and never turns into a cartoon or 2D character, smooth cinematic camera motion with a clear change of viewpoint, warm cozy mood, soft warm light, no text"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
balance() { higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('credits',0))" 2>/dev/null; }
guard() {
  local bal; bal=$(balance)
  python -c "import sys; sys.exit(0 if float('${bal:-0}') >= $MIN_BALANCE else 1)" || { log "잔액 부족(${bal}) — 중단"; exit 1; }
}
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
    log "생성 오류: $(echo "$out" | tr -d '\n' | head -c 250)"
    echo ""; return 1
  done
  echo ""; return 1
}
fetch() {
  local url
  url=$(higgsfield generate wait "$1" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))" 2>/dev/null)
  [ -n "$url" ] && curl -s -o "$2" "$url" && [ -s "$2" ]
}

mkdir -p img_reject
for k in 01 03; do
  [ -s "img/$k.png" ] && [ ! -s "img_reject/${k}_old.png" ] && cp "img/$k.png" "img_reject/${k}_old.png"
  [ -s "clips/$k.mp4" ] && [ ! -s "clips/${k}_old.mp4" ] && cp "clips/$k.mp4" "clips/${k}_old.mp4"
done

# ---------- 01: 소품 선물 ----------
IMG01="low angle morning shot inside a cozy felt bedroom with a round window, Gomgom sitting on a knitted rug already wearing the tiny brown felt satchel bag across its body, Kong hovering right in front of the bear chest holding a small flat matte coral pink wool felt heart badge with visible fuzzy felt fibers and stitched edges, the badge is small and completely matte with no glow and no plastic shine, sunbeams and floating dust sparkles"
MOV01="Kong presses the small matte coral felt heart badge onto the bear chest and it stays there, Gomgom looks down at the badge on its chest and pats it happily with both paws while still wearing the brown satchel, Kong flutters up and lands on the bear head, the camera rises slowly from floor level to eye level"

# ---------- 03: 비교의 탑 ----------
IMG03="wide low angle shot from the floor of a felt room at dusk, Gomgom standing small in the lower left of the frame looking up with a slightly shrinking posture, a tall leaning tower of small glowing golden photo frames rising above it, every photo inside the frames shows a tiny needle-felted animal friend such as a rabbit, a fox and a hedgehog on a picnic, no human faces anywhere, Kong perched on the lowest frame, soft blue evening shadows and warm glow"
MOV03="the tower of glowing frames leans and sways higher while Gomgom stays in the lower part of the frame the whole time, Gomgom pulls in its shoulders and takes a small step back still fully visible, Kong flutters up along the frames, the camera slowly arcs sideways around Gomgom and tilts up without ever losing the bear from the frame"

guard; log "그림 01 재생성"
id=$(create_job seedream_v5_lite --prompt "$IMG01, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
[ -n "$id" ] && { fetch "$id" img/01.png && log "완료 img/01.png" || log "다운로드 실패 그림 01"; }

guard; log "그림 03 재생성"
id=$(create_job seedream_v5_lite --prompt "$IMG03, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
[ -n "$id" ] && { fetch "$id" img/03.png && log "완료 img/03.png" || log "다운로드 실패 그림 03"; }

guard; log "영상 01 재생성"
id=$(create_job seedance1_5 --prompt "$MOV01, $VTAIL" --start-image "img/01.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
[ -n "$id" ] && { fetch "$id" clips/01.mp4 && log "완료 clips/01.mp4" || log "다운로드 실패 영상 01"; }

guard; log "영상 03 재생성"
id=$(create_job seedance1_5 --prompt "$MOV03, $VTAIL" --start-image "img/03.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
[ -n "$id" ] && { fetch "$id" clips/03.mp4 && log "완료 clips/03.mp4" || log "다운로드 실패 영상 03"; }

log "잔액 $(balance)"
log "FIX DONE"
