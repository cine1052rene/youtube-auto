#!/usr/bin/env bash
# 시즌2 에피소드 생성(그림→영상). 사용: bash generate.sh img|vid [키...]
# (구) 10/6: 4화 05(부엉이 작음·빈 배경) / 6화 05·06·11(빈 배경) 07·11·12(콩이 큼) — 전부 새로 생성
# 사용: bash fix.sh img [키...]  (그림)   |  bash fix.sh vid [키...]  (영상, 그림 있는 컷만)
set -u
cd "$(dirname "$0")"
STAGE=${1:-img}
REF=../../ref/gomgom_master_s2c.png
LOG=fix.log
GOM="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small matte yellow felt star badge on its chest with no glow and no plastic shine and a tiny brown felt satchel bag across its body"
KONG="Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head, Kong is tiny, exactly as small as in the reference image, Kong's whole body is exactly one third the width of Gomgom's head, Kong never grows or shrinks and is never as big as Gomgom's head, Kong keeps its pink blush cheeks, round yellow face and small orange beak"
OWL="Grandpa Owl, a kind old round grey-brown felt owl with a cream chest, fluffy white eyebrows and small round spectacles, wearing a mustard knitted cardigan, Grandpa Owl is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big"
FRIENDS="small felt animal friends such as a rabbit, a squirrel and a hedgehog, each about as tall as Gomgom"
SIZE="scale rule: Gomgom is the size reference, a palm-sized needle-felted doll about three heads tall, Grandpa Owl is slightly taller than Gomgom, other animal friends are about as tall as Gomgom, Kong is always the smallest character, Kong's whole body is exactly one third the width of Gomgom's head in every shot, even when Kong is close to the camera or far away, in wide shots Kong is still clearly visible"
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
IMG[01]="close eye level shot of Gomgom standing in front of a tall wooden shelf packed with many rows of little glass honey jars of many different golden colors, each jar with a cloth lid tied with string and no labels or letters, Gomgom's mouth softly open in amazement with no teeth and eyes wide, warm shop lights"
MOV[01]="Gomgom's eyes move up and down the rows of honey jars and its head tilts from side to side, the camera slides sideways along the long shelf toward Gomgom"
CH[01]="$GOM; Kong is not in this scene"; DUR[01]=4
IMG[02]="dramatic low worm's-eye angle from the honey shop floor looking up at a towering wall of honey jar shelves rising all the way to a high vaulted wooden ceiling with a round skylight, warm golden light glowing through hundreds of amber and gold jars with no labels, a rolling library ladder, hanging dried flowers and a felt bee mobile, Gomgom standing small at the bottom with its head tilted far back gazing up in awe, tiny Kong sitting at the very top center of Gomgom's head between its ears"
MOV[02]="Gomgom stands still in the same spot in the center of the frame and slowly lifts its head to gaze up at the towering shelves in awe with its mouth closed, exactly one small mouth, tiny Kong on its head looks up too, light glints across the jars, the camera stays low near the floor at the same height and slowly arcs halfway around Gomgom, it never rises and never tilts up, Gomgom stays fully visible in the center of the frame from start to end, Kong stays tiny"
CH[02]="$GOM; $KONG"; DUR[02]=4
IMG[03]="medium three-quarter shot of Gomgom in the honey shop holding one small honey jar in each paw, looking back and forth between them with a thoughtful frown, shelves of honey jars behind, a wicker shopping basket on the floor, warm light"
MOV[03]="Gomgom lifts the left jar, then the right jar, looks back and forth and tilts its head unable to decide, the camera circles slowly around Gomgom"
CH[03]="$GOM; Kong is not in this scene"; DUR[03]=4
IMG[04]="medium shot of an outdoor felt village market stall, Grandpa Owl slightly taller than Gomgom standing behind a tasting table setting out small tasting spoons in front of little jam jars with no labels, a striped awning and bunting overhead, a few small felt animal friends such as a squirrel and a hedgehog, each about as tall as Gomgom, walking up to the table, baskets of fruit"
MOV[04]="Grandpa Owl places tiny tasting spoons one by one in front of the jam jars with its wing, the animal friends walk up to the table, the bunting flutters, the camera glides sideways at table height"
CH[04]="$OWL; Gomgom and Kong are not in this scene"; DUR[04]=4
IMG[05]="spectacular high aerial view over a festive felt village market square, colorful striped awnings, strings of bunting flags and paper lanterns crisscrossing above, a fountain in the middle, and one very long tasting table crowded with twenty-four little jam jars in rainbow colors with no labels, many small felt animal friends such as squirrels, hedgehogs, foxes and sheep, each about as tall as Gomgom, crowding around it with empty shopping baskets, cobblestone paths and flower carts all around"
MOV[05]="the animal friends taste from tiny spoons, look at each other, shrug and wander off without picking up any jar, their baskets stay empty, the bunting sways in the breeze, the camera glides slowly along above the long table from high in the air"
CH[05]="$FRIENDS; Gomgom and Kong are not in this scene"; DUR[05]=4
IMG[06]="medium shot of a short tasting table with only six little jam jars, a felt squirrel and a felt hedgehog, each about as tall as Gomgom, each happily putting one jam jar into their shopping basket, Grandpa Owl slightly taller than them smiling behind the table, bunting and baskets of fruit"
MOV[06]="the squirrel and the hedgehog each pick up one jam jar and put it into their basket with a happy nod, Grandpa Owl nods back, the camera arcs slowly around the short table"
CH[06]="$OWL; Gomgom and Kong are not in this scene"; DUR[06]=4
IMG[07]="wide shot of Gomgom sitting on a little stool in front of the huge wall of honey jars in the honey shop, holding its head with both paws, looking small and overwhelmed, the shelves stretching high above, warm light"
MOV[07]="Gomgom holds its head with both paws, then lowers them and lets out a small sigh with its mouth closed, the camera slowly pulls back to reveal how big the wall of jars is"
CH[07]="$GOM; Kong is not in this scene"; DUR[07]=4
IMG[08]="medium shot inside the honey shop, Gomgom and Grandpa Owl both standing side by side on the wooden shop floor, Grandpa Owl only slightly taller than Gomgom, about a quarter head taller, Grandpa Owl resting one wing gently on Gomgom's shoulder and pointing with the other wing toward one friendly honey jar on a low shelf beside them, Gomgom looking up at Grandpa Owl, warm lamp light, shelves of honey jars behind"
MOV[08]="Grandpa Owl pats Gomgom's shoulder and nods kindly, Gomgom's face brightens into a soft closed-mouth smile, both keep their feet on the floor, the camera moves slowly around the two of them, Grandpa Owl stays only slightly taller than Gomgom"
CH[08]="$GOM; $OWL; Kong is not in this scene"; DUR[08]=4
IMG[09]="close side shot along a wooden shelf of little honey jars with cloth lids, tiny Kong standing on both little feet on the flat shelf between the jars, Kong only half as tall as one honey jar and one third the width of Gomgom's head, tapping one cloth lid with the tip of its small wing, soft shop light, Gomgom's blurred paw at the edge of the frame"
MOV[09]="tiny Kong walks along the shelf between the jars and gently taps three cloth lids one after another with the tip of its folded wing, Kong never jumps, never flies and never spreads its wings wide, the jars stay still, the camera follows along the shelf at Kong's height, no object moves by itself, everything that moves is moved by a character's paw or wing"
CH[09]="$GOM; $KONG"; DUR[09]=4
IMG[10]="low angle shot of Gomgom hugging one small golden honey jar with both paws and smiling happily with its mouth closed, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, the honey shop shelves softly blurred behind, warm light"
MOV[10]="Gomgom hugs the honey jar and sways happily from side to side, tiny Kong on top of its head flutters its small wings a little while staying seated, the camera circles slowly at a low angle, Kong stays tiny"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[11]="wide shot from behind of Gomgom sitting at a small wooden kitchen table at sunset, spreading golden honey on a slice of bread, the small golden honey jar open on the table, tiny Kong standing on both little feet on the flat table beside a teacup, Kong only half as tall as the teacup, a window with a glowing felt village and pink sky beyond, gingham curtains, a teapot, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[11]="seen from behind the whole time, Gomgom slowly spreads honey on the bread, its head does not turn, tiny Kong beside the teacup turns its head to stare at the honey bread and happily hops up and down in place and flutters its small wings excitedly, Kong stays in the same spot right beside the teacup, Kong stays tiny and only half as tall as the teacup even while hopping, its wings stay small, the sunset glows, the camera stays directly behind Gomgom and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny"
CH[11]="$GOM; $KONG"; DUR[11]=8

mkdir -p img clips
KEYS="01 02 03 04 05 06 07 08 09 10 11"
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
