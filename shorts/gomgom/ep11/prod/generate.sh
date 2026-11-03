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
IMG[01]="close eye level shot of Gomgom standing in a cozy felt entryway holding a brand-new bright yellow umbrella with a curved wooden handle, closed, with both paws and gazing at it with its mouth softly open in delight and no teeth, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, a wooden shoe rack with little boots, coat hooks, a round window with rain outside, a plain striped doormat with no letters or words"
MOV[01]="Gomgom gently turns the closed umbrella in its paws to admire it and tilts its head, tiny Kong on its head tilts its head too, the camera slowly rises from low in front of Gomgom, Kong stays tiny"
CH[01]="$GOM; $KONG"; DUR[01]=4
IMG[02]="spectacular view through a big arched window speckled with raindrops, Gomgom inside hugging a closed bright yellow umbrella and pressing its nose to the glass, outside a rainy miniature felt village with glowing lanterns, puddles, cobblestone streets, flower boxes and tiny rooftops, warm light inside, cool blue rain outside"
MOV[02]="Gomgom presses its nose to the window and bounces happily on its feet while hugging the umbrella, the rain keeps falling outside the window, the camera moves slowly from outside the glass toward Gomgom"
CH[02]="$GOM; Kong is not in this scene"; DUR[02]=4
IMG[03]="medium shot of a rainy felt village alley, Gomgom standing proudly under an open bright yellow umbrella, a felt squirrel and a felt hedgehog, each about as tall as Gomgom standing under a shop awning watching and smiling, cobblestones, puddles, flower pots, lanterns"
MOV[03]="Gomgom twirls the open umbrella once by its handle with a proud smile, the squirrel and the hedgehog clap their paws, raindrops spin off the umbrella edge, the camera starts low near the wet cobblestones and sweeps in a wide half circle around Gomgom from the friends' side to the front, everyone's feet stay on the ground"
CH[03]="$GOM; a felt squirrel and a felt hedgehog, each about as tall as Gomgom; Kong is not in this scene"; DUR[03]=4
IMG[04]="medium side shot of a felt entryway corner, a closed bright yellow umbrella leaning quietly against the wall beside a shoe rack, Gomgom walking past it in the background eating a cookie and not looking at the umbrella, warm lamp light, coat hooks"
MOV[04]="the camera stays almost still with only a very slow gentle push toward the corner, Gomgom takes three small slow steps to the right holding the cookie in its paw, its mouth stays closed in one gentle small smile, exactly one small mouth, Gomgom stays fully inside the frame, everything else in the room stays exactly as it is in the first frame, no hands, no people, no new objects appear, no object moves by itself, everything that moves is moved by a character's paw or wing"
CH[04]="$GOM; Kong is not in this scene"; DUR[04]=4
IMG[05]="medium shot of a cozy felt living room, a felt raccoon friend about as tall as Gomgom sitting on a plump sofa hugging a small sparkling pouch of gold coins with no letters or numbers anywhere, knitted cushions, a lamp, a window, a rug"
MOV[05]="the raccoon hugs the pouch of coins happily, then slowly sets it down on the sofa beside it and lets out a small yawn with its mouth softly open and no teeth, the camera slowly arcs around the sofa"
CH[05]="a felt raccoon friend about as tall as Gomgom; Gomgom and Kong are not in this scene"; DUR[05]=4
IMG[06]="medium shot of a cozy study full of bookshelves, Grandpa Owl slightly taller than Gomgom sitting in a little armchair talking kindly, Gomgom sitting across from it on a small stool listening, a small round table between them with two teacups, a warm reading lamp, a globe"
MOV[06]="Grandpa Owl lifts one wing slightly as it explains, Gomgom nods slowly with a closed-mouth smile, the camera glides slowly between the two of them, Grandpa Owl stays only slightly taller than Gomgom"
CH[06]="$GOM; $OWL; Kong is not in this scene"; DUR[06]=4
IMG[07]="low angle shot in the felt entryway, Gomgom picking up a brand-new bright yellow umbrella with a curved wooden handle again from the corner and smiling, tiny Kong standing on both little feet on the flat top of the wooden shoe rack right beside a pair of small rain boots, Kong only half as tall as one rain boot and one third the width of Gomgom's head, coat hooks, round window with rain"
MOV[07]="Gomgom opens the umbrella with a happy closed-mouth smile, tiny Kong on the shoe rack tilts its head and watches, Kong never jumps or flies, the camera looks up from low and rises a little"
CH[07]="$GOM; $KONG"; DUR[07]=4
IMG[08]="spectacular wide shot from behind of Gomgom walking slowly down a rainy flower-lined lane under an open bright yellow umbrella, tiny Kong sitting at the very top center of Gomgom's head under the umbrella, felt cottages with glowing windows, hydrangea bushes, lanterns, puddles reflecting the yellow umbrella, gentle rain, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[08]="there is exactly one Kong in the whole scene, tiny Kong stays sitting on top of Gomgom's head underneath the umbrella the whole time and never appears on top of the umbrella, nothing sits on top of the umbrella canopy, Gomgom walks slowly forward down the lane with its feet on the ground, raindrops bounce off the umbrella, seen from behind the whole time, its head does not turn, the camera stays directly behind and rises smoothly from behind up to a high bird's-eye view looking down on the yellow umbrella moving along the flower lane, it never circles around, no face is visible on the back of the head, Kong stays tiny"
CH[08]="$GOM; $KONG"; DUR[08]=4
IMG[09]="close side shot under the yellow umbrella, Gomgom with its eyes softly closed listening to the rain with a peaceful closed-mouth smile, tiny Kong sitting at the very top center of Gomgom's head also looking out, raindrops dripping from the umbrella edge, soft rainy light, blurred flowers behind"
MOV[09]="Gomgom keeps its eyes closed and its gentle closed-mouth smile the whole time, exactly one small mouth that never opens, raindrops drip from the umbrella edge, tiny Kong sways a little, the camera slowly arcs beside Gomgom's face, Kong stays tiny"
CH[09]="$GOM; $KONG"; DUR[09]=4
IMG[10]="low angle shot by a puddle on a cobblestone path as the rain stops, sunlight breaking through the clouds lighting up the bright yellow umbrella, Gomgom tilting the umbrella back to look up at the sky, tiny Kong standing on both little feet on a flat round stepping stone beside the puddle, Kong only as tall as a small daisy growing beside the stone and one third the width of Gomgom's head, sparkling raindrops on flowers"
MOV[10]="sunlight spreads across the path, Gomgom gently twirls the umbrella and smiles with its mouth closed, tiny Kong flutters its small wings a little while staying standing on the stone, Kong never jumps or flies, the camera starts at puddle level showing the umbrella's reflection in the water and rises up past Gomgom to a low angle looking up at the sunlit yellow umbrella against the blue sky, Kong stays tiny"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[11]="wide shot from behind of Gomgom standing in an open felt cottage doorway in the evening after the rain, the bright yellow umbrella resting in an umbrella stand beside the door, tiny Kong sitting at the very top center of Gomgom's head, a soft rainbow over the wet village and pink sky beyond, a plain striped doormat with no letters or words, potted flowers, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[11]="Gomgom stands still gazing at the rainbow, seen from behind the whole time, its head does not turn, the camera stays directly behind and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny"
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
