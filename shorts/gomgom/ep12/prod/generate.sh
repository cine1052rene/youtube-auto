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
IMG[01]="medium three-quarter front shot of Gomgom standing on a grassy hilltop at sunset wearing a small damp backpack, gazing at a glowing orange and pink sunset over rolling felt hills with a gentle smile and no teeth, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, wildflowers, a winding path below"
MOV[01]="Gomgom takes a slow deep breath and its shoulders relax, tiny Kong on its head looks at the sunset too, the sunset glows, the camera slides slowly sideways in front of Gomgom, Kong stays tiny"
CH[01]="$GOM; $KONG"; DUR[01]=4
IMG[02]="spectacular wide shot of a sunny morning meadow with a winding flower path, a felt windmill, rolling hills and fluffy clouds, Gomgom walking along the path carrying a wicker picnic basket, tiny Kong standing on both little feet on the flat wicker lid of the basket, Kong only one third the width of Gomgom's head, butterflies, daisies"
MOV[02]="Gomgom walks happily along the flower path with its feet on the ground swinging the basket gently, tiny Kong stays standing on the basket lid and looks around, Kong never jumps or flies, the camera starts high above the meadow and swoops down to travel alongside Gomgom at its height, Kong stays tiny"
CH[02]="$GOM; $KONG"; DUR[02]=4
IMG[03]="high angle shot of Gomgom in the middle of an open meadow under sudden dark rain clouds, heavy rain pouring down, Gomgom holding the wicker picnic basket over its head to block the rain, tiny Kong peeking out of the small front pocket of Gomgom's brown satchel, the flower path turning into puddles, a misty forest edge"
MOV[03]="Gomgom lifts the basket above its head in surprise, the rain pours down hard, tiny Kong ducks into the satchel pocket, the camera slowly descends from above toward Gomgom, Kong stays tiny"
CH[03]="$GOM; $KONG"; DUR[03]=4
IMG[04]="medium shot of a cozy felt cabin like a little laboratory, Grandpa Owl slightly taller than Gomgom standing beside two round wooden basins of water on a table, a felt squirrel about as tall as Gomgom dipping one paw into the left basin and flinching from the cold, a small wooden sand hourglass on the table, shelves of jars, a window"
MOV[04]="the squirrel dips its paw into the water and hunches its shoulders shivering, Grandpa Owl watches the sand hourglass closely, the camera glides sideways at basin height"
CH[04]="$OWL; a felt squirrel about as tall as Gomgom; Gomgom and Kong are not in this scene"; DUR[04]=4
IMG[05]="medium shot in the same cozy felt cabin, a felt squirrel about as tall as Gomgom pointing with one paw at the right one of two round wooden basins of water and nodding, Grandpa Owl slightly taller than Gomgom smiling beside it, a small sand hourglass on the table, shelves of jars"
MOV[05]="the squirrel points at the right basin and nods firmly, Grandpa Owl nods back with a smile, the camera arcs slowly around the table from the other side"
CH[05]="$OWL; a felt squirrel about as tall as Gomgom; Gomgom and Kong are not in this scene"; DUR[05]=4
IMG[06]="medium shot by a warm crackling fireplace, Grandpa Owl slightly taller than Gomgom and Gomgom sitting side by side in two little armchairs talking, two teacups on a small table, a knitted rug, a bookshelf, warm firelight"
MOV[06]="Grandpa Owl lifts one wing slightly as it explains, Gomgom listens and nods slowly with a closed-mouth smile, the firelight flickers, the camera moves slowly in from the fireplace side, Grandpa Owl stays only slightly taller than Gomgom"
CH[06]="$GOM; $OWL; Kong is not in this scene"; DUR[06]=4
IMG[07]="medium side shot of Gomgom sitting by a cabin window in the evening, warm sunset light glowing on its face, a thoughtful gentle smile with its mouth closed, the damp picnic basket on the floor beside it, potted plants on the sill"
MOV[07]="Gomgom looks out the window and slowly nods to itself with a soft closed-mouth smile, the sunset light shifts, the camera slides slowly along the window toward Gomgom's face"
CH[07]="$GOM; Kong is not in this scene"; DUR[07]=4
IMG[08]="spectacular low angle wide shot of a rain-washed meadow with a huge bright rainbow arching across the clearing sky, sunbeams through parting clouds, sparkling wet grass and wildflowers, Gomgom standing with the picnic basket set down beside it, looking up at the rainbow, tiny Kong sitting at the very top center of Gomgom's head"
MOV[08]="Gomgom slowly opens its arms wide toward the rainbow with a closed-mouth smile, exactly one small mouth, the clouds drift apart, tiny Kong looks up too, the camera starts low in the wet grass behind the flowers and rises up and back to reveal the huge rainbow arching over Gomgom, Kong stays tiny"
CH[08]="$GOM; $KONG"; DUR[08]=4
IMG[09]="medium shot on a checkered picnic blanket under the rainbow, Gomgom holding a warm mug of cocoa with both paws, tiny Kong standing on both little feet on the blanket right beside a small cup, Kong only half as tall as the small cup and one third the width of Gomgom's head, cookies on a plate, the wicker basket, wet flowers glistening"
MOV[09]="Gomgom blows gently on the cocoa and takes a small sip, tiny Kong beside the small cup nods happily, Kong never jumps or flies, steam rises from the mug, the camera circles slowly at blanket height, Kong stays tiny"
CH[09]="$GOM; $KONG"; DUR[09]=4
IMG[10]="wide shot from behind of Gomgom walking home along a sunset path carrying the wicker basket, tiny Kong sitting at the very top center of Gomgom's head, the sky glowing red and gold, felt cottages with lit windows in the distance, fireflies, wildflowers along the path, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[10]="Gomgom walks slowly away along the path with its feet on the ground, the sky glows warmer, seen from behind the whole time, its head does not turn, the camera stays directly behind and rises high behind Gomgom to show the whole winding sunset path and the glowing village ahead, it never circles around, no face is visible on the back of the head, Kong stays tiny"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[11]="wide shot from behind of Gomgom standing at a cabin window at night, a warm mug of cocoa on the windowsill and a small crayon drawing of a rainbow with no letters propped beside it, tiny Kong standing on both little feet on the flat windowsill right beside the mug, Kong only half as tall as the mug, stars and a crescent moon over the felt village outside, gingham curtains, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[11]="Gomgom stands still gazing at the stars, tiny Kong on the windowsill looks out too, seen from behind the whole time, its head does not turn, the camera stays directly behind and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny"
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
