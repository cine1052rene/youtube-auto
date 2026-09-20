#!/usr/bin/env bash
# 곰곰한 마음 5화 「걱정을 내려놓고 싶을 때」 — 12컷 전부 Seedance (01~11 4초, 12 8초)
# 규칙: 첫 컷은 훅 / 이빨 금지 / 만화풍 변신 금지 / 조연은 곰곰이와 같은 키, 콩이는 절반 / 정적인 줌만 금지
# 이미 있는 파일은 건너뜀 → 중단 후 다시 실행하면 이어서 진행
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master_s1.png
LOG=gen.log
MIN_BALANCE=12

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small coral pink felt heart badge on its chest and a tiny brown felt satchel bag across its body; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head"
OWL="Grandpa Owl, a kind old round grey-brown felt owl with a cream chest, fluffy white eyebrows and small round spectacles, wearing a mustard knitted cardigan, Grandpa Owl stands exactly as tall as Gomgom and is never taller or bulkier than Gomgom"
SIZE="scale rule: Gomgom is the size reference, a palm-sized needle-felted doll about three heads tall, every other animal character stands exactly as tall as Gomgom and is never taller, never shorter and never bulkier, Kong is always the smallest character with its round body only as big as Gomgom's head and about half of Gomgom's total height"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
VTAIL="Kong is lively and expressive, the bear mouth may open softly but no teeth are ever visible, every character keeps exactly the same needle-felted wool texture, proportions, colors, accessories and body size from the first frame to the last and never turns into a cartoon or 2D character, nobody grows or shrinks during the shot, smooth cinematic camera motion with a clear change of viewpoint, warm cozy mood, soft warm light, no text"

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

mkdir -p img clips

# ---------- 시작 그림 ----------
declare -A IMG
IMG[01]="high angle night shot of a cozy felt bedroom, Gomgom lying awake in a small wooden bed with the blanket pulled up, a long chain of small grey worry clouds linked one after another floating above its head and curling around the room, Kong sitting on the pillow looking up at the clouds, soft blue moonlight with a warm lamp glow"
IMG[02]="close side view of Gomgom rolling over in bed with wide open round eyes, the grey worry clouds still drifting above, Kong flopped upside down beside the pillow with its eyes also wide open, cozy knitted blanket and a tiny felt moon lamp"
IMG[03]="medium shot at dawn of a small felt stone terrace with olive trees and low white columns, OWLDESC standing beside Gomgom at exactly the same height and gesturing gently, Kong perched on a low column, soft pink morning light"
IMG[04]="medium shot of two woven felt baskets side by side on the stone terrace, one basket with a warm honey colored ribbon and one with a cool grey ribbon, Grandpa Owl setting them down while Gomgom watches, Kong hopping between the two baskets"
IMG[05]="close top down shot of the honey ribboned basket, small felt objects being placed inside it, a tiny yellow umbrella, a seed packet and a wool ball, Gomgom's paws lowering the umbrella in, Kong peeking over the rim"
IMG[06]="close top down shot of the grey ribboned basket holding soft floating things, a small grey rain cloud, a gust of wind swirl and a tiny weather vane, Kong tilting its head at the cloud, Gomgom watching from the side"
IMG[07]="side view of Gomgom standing at a round cottage window looking up at a heavy grey sky outside, small worry clouds gathering above its head again, Kong on the windowsill following its gaze, warm indoor lamp light against the cold blue outside"
IMG[08]="close shot of Gomgom taking a small yellow felt umbrella down from a wooden hook by the door and tucking it under its arm, Kong fluttering beside the hook, warm hallway light"
IMG[09]="medium shot of Gomgom placing the yellow umbrella into the honey ribboned basket with a relieved gentle expression, Kong landing on the basket rim, the grey basket sitting a little apart"
IMG[10]="low angle shot of Gomgom holding the heavy grey ribboned basket with both paws, the basket stuffed full of grey clouds and pressing it down, Kong flying around trying to lift a corner, soft evening light"
IMG[11]="medium wide shot of Gomgom setting the grey basket down on the grass and stepping back, the grey clouds lifting out of the basket and floating up into the sky turning soft pink, Kong spiralling upward with them, the sky clearing"
IMG[12]="wide shot from behind of Gomgom and Kong sitting on a small grassy hill under a clear night sky full of stars, the empty grey basket resting beside them, a handmade felt village with tiny glowing windows below, calm and peaceful"

for k in 01 02 03 04 05 06 07 08 09 10 11 12; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard; log "그림 생성 $k"
  P="${IMG[$k]}"
  P="${P//OWLDESC/$OWL}"
  C="$CHAR"
  case "$k" in 03|04) C="$CHAR; $OWL" ;; esac
  id=$(create_job seedream_v5_lite --prompt "$P, $C, $SIZE, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 그림 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 그림 $k ($id)"
done

# ---------- 영상 ----------
declare -A MOV
MOV[01]="the chain of worry clouds keeps growing and slowly circles the room, Gomgom's eyes follow them and it pulls the blanket higher, Kong turns its head to track one cloud, the camera drifts down from the ceiling to the bed"
MOV[02]="Gomgom rolls over restlessly and sighs with its mouth closed, Kong flips upright and flops down again, the clouds drift past, the camera slides slowly along the bed"
MOV[03]="Grandpa Owl gestures with a wing and Gomgom steps closer, both staying exactly the same height, Kong hops along the column, the camera moves sideways around them as the morning light warms"
MOV[04]="Grandpa Owl sets the two baskets down and nudges them apart, Gomgom leans in to look, Kong hops from one basket into the other, the camera pushes in from above and tilts down"
MOV[05]="the small umbrella, the seed packet and the wool ball drop one by one into the honey basket, Kong pokes the wool ball with its beak, the camera slowly circles above the basket"
MOV[06]="the little grey cloud puffs and drifts inside the basket, the wind swirl spins, Kong flutters back in surprise, the camera arcs low around the basket"
MOV[07]="dark clouds roll across the sky outside the window while worry clouds gather over Gomgom's head, Gomgom's shoulders sink, Kong presses closer to the glass, the camera pulls back from the window into the room"
MOV[08]="Gomgom lifts the yellow umbrella off the hook and tucks it under its arm with a small determined nod, Kong flies a happy loop around it, the camera follows the umbrella upward"
MOV[09]="Gomgom lowers the umbrella into the honey basket and pats it once, its shoulders relaxing, Kong lands on the rim and bobs, the camera moves from a side angle to the front"
MOV[10]="Gomgom struggles under the heavy grey basket and sways, Kong tugs at a corner with its beak and flaps hard, the camera rises from a low angle to show how full the basket is"
MOV[11]="Gomgom sets the basket down and steps back, the grey clouds float up out of it and rise into the clearing sky, Kong spirals upward following them, the camera tilts up with the clouds as the sky turns pink"
MOV12="seen from behind, Gomgom and Kong sit still on the hill while the last clouds drift away and stars brighten one by one across the sky, Kong leans against Gomgom's side, the camera rises slowly and pulls back to reveal the whole calm valley"

for k in 01 02 03 04 05 06 07 08 09 10 11; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상 $k (4초)"
  id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $SIZE, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done
if [ ! -s clips/12.mp4 ] && [ -s img/12.png ]; then
  guard; log "영상 12 (8초)"
  id=$(create_job seedance1_5 --prompt "$MOV12, $SIZE, $VTAIL" --start-image "img/12.png" --aspect_ratio 9:16 --duration 8 --generate_audio false --resolution 720p) || true
  if [ -n "$id" ]; then
    fetch "$id" clips/12.mp4 && log "완료 clips/12.mp4" || log "다운로드 실패 영상 12 ($id)"
  fi
fi

log "잔액 $(balance)"
missing=0
for k in 01 02 03 04 05 06 07 08 09 10 11 12; do
  [ -s "clips/$k.mp4" ] || { log "누락 clips/$k.mp4"; missing=1; }
done
if [ $missing -eq 0 ]; then log "EP05 ALL DONE"; else log "EP05 FINISHED WITH MISSING"; fi
