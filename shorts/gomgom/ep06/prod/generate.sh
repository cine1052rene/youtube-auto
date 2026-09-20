#!/usr/bin/env bash
# 곰곰한 마음 6화 「별일 아닌데 괜히 서운할 때」 — 12컷 전부 Seedance (01~11 4초, 12 8초)
# 규칙: 첫 컷은 훅 / 이빨 금지 / 만화풍 변신 금지 / 조연은 곰곰이와 같은 키, 콩이는 절반 / 정적인 줌만 금지
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
IMG[01]="medium shot of Gomgom sitting alone on a small wooden step of a felt cottage with its shoulders drooping and its gaze lowered, one paw resting on its knee, a single small grey cloud hovering right in front of its chest, warm late afternoon light and a quiet empty garden"
IMG[02]="low angle shot looking up at a bright blue sky, Kong flying away cheerfully with its wings spread wide, seen from below and behind, tiny felt rooftops at the bottom edge of the frame"
IMG[03]="side view of Gomgom standing in the garden with one paw half raised to wave goodbye and the wave stopping in the air, watching Kong shrink into the distance, its ears drooping slightly"
IMG[04]="high angle shot of Gomgom going through its day inside the cottage, watering a small felt plant with a tiny watering can while its head is turned toward the window, half kneaded dough and a wooden spoon left on the table, warm daylight across the floor"
IMG[05]="medium shot of Gomgom and OWLDESC sitting facing each other on two small round cushions at exactly the same height, a low wooden table with two tiny cups between them, Grandpa Owl leaning in kindly, warm lamp light"
IMG[06]="medium shot of a soft translucent felt thought bubble floating above Gomgom's head showing a simple picture of a small yellow bird waving, the bubble gently cracked in one place, Gomgom looking up at it, Grandpa Owl watching from the side"
IMG[07]="close side view of Gomgom sitting by the garden gate with its chin resting on its paws, looking down the empty path, the small grey cloud still near its chest, long soft shadows"
IMG[08]="wide shot from Kong's side of the story, Kong flying happily over a sunny felt meadow with a big seed held in its beak, completely unaware, flowers and tiny hills below, bright cheerful light"
IMG[09]="close shot of Kong landing on a wooden fence post with the big seed in its beak, wings still spread with excitement, the cottage visible small in the background"
IMG[10]="medium shot of Gomgom looking down at the small grey cloud in front of its chest and reaching out one paw toward it instead of turning away, Kong landing quietly on the step behind, soft golden light"
IMG[11]="close shot of the grey cloud shrinking to the size of a pebble in Gomgom's open paw while Gomgom looks at it calmly, Kong holding out the seed beside it, warm light"
IMG[12]="wide shot from behind of Gomgom and Kong sitting side by side on the cottage step at sunset, Kong nestled against Gomgom's arm, the tiny seed planted in a small pot in front of them, a handmade felt village with glowing windows beyond the garden"

for k in 01 02 03 04 05 06 07 08 09 10 11 12; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard; log "그림 생성 $k"
  P="${IMG[$k]}"
  P="${P//OWLDESC/$OWL}"
  C="$CHAR"
  case "$k" in 05|06) C="$CHAR; $OWL" ;; esac
  id=$(create_job seedream_v5_lite --prompt "$P, $C, $SIZE, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 그림 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 그림 $k ($id)"
done

# ---------- 영상 ----------
declare -A MOV
MOV[01]="Gomgom lets out a small sigh with its mouth closed and its shoulders sink further, the little grey cloud drifts closer to its chest, a leaf falls past, the camera slowly pushes in from the side and settles at eye level"
MOV[02]="Kong beats its wings and climbs higher into the blue sky, growing smaller as it goes, the camera tilts up and follows it until the rooftops leave the frame"
MOV[03]="Gomgom's raised paw slowly lowers back down and its ears droop, it keeps watching the empty sky, the camera moves from a side view around toward its back"
MOV[04]="Gomgom tips the watering can while still looking at the window and the water overflows a little, it blinks and looks down, Kong is nowhere in sight, the camera drifts down from a high angle to table height"
MOV[05]="Grandpa Owl speaks gently and tilts its head, Gomgom looks up and nods slowly, both staying exactly the same height, the camera arcs slowly around the low table"
MOV[06]="the thought bubble drifts and turns above Gomgom's head and the crack widens softly without breaking, Gomgom reaches a paw toward it, the camera rises along the bubble and tilts down to Gomgom"
MOV[07]="Gomgom shifts its chin on its paws and looks down the empty path, a breeze moves the grass, the small grey cloud bobs, the camera slides sideways past the gate"
MOV[08]="Kong flies across the sunny meadow with the seed in its beak, dipping and rising happily, flowers sway below, the camera tracks alongside Kong"
MOV[09]="Kong lands on the fence post and folds its wings, looking around brightly for Gomgom, the camera pushes in and the cottage in the background comes into focus"
MOV[10]="Gomgom reaches toward the small grey cloud and cups it in its paw, turning it gently to look at it, Kong lands softly on the step behind and tilts its head, the camera moves from behind Gomgom around to its side"
MOV[11]="the grey cloud shrinks down to a pebble in Gomgom's paw and fades, Kong holds out the seed and hops closer, Gomgom's ears lift again, the camera pushes in on the two paws meeting"
MOV12="seen from behind, Gomgom and Kong sit together on the step as the sunset deepens, Kong nestles closer against Gomgom's arm and Gomgom rests a paw beside it, a few fireflies rise around the little planted pot, the camera rises slowly and pulls back to reveal the glowing village beyond the garden"

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
if [ $missing -eq 0 ]; then log "EP06 ALL DONE"; else log "EP06 FINISHED WITH MISSING"; fi
