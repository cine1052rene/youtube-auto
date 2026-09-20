#!/usr/bin/env bash
# 4화 캐릭터 크기 보정 — 04·05(부엉이), 09·10(보리), 13(콩이)
# 기준: 곰곰이 = 크기 기준. 조연(보리·부엉이)은 곰곰이와 똑같은 키.
#       콩이는 항상 제일 작고, 몸통이 곰곰이 머리 크기 = 곰곰이 키의 절반.
set -u
cd "$(dirname "$0")"
REF=../../ref/gomgom_master_s1.png
LOG=fix_size.log
MIN_BALANCE=12

CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small coral pink felt heart badge on its chest and a tiny brown felt satchel bag across its body; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head"
BORI="Bori, a small white needle-felted rabbit with long soft ears, pale pink inner ears, round black bead eyes and a mint green knitted scarf, Bori stands exactly as tall as Gomgom and is never taller or bulkier than Gomgom"
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

mkdir -p img_reject
for k in 04 05 09 10 13; do
  [ -s "img/$k.png" ] && [ ! -s "img_reject/${k}_size_old.png" ] && cp "img/$k.png" "img_reject/${k}_size_old.png"
  [ -s "clips/$k.mp4" ] && [ ! -s "clips/${k}_size_old.mp4" ] && cp "clips/$k.mp4" "clips/${k}_size_old.mp4"
done

declare -A IMG
declare -A MOV
declare -A WHO

WHO[04]="$OWL"
IMG[04]="medium shot of a cozy felt study with shelves of small blank-spined books and a woolen armchair, Grandpa Owl standing on the floor right beside Gomgom at exactly the same height as Gomgom, one wing raised toward a large board made of colored yarn lines and felt circles, Gomgom standing next to the owl shoulder to shoulder and Kong perched on a small wooden stool beside them"
MOV[04]="Grandpa Owl taps the yarn board with a wing and the yarn lines shift into a new pattern, Gomgom tilts its head and steps closer, Kong hops along the stool, the camera slides sideways around the two of them while they stay the same height as each other"

WHO[05]="$OWL"
IMG[05]="side view of a big felt tree trunk used as a height chart with small carved notches, Gomgom standing straight with its back against the trunk while Grandpa Owl, who is exactly the same height as Gomgom, stretches a ribbon tape along the bear back, Kong standing on top of the bear head stretching upward to look taller, a queue of tiny felt animals waiting behind"
MOV[05]="Grandpa Owl stretches the ribbon tape along the bear back and marks a notch while both of them stay exactly the same height, Kong stretches taller on the bear head and wobbles, the camera pushes in from a low angle and tilts up along the trunk"

WHO[09]="$BORI"
IMG[09]="wide shot of a cozy messy felt room, a glowing empty photo frame on the wall, Bori sitting on the floor beside a laundry pile and stacked cups, Gomgom sitting right next to Bori at exactly the same height so their heads are level, Kong standing in front of them and reaching only up to their chests, soft late afternoon light"
MOV[09]="the camera pulls back from the glowing frame to reveal the whole messy room, Bori slumps down onto a cushion and Gomgom leans toward her, both staying exactly the same height, Kong hops between them"

WHO[10]="$BORI"
IMG[10]="close up of Bori wearing a knitted nightcap and yawning with her eyes squeezed shut and her mouth open without any teeth showing, holding a warm mug, Gomgom standing right beside her at exactly the same height with their heads level, Kong standing on the table between them reaching only up to their chests, cozy lamp light"
MOV[10]="Bori yawns and then rubs one eye with a paw, Gomgom beside her mirrors the sleepy look and both stay exactly the same height, Kong bobs up and down with silent laughter, the camera drifts sideways into the room"

WHO[13]="$CHAR"
IMG[13]="wide shot from behind of Gomgom sitting on a small grassy hill at sunset looking over a handmade felt village with tiny glowing windows, Kong sitting right beside Gomgom and reaching only up to the bear shoulder because Kong is only half of Gomgom's height, long soft shadows, first stars appearing in a pink and gold sky"
MOV[13]="seen from behind, Kong lifts off and flies in a wide circle over the glowing village and comes back to land beside Gomgom, Kong stays tiny and the same size the whole time, the camera rises slowly and pulls back to reveal the whole valley while the first stars brighten"

for k in 04 05 09 10 13; do
  guard; log "그림 $k 재생성"
  C="$CHAR"
  [ "$k" = "13" ] || C="$CHAR; ${WHO[$k]}"
  id=$(create_job seedream_v5_lite --prompt "${IMG[$k]}, $C, $SIZE, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
  [ -n "$id" ] && { fetch "$id" "img/$k.png" && log "완료 img/$k.png" || log "다운로드 실패 그림 $k"; }
done

for k in 04 05 09 10; do
  [ -s "img/$k.png" ] || { log "시작 그림 없음 $k"; continue; }
  guard; log "영상 $k 재생성 (4초)"
  id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $SIZE, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration 4 --generate_audio false --resolution 720p) || true
  [ -n "$id" ] && { fetch "$id" "clips/$k.mp4" && log "완료 clips/$k.mp4" || log "다운로드 실패 영상 $k"; }
done

if [ -s img/13.png ]; then
  guard; log "영상 13 재생성 (8초)"
  id=$(create_job seedance1_5 --prompt "${MOV[13]}, $SIZE, $VTAIL" --start-image "img/13.png" --aspect_ratio 9:16 --duration 8 --generate_audio false --resolution 720p) || true
  [ -n "$id" ] && { fetch "$id" clips/13.mp4 && log "완료 clips/13.mp4" || log "다운로드 실패 영상 13"; }
fi

log "잔액 $(balance)"
log "SIZE FIX DONE"
