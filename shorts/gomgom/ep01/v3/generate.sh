#!/usr/bin/env bash
# 곰곰한 마음 1화 v3 — 13컷 전부 영상 (Seedance 1.5 기본 + 핵심 컷 Wan 2.7)
# 재사용: 01(그림+Wan 영상), 05(끝그림을 시작그림으로), 11(그림+Veo 영상)
# 이미 있는 파일은 건너뜀 → 중단 후 다시 실행해도 이어서 진행
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master.png
LOG=gen.log
MIN_BALANCE=15

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile; Kong, a tiny round yellow felt baby chick with a small orange beak"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, no text, no letters"
VTAIL="Kong is lively and expressive, both characters keep exactly the same appearance and stay cute with bright open eyes, smooth cinematic camera motion, soft warm light, no text"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
balance() { higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('credits',0))" 2>/dev/null; }
guard() {
  local bal; bal=$(balance)
  python -c "import sys; sys.exit(0 if float('${bal:-0}') >= $MIN_BALANCE else 1)" || { log "잔액 부족(${bal}) — 중단"; exit 1; }
}
create_job() {
  local tries=0 out id
  while [ $tries -lt 6 ]; do
    out=$(higgsfield generate create "$@" --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')" 2>/dev/null)
    if [ -n "$id" ]; then echo "$id"; return 0; fi
    if echo "$out" | grep -q rate_limit; then tries=$((tries+1)); sleep 20; continue; fi
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

mkdir -p img clips
# ---------- 재사용 ----------
[ -s img/01.png ]   || cp ../v2/img/t01.png img/01.png
[ -s clips/01.mp4 ] || cp ../v2/clips/t01_wan27.mp4 clips/01.mp4
[ -s img/05.png ]   || cp ../v2/img/t05_end.png img/05.png
[ -s img/11.png ]   || cp ../v2/img/t11.png img/11.png
[ -s clips/11.mp4 ] || cp ../v2/clips/t11.mp4 clips/11.mp4
log "재사용 준비 완료 (01, 05 시작그림, 11)"

# ---------- 시작 그림 ----------
declare -A IMG
IMG[02]="close up from a low side angle of Gomgom curled up under a chunky knit blanket on the sofa with only the face peeking out, Kong hopping along the top of the blanket, a sunny window with a felt town behind, shelves and plants in the background"
IMG[03]="over the shoulder view from behind Gomgom lying on the sofa holding a smartphone whose screen shows only a soft blank glow, Kong peeking curiously over the top edge of the phone, cozy living room with string lights and bookshelves beyond"
IMG[04]="side profile medium shot of Gomgom sitting on the sofa at sunset in the middle of a big yawn with one paw on its head, Kong standing on top of Gomgom's head gently patting it with one tiny wing, warm orange light streaming through the window, felt town rooftops outside"
IMG[06]="top down overhead view of a low wooden coffee table with little mugs, coasters and a felt plant, Gomgom gently closing a small laptop while Kong pushes the lid down with its whole tiny body, a knitted rug around the table"
IMG[07]="wide low angle front view of Gomgom standing on a knitted rug stretching both arms high above its head with eyes happily closed, Kong beside Gomgom copying the stretch with both tiny wings raised high, bright cozy room with plants, shelves and a big window"
IMG[08]="macro close up at table height beside a sunny windowsill full of tiny felt plants, Gomgom carefully watering a small green sprout in a terracotta pot with a little watering can, Kong splashing happily in a tiny puddle of water drops next to the pot"
IMG[09]="three quarter view of Gomgom standing in a cozy wooden entryway with wall hooks, little coats, a shoe rack and a round door window, holding a straw sun hat in one paw and a plain cloth book with a blank cover in the other, Kong popping its head out from inside the straw hat"
IMG[10]="wide side view of the cozy living room in afternoon light, Gomgom sitting up on the knitted sofa and placing a smartphone face down on a cushion, Kong in mid flight across the room with tiny wings spread wide toward Gomgom, bookshelves, string lights and plants all around"
IMG[12]="close up at a warm kitchen windowsill with tiny jars, a teapot and hanging herbs, Gomgom holding a mug of hot cocoa with steam rising, Kong beside the mug dipping its beak into a tiny thimble cup of cocoa, soft golden afternoon glow"
IMG[13]="wide view from behind and slightly above of Gomgom and Kong sitting side by side on a wooden window ledge, looking out over a handmade felt town with glowing windows and rolling hills under a warm pink and orange sunset sky"

for k in 02 03 04 06 07 08 09 10 12 13; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard; log "그림 생성 $k"
  id=$(create_job seedream_v5_lite --prompt "${IMG[$k]}, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 그림 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 그림 $k ($id)"
done

# ---------- 영상 ----------
declare -A MOV
MOV[02]="the camera slowly slides sideways along the blanket, Kong hops happily from one knit bump to the next, Gomgom's eyes follow Kong and it snuggles deeper under the blanket"
MOV[03]="the camera gently moves closer over Gomgom's shoulder, Gomgom scrolls lazily, Kong leans further over the edge of the phone, tilts its head and flaps its wings in curiosity"
MOV[04]="the camera slowly arcs around to the front, Gomgom finishes a big yawn and rubs its head, Kong pats Gomgom's head with its wing and chirps"
MOV[05]="the camera slowly rises upward, the four glowing orbs gently drift, Kong flutters up and circles playfully around the orbs, Gomgom watches in wonder"
MOV[06]="the camera slowly rotates from directly overhead, Gomgom closes the laptop and Kong helps by pushing the lid down, then Kong sits on the closed laptop proudly"
MOV[07]="the camera slowly pulls back to reveal the bright room, Gomgom stretches high, Kong copies the stretch and does a tiny happy hop"
MOV[08]="the camera slowly pushes in, water drops sparkle as Gomgom waters the sprout, Kong splashes in the tiny puddle and shakes off the droplets"
MOV[09]="the camera gently orbits a little, Gomgom looks back and forth between the hat and the book, Kong pops out of the straw hat and wiggles"
MOV[12]="the camera slowly pushes in toward the mugs, steam curls up, Gomgom takes a slow sip, Kong dips its beak into its tiny cup and looks up happily"
declare -A WAN
WAN[10]="the camera follows Kong flying across the room, Gomgom puts the smartphone down and sits up, Kong lands softly on top of Gomgom's head and Gomgom smiles"
WAN[13]="Gomgom and Kong turn to each other and smile, Kong snuggles against Gomgom's cheek, the camera slowly rises and pulls back to reveal the glowing felt town under the sunset"
declare -A WANDUR=( [10]=6 [13]=5 )

for k in 02 03 04 05 06 07 08 09 12; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상(Seedance) $k"
  id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done
for k in 10 13; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상(Wan ${WANDUR[$k]}초) $k"
  id=$(create_job wan2_7 --prompt "${WAN[$k]}, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration ${WANDUR[$k]} --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done

log "잔액 $(balance)"
missing=0
for k in 01 02 03 04 05 06 07 08 09 10 11 12 13; do
  [ -s "clips/$k.mp4" ] || { log "누락 clips/$k.mp4"; missing=1; }
done
[ $missing -eq 0 ] && log "ALL DONE" || log "FINISHED WITH MISSING"
