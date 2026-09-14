#!/usr/bin/env bash
# 곰곰한 마음 2화 — 13컷 전부 영상 (Seedance 1.5 기본 + 01·10·13 Wan 2.7)
# 이미 있는 파일은 건너뜀 → 중단 후 다시 실행해도 이어서 진행
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master.png
LOG=gen.log
MIN_BALANCE=15

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile; Kong, a tiny round yellow felt baby chick with a small orange beak"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
VTAIL="Kong is lively and expressive, both characters keep exactly the same appearance and stay cute with bright open eyes, smooth cinematic camera motion, warm cozy mood, soft warm light, no text"

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
IMG[01]="wide low angle shot of a cozy handmade felt town plaza in golden afternoon light, Gomgom standing in the middle surrounded by many small glowing pink felt hearts floating in the air, one tiny grey felt raincloud hovering just above Gomgom's head, Kong perched on Gomgom's shoulder looking up at the little cloud, felt shops with striped awnings and flower boxes around the plaza"
IMG[02]="medium low angle shot of Gomgom standing on a small wooden stage in a cozy felt community hall with wooden beams and warm hanging lamps, little pink felt heart confetti drifting down, Kong tossing heart confetti from a tiny woven basket, small soft felt animal friends clapping in the blurred foreground"
IMG[03]="close up side view of Gomgom's face as a tiny grey felt raincloud drifts down in front of it, Gomgom's smile fading into a small surprised look, a few pink felt hearts still floating in the warm blurred background, Kong peeking out from behind Gomgom's ear"
IMG[04]="top down overhead view of a cozy felt bedroom at night lit by a warm little nightlight, Gomgom lying awake in bed under a colorful patchwork quilt, the tiny grey felt raincloud circling above its head, Kong in a tiny knitted nest on the nightstand peeking over the edge, soft moonlight through a round window"
IMG[05]="low three quarter view of Gomgom and Kong standing beside a large handmade wooden balance scale in a cozy felt workshop, one pan piled with many small pink felt hearts and the other pan holding a single tiny grey felt raincloud, the cloud side hanging much lower, spools of yarn, little tools and warm lamps in the background"
IMG[06]="wide shot through big felt fern leaves in the foreground of a lush handmade felt prehistoric jungle with giant felt mushrooms and a gentle felt volcano far away, Gomgom wearing a tiny leaf cape standing alert with ears perked up, Kong on a branch above acting as a lookout, bright and playful not scary"
IMG[07]="side view of Gomgom and Kong peeking out safely from behind a big mossy felt rock in the felt jungle, a big round friendly-looking felt dinosaur strolling past in the soft background, Gomgom looking relieved, bright and playful not scary"
IMG[08]="macro close up of Gomgom sitting on a knitted rug holding the tiny grey felt raincloud gently in both paws and examining it curiously, Kong leaning in close to look at it too, warm lamplight and bookshelves softly blurred behind"
IMG[09]="low front view of Gomgom standing tall on a knitted rug making a cute brave pose with one tiny arm raised like a strong hero, Kong beside it copying the pose with one wing raised, warm cozy room with plants and a sunny window behind"
IMG[10]="medium shot of Gomgom hugging the tiny grey felt raincloud close to its chest in a cozy sunlit room, Kong flying toward them with tiny wings spread, warm golden light through a big window, plants and string lights around"
IMG[11]="close up at table height of Gomgom placing a small glowing yellow felt star into a clear glass jar that already holds one star, Kong holding a third glowing star in its beak on the wooden table, cozy desk with a little lamp and balls of yarn"
IMG[12]="front view of the handmade wooden balance scale in the felt workshop now perfectly level, one pan holding a glass jar of three glowing felt stars and the other pan holding a small white fluffy felt cloud, Gomgom and Kong standing beside the scale smiling"
IMG[13]="wide shot from behind of Gomgom and Kong sitting on a grassy felt hilltop at golden sunset overlooking a cozy felt town with glowing windows, an open glass jar of glowing felt stars in Gomgom's paws"

for k in 01 02 03 04 05 06 07 08 09 10 11 12 13; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard; log "그림 생성 $k"
  id=$(create_job seedream_v5_lite --prompt "${IMG[$k]}, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 그림 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 그림 $k ($id)"
done

# ---------- 영상 ----------
declare -A MOV
MOV[02]="heart confetti gently falls, Gomgom smiles shyly and waves, Kong tosses more heart confetti happily from its basket, the camera slowly rises"
MOV[03]="the little grey cloud slowly drifts closer to Gomgom, Gomgom blinks, Kong leans out from behind the ear and stares at the cloud with wide eyes, slow push in"
MOV[04]="the little grey cloud slowly circles above Gomgom's head, Gomgom turns over under the quilt, Kong hops out of its nest onto the pillow, the camera slowly rotates overhead"
MOV[05]="the scale tips further toward the grey cloud side, Gomgom tilts its head in surprise, Kong hops onto the heart side and bounces trying to balance it, the camera slowly orbits"
MOV[06]="Gomgom's ears twitch and it looks around alertly, Kong stretches up tall on the branch and points with a wing, the ferns sway, the camera slowly moves through the ferns"
MOV[07]="the friendly felt dinosaur strolls away in the background, Gomgom lets out a relieved breath, Kong wipes its brow with a wing and hops, gentle sideways camera slide"
MOV[08]="Gomgom gently turns the little cloud in its paws, the cloud makes a tiny drizzle, Kong leans in, gets a drop on its beak and shakes its head, slow push in"
MOV[09]="Gomgom puffs up its chest proudly, Kong mimics and puffs up its feathers, both nod together, the camera slowly rises"
MOV[11]="Gomgom drops the star into the jar and it lights up, Kong hops over and drops the third star in, all three stars glow warmly, the camera slowly pushes in"
MOV[12]="the scale gently wobbles and settles perfectly level, Gomgom claps its paws happily, Kong does a little dance beside the scale, slow camera pull back"
declare -A WAN
WAN[01]="the camera moves in toward Gomgom, the pink hearts gently drift up and fade away while the little grey cloud stays above Gomgom's head, Kong flaps up and pecks at the grey cloud"
WAN[10]="Gomgom hugs the little cloud gently and it slowly turns fluffy white and glows warmly, Kong flies in and snuggles into the hug, the camera circles around them"
WAN[13]="Gomgom opens the jar and the glowing stars float up into the sunset sky, Kong flies up among the stars, Gomgom turns and waves, the camera slowly rises and pulls back to reveal the whole glowing town"
declare -A WANDUR=( [01]=5 [10]=5 [13]=5 )

for k in 02 03 04 05 06 07 08 09 11 12; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상(Seedance) $k"
  id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done
for k in 01 10 13; do
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
