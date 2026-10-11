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
IMG[01]="close shot of Gomgom in front of a round wooden mirror in a cozy bedroom in the morning, one tuft of fur on top of its head sticking straight up, Gomgom patting it with both paws with a worried face, a felt hairbrush and a tiny comb on the dresser, morning sun through curtains, a little potted cactus"
MOV[01]="Gomgom pats the sticking-up tuft down with both paws but it springs back up again, Gomgom's ears droop in a funny worried way, the camera moves from the mirror reflection around to Gomgom's side"
CH[01]="$GOM; Kong is not in this scene"; DUR[01]=4
IMG[02]="wide eye level shot of a bustling handmade felt village market street with striped awnings, fruit stalls, flower carts and bunting flags, Gomgom walking in with one paw held over the sticking-up tuft on its head, tiny Kong perched on Gomgom's shoulder, $FRIENDS shopping in the background"
MOV[02]="Gomgom walks into the market keeping one paw on its head, glancing left and right, tiny Kong on its shoulder looks around curiously, the awnings flutter, the camera tracks backward in front of Gomgom"
CH[02]="$GOM; $KONG"; DUR[02]=4
IMG[03]="low angle shot of Gomgom standing in the middle of the market with its shoulders hunched, a soft warm theater spotlight beam shining down on it from above like on a stage, the rest of the market slightly dimmer around it, tiny Kong on its shoulder squinting up at the light"
MOV[03]="the soft spotlight follows Gomgom as it takes two shy steps, Gomgom hunches lower and holds its tuft, tiny Kong squints at the light, the camera circles slowly around Gomgom at low height"
CH[03]="$GOM; $KONG"; DUR[03]=4
IMG[04]="high angle wide shot above the busy felt market, all the small felt animal friends busy with their own things, a rabbit choosing carrots, a squirrel counting acorns, a hedgehog arranging flowers, nobody looking at Gomgom who stands small in the middle, bunting and lanterns between the stalls"
MOV[04]="the animal friends keep busy with their shopping and nobody turns to Gomgom, the camera rises higher above the market to show everyone busy, small Gomgom in the middle looks around"
CH[04]="$GOM; $FRIENDS; Kong is not visible"; DUR[04]=4
IMG[05]="medium shot of Grandpa Owl standing slightly taller than Gomgom at a little outdoor market stall, Grandpa Owl holding up a tiny bright yellow felt T-shirt with a funny cartoon face print and no letters, Gomgom looking at it with a curious face, a clothesline of tiny felt clothes behind them, baskets and lanterns"
MOV[05]="Grandpa Owl lifts the tiny bright T-shirt and wiggles it, Gomgom tilts its head with interest, the clothesline sways in the breeze, the camera arcs slowly around the stall"
CH[05]="$GOM; $OWL; Kong is not in this scene"; DUR[05]=4
IMG[06]="wide shot of a cozy felt classroom with little wooden desks, a small felt rabbit standing at the doorway wearing a plain bright yellow T-shirt with no print and no letters, cheeks pink and covering its face shyly, the rabbit is exactly as tall as the other animal friends, its ears only reach the top of the doorway handle, both of its feet stand firmly on the floor, there is only one rabbit in the whole room, no yellow chick anywhere in the classroom, a squirrel, a hedgehog, a fox and a sheep sitting at the desks, no other rabbits, a board with only doodles of flowers and no letters, potted plants"
MOV[06]="the small rabbit in the plain yellow T-shirt stands still at the doorway with both feet planted on the floor, it covers its face shyly and then peeks out between its paws, its feet never leave the floor and it never floats or flies, the camera very slowly pushes in toward the rabbit, no other rabbit and no new characters appear, the classmates stay seated at their desks, everyone keeps the same size the whole time"
CH[06]="small felt animal classmates: a squirrel, a hedgehog, a fox and a sheep, each about as tall as Gomgom, the only rabbit is the one in the yellow T-shirt; Gomgom and Kong are not in this scene"; DUR[06]=4
IMG[07]="medium wide shot of the same felt classroom, the shy rabbit in the bright yellow T-shirt sitting down, three of the four animal friends busy reading picture books, drawing and chatting, only one hedgehog glancing at the T-shirt briefly, warm window light, plants and a globe"
MOV[07]="most of the animal friends keep reading and drawing without looking up, only the hedgehog glances once at the T-shirt and goes back to its book, the rabbit in the yellow T-shirt relaxes and smiles, the camera slowly pushes in toward the rabbit in the yellow T-shirt which stays in the center of the frame the whole time, no new characters appear"
CH[07]="$FRIENDS; Gomgom and Kong are not in this scene"; DUR[07]=4
IMG[08]="front view of a tiny cozy felt puppet theater stage with velvet curtains and little footlights, Gomgom standing alone on the stage under a bright spotlight looking shy, rows of little wooden seats where a few small needle-felted animal dolls are turned around chatting to each other, every audience member is a felt animal doll, no humans, no people anywhere"
MOV[08]="the bright spotlight on Gomgom slowly widens and softens into warm general light, Gomgom looks up and its shoulders relax, the curtains sway, the camera slowly pushes in toward the stage, every audience member stays a small felt animal doll, no humans appear"
CH[08]="$GOM; Kong is not in this scene"; DUR[08]=4
IMG[09]="eye level shot along the busy felt market stalls, a rabbit weighing carrots on a little scale, a squirrel counting acorns into jars, a hedgehog tying a bouquet of felt flowers, everyone happily focused on their own work, warm afternoon light, bunting overhead, Gomgom small in the background"
MOV[09]="the market friends keep busy with their own tasks, carrots tumble onto the scale and acorns drop into jars, the camera tracks along the stalls past each busy friend"
CH[09]="$GOM; $FRIENDS; Kong is not visible"; DUR[09]=4
IMG[10]="close shot of Gomgom sitting on a market bench, tiny Kong standing on top of Gomgom's head pressing down the sticking-up tuft with both little wings, Gomgom smiling quietly with its eyes softly closed and its small stitched smile line, mouth closed, a basket of apples beside it, flower stall behind"
MOV[10]="tiny Kong presses the tuft down with its little wings, the tuft springs back up and Kong presses again, Gomgom smiles quietly with its eyes softly closed, its small stitched smile line stays exactly the same and the mouth never opens, Kong stays tiny on top of the head, the camera arcs slowly around the bench"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[11]="wide three-quarter shot of Gomgom walking happily through the market with its head held high and the tuft still sticking up, holding a little paper bag of bread, tiny Kong perched on its head, stall keepers busy with their work, bunting, lanterns and flower carts"
MOV[11]="Gomgom walks cheerfully past the stalls looking around with a happy face, tiny Kong rides on its head, a squirrel waves casually and goes back to work, the camera tracks alongside Gomgom"
CH[11]="$GOM; $KONG"; DUR[11]=4
IMG[12]="wide shot from behind of Gomgom sitting on a little hill at sunset overlooking the felt market village where lanterns are lighting up, tiny Kong perched on Gomgom's head next to the sticking-up tuft, a paper bag of bread beside Gomgom, pink and gold sky, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[12]="seen from behind, Gomgom sits on the hill as the lanterns of the market light up one by one, tiny Kong snuggles beside the tuft, the breeze makes the tuft wiggle, the camera rises slowly and pulls back to reveal the whole glowing village"
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
