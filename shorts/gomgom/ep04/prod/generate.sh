#!/usr/bin/env bash
# 곰곰한 마음 4화 — 13컷 전부 Seedance 1.5 (01~12 4초, 13 8초)
# 시즌1 소품 첫 등장: 01컷에서 콩이가 갈색 가방 + 코랄 하트 배지를 선물, 02컷부터 착용
# 규칙: 입은 벌려도 되지만 이빨 금지 / 만화풍 변신 금지 / 정적인 줌만 하는 컷 금지
# 이미 있는 파일은 건너뜀 → 중단 후 다시 실행하면 이어서 진행
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master_s1.png
LOG=gen.log
MIN_BALANCE=12

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small coral pink felt heart badge on its chest and a tiny brown felt satchel bag across its body; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head"
CHAR0="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, with nothing on its chest and no bag; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head"
BORI="Bori, a small white needle-felted rabbit with long soft ears, pale pink inner ears, round black bead eyes and a mint green knitted scarf"
OWL="Grandpa Owl, a kind old round grey-brown felt owl with a cream chest, fluffy white eyebrows and small round spectacles, wearing a mustard knitted cardigan"
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

mkdir -p img clips

# ---------- 시작 그림 ----------
declare -A IMG
IMG[01]="low angle morning shot inside a cozy felt bedroom with a round window, Kong flying in holding a tiny brown felt satchel bag and a small coral pink felt heart badge, Gomgom sitting on a knitted rug with both paws reaching out in delight, sunbeams and floating dust sparkles"
IMG[02]="high angle shot of a small felt garden mailbox, Gomgom lifting the lid while a cluster of tiny glowing framed photographs of animal friends floats out into the air like fireflies, Kong fluttering among the floating photos, morning light"
IMG[03]="wide low angle shot from the floor, Gomgom standing very small at the base of a tall leaning tower of glowing golden photo frames that rises high above it, looking up with a slightly shrinking posture, Kong perched on the lowest frame, soft blue evening shadows and warm glow"
IMG[04]="medium shot of a cozy felt study with shelves of small blank-spined books and a woolen armchair, OWLDESC standing beside a large board made of colored yarn lines and felt circles, one wing raised in explanation, Gomgom and Kong sitting on a small stool listening"
IMG[05]="side view of a big felt tree trunk used as a height chart with small carved notches, Gomgom standing straight against the trunk while OWLDESC measures it with a ribbon tape, Kong standing on top of the bear head stretching upward to look taller, a queue of tiny felt animals waiting behind"
IMG[06]="close up of a glowing golden photo frame on a felt shelf showing BORIDESC beaming at her brightest moment holding a huge sunflower with confetti and sparkles around her, Kong hovering in front of the frame with wide shining eyes, Gomgom softly blurred behind"
IMG[07]="high angle shot of a very ordinary cozy afternoon in a small felt kitchen, laundry drying on a line, a half-drunk mug, crumbs and a wooden broom, Gomgom sweeping with a tired but gentle face, Kong hopping after the dust, flat soft daylight"
IMG[08]="medium shot of BORIDESC inside a bright floating photo frame in a sunny meadow, waving cheerfully with one paw, petals drifting, the frame edge glowing golden"
IMG[09]="wide shot revealing the world beyond the photo frame, the glowing frame at the left edge of the picture and outside it BORIDESC sitting in her messy cozy felt room with a laundry pile, stacked cups and a tipped over basket, soft late afternoon light"
IMG[10]="close up of BORIDESC wearing a knitted nightcap and yawning with her eyes squeezed shut and her mouth open, holding a warm mug, Gomgom and Kong peeking in from the side of the frame with surprised round eyes, cozy lamp light"
IMG[11]="medium shot at desk height of Gomgom sitting at a small wooden desk turning the page of a little blank felt notebook with a stubby pencil, a tiny calendar with blank squares on the wall, Kong hopping across the desk, warm lamp glow and evening window"
IMG[12]="side view of a wooden door frame with two small notches carved at different heights, Gomgom standing tall against it measuring itself with one paw flat on top of its head, Kong pointing a wing at the lower notch, warm orange evening light through the window"
IMG[13]="wide shot from behind of Gomgom and Kong sitting together on a small grassy hill at sunset looking over a handmade felt village with tiny glowing windows, long soft shadows, first stars appearing in a pink and gold sky"

for k in 01 02 03 04 05 06 07 08 09 10 11 12 13; do
  f="img/$k.png"
  [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  guard; log "그림 생성 $k"
  C="$CHAR"
  [ "$k" = "01" ] && C="$CHAR0"
  case "$k" in 08|09) C="$BORI" ;; 10) C="$BORI; $CHAR" ;; 06) C="$BORI; $CHAR" ;; esac
  P="${IMG[$k]}"
  P="${P//OWLDESC/$OWL}"
  P="${P//BORIDESC/$BORI}"
  id=$(create_job seedream_v5_lite --prompt "$P, $C, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -z "$id" ] && { log "실패 그림 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 그림 $k ($id)"
done

# ---------- 영상 ----------
declare -A MOV
MOV[01]="Kong flies down and gently hangs the little brown satchel over the bear shoulder, then presses the coral heart badge onto its chest, Gomgom looks down at the badge and hugs it happily, the camera rises slowly from floor level to eye level"
MOV[02]="Gomgom lifts the mailbox lid and the glowing photos stream out and swirl into the sky, Kong chases them in a loop, the camera follows the photos upward and tilts up"
MOV[03]="the tower of glowing frames sways higher above the small bear, Gomgom pulls in its shoulders and steps back, Kong flutters up along the frames, the camera slowly rises along the tower"
MOV[04]="Grandpa Owl taps the yarn board with a wing and the yarn lines shift into a new pattern, Gomgom tilts its head, Kong hops onto the stool arm, the camera slides sideways around them"
MOV[05]="Grandpa Owl stretches the ribbon tape along the bear back and marks a notch, Kong stretches taller on the bear head and wobbles, the camera pushes in from a low angle and tilts up along the trunk"
MOV[06]="the sunflower photo sparkles brighter and confetti drifts inside the frame, Kong flutters closer and its reflection glows on the glass, the camera arcs around the frame"
MOV[07]="Gomgom sweeps the floor slowly and a sock slips off the laundry line onto its head, Kong hops after the rolling dust, the camera drifts down from a high angle to table height"
MOV[08]="Bori waves and gives a cheerful little hop inside the glowing frame, petals swirl past, the camera slowly pulls back from the frame"
MOV[09]="the camera keeps pulling back past the edge of the glowing frame to reveal the messy room around it, Bori slumps down onto a cushion beside the laundry pile"
MOV[10]="Bori yawns with her eyes shut and then rubs one eye, Gomgom and Kong lean further into the frame and exchange a knowing look, Kong bobs with silent laughter, the camera drifts sideways into the room"
MOV[11]="Gomgom turns the page of the notebook and taps the pencil thoughtfully, Kong hops onto the notebook and looks up, the camera swings from the side of the desk around to the front"
MOV[12]="Gomgom presses its paw flat on its head, steps away from the door frame to look at the new notch and bounces on its toes, Kong flies up to the higher notch, the camera pushes in from the side"
MOV13="seen from behind, Gomgom and Kong sit on the hill as the sunset deepens, Kong lifts off and flies in a wide circle over the glowing village and comes back to the bear shoulder, the camera rises slowly and pulls back to reveal the whole valley while the first stars brighten"

for k in 01 02 03 04 05 06 07 08 09 10 11 12; do
  f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k — 건너뜀"; continue; }
  guard; log "영상 $k (4초)"
  id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
  [ -z "$id" ] && { log "실패 영상 $k"; continue; }
  fetch "$id" "$f" && log "완료 $f" || log "다운로드 실패 영상 $k ($id)"
done
if [ ! -s clips/13.mp4 ] && [ -s img/13.png ]; then
  guard; log "영상 13 (8초)"
  id=$(create_job seedance1_5 --prompt "$MOV13, $VTAIL" --start-image "img/13.png" --aspect_ratio 9:16 --duration 8 --generate_audio false --resolution 720p) || true
  if [ -n "$id" ]; then
    fetch "$id" clips/13.mp4 && log "완료 clips/13.mp4" || log "다운로드 실패 영상 13 ($id)"
  fi
fi

log "잔액 $(balance)"
missing=0
for k in 01 02 03 04 05 06 07 08 09 10 11 12 13; do
  [ -s "clips/$k.mp4" ] || { log "누락 clips/$k.mp4"; missing=1; }
done
if [ $missing -eq 0 ]; then log "ALL DONE"; else log "FINISHED WITH MISSING"; fi
