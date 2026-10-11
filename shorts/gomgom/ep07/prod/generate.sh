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
IMG[01]="close three-quarter angle across a cluttered felt workbench at dusk, Gomgom sitting with a half-built miniature brick house made of tiny felt bricks in front of it, a tiny trowel in its paw, looking up in surprise at a round window where the orange sun is already setting, tiny Kong standing on both little feet on the flat workbench right beside the half-built brick house, clearly separate from Gomgom's body, Kong is much shorter than the half-built brick wall, its whole body only as tall as four stacked tiny felt bricks and only one third the width of Gomgom's head, spools of thread, little jars of felt bricks, a desk lamp, a cork board with felt fabric swatches"
MOV[01]="Gomgom looks from the half-built house up to the window as the last sunlight fades, its ears droop a little, tiny Kong standing on the workbench beside the little house looks up at the window and tilts its head, Kong's feet stay on the workbench, the lamp flickers on, the camera slowly arcs from the workbench side toward the window"
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
IMG[08]="medium shot at a cozy breakfast nook, Gomgom sitting with a tiny notebook and a pencil, tapping the pencil on its chin thoughtfully, a cup of cocoa and a plate of tiny cookies, morning light through checkered curtains, tiny Kong standing on both little feet on the flat table right next to the open notebook, peeking at the page, clearly separate from Gomgom's body, Kong is only half as tall as the cocoa cup and only one third the width of Gomgom's head, Gomgom is the only bear and the only doll in the room, no other plush toys or round cream objects anywhere in the foreground or background, a little cuckoo clock on the wall"
MOV[08]="Gomgom taps the pencil on its chin and then raises one finger as if it has an idea, tiny Kong stays standing on the table beside the notebook with its wings folded and both feet on the table the whole time, it only tilts its head and bobs gently, Kong never jumps and never flies, steam curls from the cocoa, the camera slowly pushes in toward Gomgom from slightly lower, Gomgom stays in frame the whole time, there is only one bear in the room"
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
IMG[12]="wide shot from behind of Gomgom sitting on the workshop porch step at sunset beside the finished miniature brick house placed on the step, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, a watering can, a little lantern and flower pots on the porch, a handmade felt village and pink sky beyond, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[12]="seen from behind the whole time, Gomgom sits still on the porch facing away as the sunset deepens, its head does not turn, tiny Kong sits still at the very top center of Gomgom's head between the ears, looking at the sunset, the tiny house windows glow and fireflies rise, the camera stays directly behind Gomgom and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny at the top center of the head"
CH[12]="$GOM; $KONG"; DUR[12]=8

# ── 10/12 추가·교체: 느리게 늘리지 않도록 컷 나누기(NNb) + 제자리 줌인 교체(06·10) ──
IMG[02b]="close low angle on the sunny workbench, Gomgom's fuzzy paws happily pressing tiny felt bricks one by one along a pencil line on a plan sheet, the first neat row of the little brick house growing, tiny Kong standing on both little feet on top of the brick pile beside it, Kong only as tall as three stacked tiny felt bricks, a small wooden hammer, a ruler, sunlight and dust sparkles"
MOV[02b]="Gomgom presses three felt bricks into the row quickly one after another and gives a proud little nod, tiny Kong bobs happily on the brick pile with its wings folded and its feet staying on the bricks, the camera slides sideways along the growing brick row"
CH[02b]="$GOM; $KONG"; DUR[02b]=4
IMG[06]="dreamy sparkly daydream version of the sunny workshop glowing with soft golden light and floating sparkles, tiny felt bricks floating up in the air by magic and stacking themselves neatly onto the walls of the miniature brick house, Gomgom standing beside the workbench clapping its paws in delight with a big happy smile, soft pastel glow, dreamlike haze around the edges"
MOV[06]="tiny felt bricks fly up one after another and click into place by themselves, the walls of the little house rise quickly, Gomgom claps and bounces happily on its feet, sparkles swirl, the camera circles quickly around the rising house"
CH[06]="$GOM; Kong is not in this scene"; DUR[06]=4
IMG[06b]="dreamy sparkly daydream of the finished miniature brick house on the workbench glowing in golden light, little felt roof tiles flying through the air with sparkles toward the roof, a bright felt sun shining through the window, Gomgom spinning happily beside it with its arms open, soft pastel glow, dreamlike haze around the edges"
MOV[06b]="the last felt roof tiles fly onto the roof and snap into place with a puff of sparkles, the chimney pops up, Gomgom twirls around once happily, the camera swoops up over the roof"
CH[06b]="$GOM; Kong is not in this scene"; DUR[06b]=4
IMG[08b]="close over the shoulder shot at the cozy breakfast table, Gomgom's paws quickly flipping the pages of its little notebook backward looking for an old page, pages full of small doodles of tiny houses and birdhouses with no letters and no numbers, a cup of cocoa with steam, tiny Kong standing on both little feet on the table beside the notebook, Kong only half as tall as the cocoa cup, checkered curtains and morning light"
MOV[08b]="Gomgom flips the notebook pages backward quickly and stops on an old doodle page, tilting its head curiously, tiny Kong leans in to peek with its wings folded and its feet on the table, the camera moves around Gomgom's shoulder toward the notebook, there is only one bear"
CH[08b]="$GOM; $KONG"; DUR[08b]=4
IMG[10]="cozy workshop morning, Gomgom standing on a little wooden stool in front of a big friendly felt wall clock with no numbers, turning the long minute hand with both paws, tiny Kong sitting on the flat top of the clock, Kong only as big as the clock's center knob, shelves of tools and potted plants, warm morning light"
MOV[10]="Gomgom pushes the clock's long minute hand all the way around in a big generous circle with both paws and nods firmly, tiny Kong on top of the clock sways along happily with its wings folded, the camera arcs from the side around to the front of the clock"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[10b]="close shot on the workbench, Gomgom flipping over a big cute felt hourglass full of golden sand, the sand starting to pour down, the half-built little brick house and neat piles of felt bricks waiting beside it, tiny Kong standing on both little feet beside the hourglass, Kong only half as tall as the hourglass, warm morning light"
MOV[10b]="Gomgom turns the big hourglass over with both paws and sets it down with a happy pat, golden sand begins to pour, tiny Kong watches the sand with its head tilting and its feet on the table, the camera glides low past the hourglass toward Gomgom's smiling face"
CH[10b]="$GOM; $KONG"; DUR[10b]=4
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
