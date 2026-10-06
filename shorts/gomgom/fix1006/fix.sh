#!/usr/bin/env bash
# 10/6 사용자 지적 수정: 4화 05(부엉이 작음·빈 배경) / 6화 05·06·11(빈 배경) 07·11·12(콩이 큼) — 전부 새로 생성
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
# 4화 05 — 사람은 늘 남과 견주어 자신을 가늠한다고 했어요.
IMG[e04_05]="low side angle shot in a sunny felt forest clearing turned into a little playground, a big felt tree trunk used as a height chart with carved notches and tiny painted marks, Gomgom standing straight with its back against the trunk while Grandpa Owl, standing upright beside it and slightly taller than Gomgom, stretches a ribbon tape measure along the bear back, Kong perched on top of Gomgom's head stretching up on tiptoe to look taller, a queue of tiny felt animal friends waiting their turn, felt mushrooms, a little wooden sign post, bunting flags strung between branches, flower patches and a tiny wooden bench"
MOV[e04_05]="Grandpa Owl stretches the ribbon tape along the bear back and marks a notch, staying slightly taller than Gomgom the whole time, Kong stretches up on the bear head and wobbles, the bunting flutters, the camera pushes in from a low angle and tilts up along the trunk"
CH[e04_05]="$GOM; $KONG; $OWL"; DUR[e04_05]=4
# 6화 05 — 서운함은 사실,
IMG[e06_05]="high three-quarter angle shot inside Grandpa Owl's cozy treehouse library, Gomgom and Grandpa Owl sitting facing each other on two round knitted cushions at a low wooden table, Grandpa Owl slightly taller than Gomgom even while sitting, a teapot wearing a tiny knitted cozy and two little cups on the table, a round window with a forest view, curved shelves full of tiny books and jars, bundles of dried flowers hanging from the wooden beams, a warm string of tiny lights, a sleepy felt cat on a shelf, warm lamp light"
MOV[e06_05]="Grandpa Owl speaks gently and tilts its head, Gomgom looks up from its cup and listens, steam curls up from the teapot, the camera arcs slowly around the low table from high to eye level, Grandpa Owl stays slightly taller than Gomgom"
CH[e06_05]="$GOM; $OWL; Kong is not in this scene"; DUR[e06_05]=4
# 6화 06 — 말하지 않은 기대가 어긋났다는 신호래요.
IMG[e06_06]="low angle shot from the wooden floor of the same cozy treehouse library looking up, a soft translucent felt thought bubble floating above Gomgom's head showing a tiny picture of a small yellow chick waving goodbye, the bubble gently cracked in one place, Gomgom looking up at it, Grandpa Owl standing beside Gomgom slightly taller than it with one wing on Gomgom's shoulder, small hanging paper lanterns, a ladder to a loft, shelves with tiny books, potted plants and a felt wall clock behind them"
MOV[e06_06]="the thought bubble slowly turns above Gomgom's head and the crack widens softly without breaking, Gomgom reaches one paw up toward it, Grandpa Owl pats its shoulder, the lanterns sway, the camera rises from the floor along the bubble and tilts down to the two of them"
CH[e06_06]="$GOM; $OWL; Kong is not in this scene"; DUR[e06_06]=4
# 6화 07 — 곰곰이는 인사를 기다리고 있었거든요.
IMG[e06_07]="over-the-shoulder shot from behind Gomgom sitting alone on a tiny wooden stool by its garden gate, the gate wrapped in blooming felt morning glories, a little red mailbox and a small glowing lantern on the gate post, looking down a long empty winding path lined with flowers toward a distant felt village, the small grey cloud floating near its shoulder, long soft afternoon shadows, Gomgom is completely alone, seen from behind so the coral heart badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it, no badge or heart on the back"
MOV[e06_07]="Gomgom shifts on its stool and leans forward to look down the empty path, a breeze moves the flowers and the morning glories, the little grey cloud bobs beside it, the camera slides sideways from behind Gomgom to its profile, nobody comes down the path"
CH[e06_07]="$GOM; Kong is not in this scene, Gomgom is alone"; DUR[e06_07]=4
# 6화 11 — 내가 뭘 기대했는지 먼저 살펴보세요.
IMG[e06_11]="medium shot at bench height, Gomgom sitting on a little wooden bench in its sunset cottage garden holding a tiny grey felt cloud the size of a pebble in its open paw and looking at it calmly, tiny Kong perched on Gomgom's shoulder holding a small seed in its beak, Kong much smaller than Gomgom's head and sitting behind the bear head line, flower beds, a small watering can, a tiny vegetable patch with felt carrots, bunting flags and the cottage window glowing behind them"
MOV[e06_11]="the little grey cloud in Gomgom's paw slowly shrinks smaller and smaller until it is gone, leaving the paw empty, tiny Kong on Gomgom's shoulder leans down and drops the seed into the empty paw, Gomgom smiles softly with its mouth closed, the camera slowly arcs sideways around the bench at the same distance without pushing in, Kong stays tiny on the shoulder"
CH[e06_11]="$GOM; $KONG"; DUR[e06_11]=4
# 6화 12 — 최근에 서운했던 일, 사실은 뭘 기대했었나요?
IMG[e06_12]="wide shot from behind of Gomgom sitting on the cottage step at sunset, tiny Kong perched on Gomgom's shoulder nestled against its ear, Kong much smaller than Gomgom's head, a tiny seedling planted in a small clay pot on the step in front of them, a watering can and a little lantern beside the pot, a handmade felt village with glowing windows beyond the garden fence, pink and golden sunset sky, seen from behind so the coral heart badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it, no badge or heart on the back"
MOV[e06_12]="seen from behind, Gomgom sits on the step as the sunset deepens, tiny Kong on its shoulder nestles against its ear, a few fireflies rise around the little planted pot and the lantern glows, the camera rises slowly and pulls back to reveal the glowing village beyond the garden, Kong stays tiny on Gomgom's shoulder"
CH[e06_12]="$GOM; $KONG"; DUR[e06_12]=8

mkdir -p img clips
KEYS="e04_05 e06_05 e06_06 e06_07 e06_11 e06_12"
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
