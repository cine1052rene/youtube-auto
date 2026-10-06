#!/usr/bin/env bash
# 10/7 사용자 지적 수정: 4화 13(콩이 날개 큼) / 6화 03(날아갔다는데 뒤에 서 있음)
# (구) 10/6: 4화 05(부엉이 작음·빈 배경) / 6화 05·06·11(빈 배경) 07·11·12(콩이 큼) — 전부 새로 생성
# 사용: bash fix.sh img [키...]  (그림)   |  bash fix.sh vid [키...]  (영상, 그림 있는 컷만)
set -u
cd "$(dirname "$0")"
STAGE=${1:-img}
REF=../ref/gomgom_master_s1.png
LOG=fix.log
GOM="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small coral pink felt heart badge on its chest and a tiny brown felt satchel bag across its body"
KONG="Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head, Kong is tiny, its whole round body no bigger than Gomgom's head"
OWL="Grandpa Owl, a kind old round grey-brown felt owl with a cream chest, fluffy white eyebrows and small round spectacles, wearing a mustard knitted cardigan, Grandpa Owl is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big"
SIZE="scale rule: Gomgom is the size reference, a palm-sized needle-felted doll about three heads tall, Grandpa Owl is slightly taller than Gomgom, other animal friends are about as tall as Gomgom, Kong is always the smallest character with its round body only as big as Gomgom's head"
STYLE="richly detailed handmade miniature world filling the whole background with layered foreground, midground and background full of cute tiny handmade props, never a plain empty wall or empty backdrop, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
VTAIL="the bear mouth may open softly but no teeth are ever visible, every character keeps exactly the same needle-felted wool texture, proportions, colors, accessories and body size from the first frame to the last and never turns into a cartoon or 2D character, nobody grows or shrinks during the shot, Kong stays tiny, smooth cinematic camera motion with a clear change of viewpoint, warm cozy mood, soft warm light, no text"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
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
    log "생성 오류: $(echo "$out" | tr -d '\n' | head -c 250)"; echo ""; return 1
  done
  echo ""; return 1
}
fetch() {
  local url
  url=$(higgsfield generate wait "$1" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))" 2>/dev/null)
  [ -n "$url" ] && curl -s -o "$2" "$url" && [ -s "$2" ]
}

declare -A IMG MOV CH DUR
BACK=", seen from behind so the coral heart badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it, no badge or heart on the back"
# 4화 13 — 어제보다 조금 나아진 것, 하나 있나요? (8초 마무리)
IMG[e04_13]="wide shot from behind of Gomgom sitting on a small grassy hilltop at sunset looking over a handmade felt village with tiny glowing windows, tiny Kong perched on Gomgom's shoulder with its small wings folded neatly against its round body, Kong much smaller than Gomgom's head, a little wooden signpost, wildflowers, a tiny felt lantern and a small kite resting in the grass beside them, first stars appearing in a pink and gold sky$BACK"
MOV[e04_13]="seen from behind, Gomgom sits on the hill as the sunset deepens, tiny Kong on its shoulder snuggles against the bear ear and gives a tiny happy hop while keeping its small wings folded, Kong never flies and never spreads its wings, fireflies rise from the grass around them and the lantern glows, the camera rises slowly and pulls back to reveal the whole glowing valley while the first stars brighten, Kong stays tiny on the shoulder"
CH[e04_13]="$GOM; $KONG, Kong's wings are tiny stubby felt wings that stay folded"; DUR[e04_13]=8
# 6화 03 — 인사를 안 하고 날아가서,
IMG[e06_03]="low angle shot from behind and below Gomgom standing in its cottage garden, one paw half raised to wave and stopping in the air, looking up at a wide bright sky where tiny Kong is only a small yellow dot flying far away toward the distant hills, Kong already far away and very small in the sky, nobody else near Gomgom, a clothesline with tiny felt laundry, a wooden birdhouse on a post, sunflowers, a garden gate and the cottage roof framing the shot$BACK"
MOV[e06_03]="Gomgom's raised paw slowly lowers back down and its ears droop, it keeps looking up at the sky as the tiny yellow dot of Kong flies further away over the hills and disappears, the laundry on the clothesline flutters, the camera slowly moves from behind Gomgom around to its side profile, Kong never comes back into the garden"
CH[e06_03]="$GOM; Kong appears only as a tiny distant yellow dot in the sky"; DUR[e06_03]=4

mkdir -p img clips
KEYS="e04_13 e06_03"
[ $# -ge 2 ] && KEYS="${*:2}"
for k in $KEYS; do
  if [ "$STAGE" = img ]; then
    f="img/$k.png"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
    log "그림 $k"
    id=$(create_job seedream_v5_lite --prompt "${IMG[$k]}, ${CH[$k]}, $SIZE, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high) || true
    if [ -n "$id" ] && fetch "$id" "$f"; then log "완료 $f"; else log "실패 그림 $k"; fi
  else
    f="clips/$k.mp4"; [ -s "$f" ] && { log "건너뜀 $f"; continue; }
    [ -s "img/$k.png" ] || { log "그림 없음 $k"; continue; }
    log "영상 $k (${DUR[$k]}초)"
    id=$(create_job seedance1_5 --prompt "${MOV[$k]}, $SIZE, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration ${DUR[$k]} --generate_audio false --resolution 720p) || true
    if [ -n "$id" ] && fetch "$id" "$f"; then log "완료 $f"; else log "실패 영상 $k"; fi
  fi
done
log "끝($STAGE)"
