#!/usr/bin/env bash
# 곰곰한 마음 3화 — 11컷 전부 영상 (Seedance 1.5 기본 + 01·11 Wan 2.7)
# 곰곰이는 모든 컷에서 입 다문 미소. 마무리 컷에서 날지 않음.
# 이미 있는 파일은 건너뜀 → 중단 후 다시 실행해도 이어서 진행
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master.png
LOG=gen.log
MIN_BALANCE=10

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle closed-mouth smile with the mouth always closed; Kong, a tiny round yellow felt baby chick with a small orange beak"
OWL="Grandpa Owl, a kind old round felt owl with fluffy white eyebrows, small round spectacles, a tiny green laurel wreath and a little white toga"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
VTAIL="Kong is lively and expressive, Gomgom keeps its mouth closed with a gentle closed-mouth smile, both characters keep exactly the same appearance and colors and stay cute with bright open eyes, smooth cinematic camera motion, warm cozy mood, soft warm light, no text"

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

# ---------- 시작 그림 ----------
declare -A IMG
IMG[01]="wide high angle shot of an extravagant handmade felt banquet hall with a very long table piled with towering pastel layer cakes, golden goblets, fruit pyramids and glittering chandeliers, Gomgom sitting at the far end wearing a tiny oversized golden crown and looking a little overwhelmed, Kong perched on top of a tall cake pecking at a cherry"
IMG[02]="wide low angle shot of a sunny handmade felt Greek garden with small white stone columns, olive trees and lavender, Gomgom and Kong walking along a stone path toward $OWL, who waves a wing in welcome"
IMG[03]="medium side view of a simple rustic wooden table under a shady olive tree, a round crusty bread loaf and a clay water jug on the table, $OWL breaking the bread and sharing a piece with Gomgom, Kong hopping across the table toward the crumbs"
IMG[04]="macro close up on a rustic wooden table of a tiny round clay pot with a lid, a felt owl wing lifting the lid to reveal soft white cheese inside, Kong leaning over the rim peeking in with wide curious eyes, Gomgom softly blurred in the background under an olive tree"
IMG[05]="medium wide shot of a small joyful feast under an olive tree with only a little clay cheese pot, a bread loaf and a water jug on the wooden table, $OWL and Gomgom gently clinking small clay cups, Kong dancing happily on the table, warm dappled sunlight and a few round paper lanterns hanging from the branches"
IMG[06]="front view of Gomgom climbing out of a huge heap of shiny ribbon-tied felt gift boxes and golden trinkets in a grand felt banquet hall, setting a tiny golden crown down on top of the pile, Kong popping its head out of one of the gift boxes"
IMG[07]="wide calm shot at dawn of a still misty lake in a felt forest, Gomgom sitting quietly on the end of a small wooden dock with its eyes gently closed, a perfect mirror reflection on the water, Kong sitting peacefully beside Gomgom, soft pink and gold morning sky"
IMG[08]="medium shot from outside a cottage window of Gomgom inside a cozy felt kitchen pulling open floral curtains to let the morning sunlight in, Kong fluttering onto the windowsill beside a small flower pot"
IMG[09]="close up at table height of Gomgom sitting at a small kitchen table tearing a warm round bread roll in half with gentle steam rising, Kong standing on the table looking up hopefully, sunlight streaming across the table, a little jam jar and a cup of milk"
IMG[10]="close up of Gomgom slowly chewing a bite of warm bread with its eyes happily closed and its mouth closed, savoring it, Kong beside Gomgom nibbling a tiny crumb held in its beak, soft morning light and cozy kitchen shelves blurred behind"
IMG[11]="wide shot of Gomgom sitting on a red checkered picnic blanket in a golden meadow at sunset with a wicker basket, a bread loaf and a tiny clay cheese pot, Kong hopping on the blanket, a cozy felt village with glowing windows in the distance"

for k in 01 02 03 04 05 06 07 08 09 10 11; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard; log "그림 생성 $k"
  id=$(create_job seedream_v5_lite --prompt "${IMG[$k]}, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 그림 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 그림 $k ($id)"
done

# ---------- 영상 ----------
declare -A MOV
MOV[02]="Gomgom and Kong walk toward Grandpa Owl, Grandpa Owl waves its wing warmly, Kong flutters ahead excitedly, the camera slowly glides along the path"
MOV[03]="Grandpa Owl breaks the bread and hands a piece to Gomgom, Kong hops across the table and pecks at the crumbs, gentle sideways camera slide"
MOV[04]="the lid slowly lifts to reveal the soft cheese, Kong leans in closer and its eyes light up, slow push in"
MOV[05]="Grandpa Owl and Gomgom gently clink their small cups, Kong dances and twirls on the table, the lanterns sway softly, the camera slowly circles"
MOV[06]="Gomgom climbs out of the pile of gifts and sets the crown down, Kong pops out of a box and shakes off a ribbon, the camera slowly pulls back"
MOV[07]="the lake stays perfectly still, a single leaf drifts down and makes a tiny ripple, Kong tilts its head and settles down beside Gomgom, very slow push in"
MOV[08]="Gomgom pulls the curtains open and sunlight pours in, Kong flutters onto the windowsill and fluffs its feathers, the camera slowly moves closer"
MOV[09]="Gomgom tears the warm bread roll and steam rises, it offers a crumb to Kong who hops up happily and takes it, slow push in"
MOV[10]="Gomgom chews slowly with its mouth closed and eyes happily closed, Kong nibbles its tiny crumb and bobs its head, the camera very slowly circles"
declare -A WAN
WAN[01]="the camera glides down along the long banquet table past the towering cakes toward Gomgom, Gomgom looks around at everything with a small puzzled expression and its mouth closed, Kong pecks the cherry off the cake and the cake wobbles"
WAN[11]="Gomgom stays seated calmly on the picnic blanket the whole time with a gentle closed-mouth smile and hands a piece of bread to Kong, Kong hops happily around the blanket, the camera slowly rises and pulls back to reveal the golden meadow and the glowing village"

for k in 02 03 04 05 06 07 08 09 10; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상(Seedance) $k"
  id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done
for k in 01 11; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상(Wan 5초) $k"
  id=$(create_job wan2_7 --prompt "${WAN[$k]}, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 5 --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done

log "잔액 $(balance)"
missing=0
for k in 01 02 03 04 05 06 07 08 09 10 11; do
  [ -s "clips/$k.mp4" ] || { log "누락 clips/$k.mp4"; missing=1; }
done
[ $missing -eq 0 ] && log "ALL DONE" || log "FINISHED WITH MISSING"
