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
IMG[01]="close three-quarter angle across a cluttered felt workbench at dusk, Gomgom sitting with a half-built miniature brick house made of tiny felt bricks in front of it, a tiny trowel in its paw, looking up in surprise at a round window where the orange sun is already setting, tiny Kong perched on Gomgom's shoulder, spools of thread, little jars of felt bricks, a desk lamp, a cork board with felt fabric swatches"
MOV[01]="Gomgom looks from the half-built house up to the window as the last sunlight fades, its ears droop a little, tiny Kong on its shoulder tilts its head, the lamp flickers on, the camera slowly arcs from the workbench side toward the window"
CH[01]="$GOM; $KONG"; DUR[01]=4
IMG[02]="bright high angle shot of a sunny afternoon workshop, Gomgom happily laying out a neat plan on the workbench next to a pile of tiny felt bricks, a small wooden hammer, a ruler and a tiny bucket of glue, tiny Kong perched on top of the brick pile cheerfully, sunlight pouring through a big window with potted plants and hanging tools on a pegboard"
MOV[02]="Gomgom places the first few felt bricks in a row and nods confidently, tiny Kong hops on top of the brick pile, sunlight sparkles on the dust, the camera glides down from a high angle to table height"
CH[02]="$GOM; $KONG"; DUR[02]=4
IMG[03]="low angle shot from the workbench surface, Gomgom carefully stacking tiny felt bricks into a wall that wobbles, a few bricks fallen over beside it, a round wall clock behind, warm late afternoon light, tiny Kong on Gomgom's head watching the wall"
MOV[03]="the wall of felt bricks wobbles and two bricks tumble down, Gomgom catches one and sighs with its mouth closed, the wall clock hands sweep forward quickly, the camera slides sideways along the bench past the brick wall"
CH[03]="$GOM; $KONG"; DUR[03]=4
IMG[04]="wide shot from outside the workshop window at night, looking in through the glowing window at Gomgom still working at the bench by lamp light, the miniature brick house still without a roof, a crescent moon and stars above a tiny felt village, fireflies, a little potted plant on the window sill"
MOV[04]="seen through the window, Gomgom rubs its eyes and keeps working under the lamp, fireflies drift past the glass, the camera slowly pulls back from the window to reveal the dark sleepy village"
CH[04]="$GOM; Kong is not in this scene"; DUR[04]=4
IMG[05]="medium shot inside Grandpa Owl's cozy treehouse library, Grandpa Owl standing slightly taller than Gomgom next to a big felt hourglass on a little table, Gomgom listening with its paws together, curved shelves of tiny books, hanging dried flowers, a teapot with a knitted cozy, round window with forest view, warm lamp light"
MOV[05]="Grandpa Owl gently turns the big felt hourglass over and the sand starts to fall, Gomgom watches it closely and blinks, the camera arcs slowly around the two of them from eye level"
CH[05]="$GOM; $OWL; Kong is not in this scene"; DUR[05]=4
IMG[06]="dreamy medium shot of Gomgom gazing upward with a soft smile, a soft translucent felt thought bubble above its head showing a tiny picture of the brick house finished with a bright sun, sparkles inside the bubble, the cozy treehouse library softly blurred behind with shelves and lanterns"
MOV[06]="inside the thought bubble the tiny brick house builds itself in a flash, Gomgom smiles dreamily, then the bubble wobbles softly, the camera rises along the bubble and tilts down to Gomgom"
CH[06]="$GOM; Kong is not in this scene"; DUR[06]=4
IMG[07]="top down shot of a wooden desk covered with Gomgom's old felt projects, a lopsided felt birdhouse, a half-knitted tiny scarf, a little boat model, Gomgom's paws flipping a scrapbook of old felt photos with no letters, tiny Kong walking across the scrapbook"
MOV[07]="Gomgom's paws slowly flip the pages of the old scrapbook, tiny Kong hops from one page to the next and stays right beside Gomgom's paws, the camera drifts slightly lower while keeping Gomgom and Kong together in frame, Kong stays tiny"
CH[07]="$GOM; $KONG"; DUR[07]=4
IMG[08]="medium shot at a cozy breakfast nook, Gomgom sitting with a tiny notebook and a pencil, tapping the pencil on its chin thoughtfully, a cup of cocoa and a plate of tiny cookies, morning light through checkered curtains, tiny Kong perched on Gomgom's shoulder peeking at the notebook, a little cuckoo clock on the wall"
MOV[08]="Gomgom taps the pencil on its chin and then raises one finger as if it has an idea, tiny Kong flaps its little wings on the shoulder, steam curls from the cocoa, the camera slowly pushes in toward Gomgom from slightly lower, Gomgom stays in frame the whole time, there is only one bear in the room"
CH[08]="$GOM; $KONG"; DUR[08]=4
IMG[09]="close shot of Gomgom looking at a cork board covered with small felt photos of its old finished projects, each photo pinned next to a tiny felt sun or moon sticker, no letters or numbers anywhere, Gomgom pointing at one photo with a curious face, string lights around the board"
MOV[09]="Gomgom moves its paw from one felt photo to the next and nods slowly as it remembers, the string lights twinkle, the camera slides along the cork board toward Gomgom's face"
CH[09]="$GOM; Kong is not in this scene"; DUR[09]=4
IMG[10]="low angle shot of a big friendly felt wall clock on the workshop wall, tiny Kong sitting on top of the clock and leaning down to push the long minute hand with its little wing, Gomgom below drawing a big generous circle on a felt calendar with no letters, warm morning light"
MOV[10]="tiny Kong pushes the clock's minute hand around in a big circle and wobbles happily, Gomgom below draws a wide circle on the calendar, the camera tilts down from the clock to Gomgom"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[11]="golden hour three-quarter shot of Gomgom proudly placing the last tiny felt roof tile on the finished miniature brick house on the workbench, the house has a little chimney and tiny windows glowing warmly, tiny Kong standing on the roof ridge, the orange sun still above the hills through the window"
MOV[11]="Gomgom presses the last roof tile into place and steps back with a happy closed-mouth smile, tiny Kong does a little hop on the roof ridge, the windows of the tiny house light up, the camera pulls back and arcs around the finished house"
CH[11]="$GOM; $KONG"; DUR[11]=4
IMG[12]="wide shot from behind of Gomgom sitting on the workshop porch step at sunset beside the finished miniature brick house placed on the step, tiny Kong perched on Gomgom's shoulder, a watering can, a little lantern and flower pots on the porch, a handmade felt village and pink sky beyond, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[12]="seen from behind the whole time, Gomgom sits still on the porch facing away as the sunset deepens, its head does not turn, tiny Kong snuggles against its ear, the tiny house windows glow and fireflies rise, the camera stays directly behind Gomgom and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny on the shoulder"
CH[12]="$GOM; $KONG"; DUR[12]=8

mkdir -p img clips
KEYS="01 02 03 04 05 06 07 08 09 10 11 12"
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
