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
IMG[01]="close high angle shot of Gomgom lying in a cozy little felt bed at night, wide awake with its round bead eyes open looking at the ceiling, a patchwork quilt pulled up to its chin, on the bedside table a small wicker basket holding a half-knitted cream scarf with two knitting needles stuck in it, a crescent moon through a round window, a tiny night lamp, a felt alarm clock with no numbers, framed felt pictures"
MOV[01]="Gomgom turns from one side to the other under the quilt and then opens its eyes again and stares at the ceiling, the moonlight shimmers through the window, the camera slowly arcs around the side of the bed"
CH[01]="$GOM; Kong is not in this scene"; DUR[01]=4
IMG[02]="medium shot of a cozy living room in the evening, Gomgom in a small wooden rocking chair yawning with its mouth softly open and no teeth, holding knitting needles with a half-finished cream scarf on its lap, tiny Kong standing on both little feet on the flat side table right beside a ball of yarn, Kong is only half as tall as the ball of yarn and one third the width of Gomgom's head, a fireplace with a warm glow, a knitted rug, a bookshelf, a potted plant"
MOV[02]="Gomgom yawns, slowly puts the needles into the basket and stands up from the rocking chair, tiny Kong stays standing on the side table and tilts its head, Kong never jumps or flies, the fire flickers, the camera glides sideways past the side table"
CH[02]="$GOM; $KONG"; DUR[02]=4
IMG[03]="dramatic straight top-down bird's-eye view from the bedroom ceiling looking down at Gomgom lying awake in the middle of a round felt bed, the patchwork quilt spread out like a colorful map, long soft cream and pastel yarn strands curling across the whole bedroom floor in big dreamy spirals around the bed like a frozen whirlpool, balls of yarn, slippers, a rug, the bedside table with the knitting basket and night lamp seen from above, moonlight shapes from the window falling across the floor"
MOV[03]="Gomgom blinks up at the ceiling and turns its head from side to side on the pillow, the yarn spirals on the floor stay completely still, the camera slowly rotates a little while staying directly above the bed and rises higher, no object moves by itself, everything that moves is moved by a character's paw or wing"
CH[03]="$GOM; Kong is not in this scene"; DUR[03]=4
IMG[04]="grand high-angle wide shot from an upper corner of a bustling two-floor felt village diner with deep perspective, a wooden balcony level with more tables, a warm chandelier and strings of tiny lights across the ceiling, many checkered tables full of $FRIENDS eating pancakes, Grandpa Owl wearing a small striped apron as the waiter, slightly taller than Gomgom, carrying a tray of plates with no notepad between the tables, Gomgom small at a window table in the corner watching curiously, a big round window with the felt village outside, plants, a cake counter"
MOV[04]="Grandpa Owl walks carefully between the busy tables carrying the tray and sets plates down in front of customers with a proud nod, the customers chat and eat, Gomgom watches from its window table, the camera glides down from the high corner over the balcony railing toward the floor, everyone's feet stay on the floor"
CH[04]="$GOM; $OWL; Kong is not in this scene"; DUR[04]=4
IMG[05]="low angle shot at the diner counter, Grandpa Owl slightly taller than Gomgom standing behind a little wooden cash register with no numbers, having just taken a coin, scratching its head with one wing with a puzzled smile, Gomgom standing at the counter laughing softly with its mouth closed, jars of cookies and a cake stand on the counter"
MOV[05]="Grandpa Owl drops the coin into the register drawer, then scratches its head as if it forgot something, Gomgom giggles with its mouth closed, the camera circles slowly at counter height"
CH[05]="$GOM; $OWL; Kong is not in this scene"; DUR[05]=4
IMG[06]="close shot of Gomgom's paws holding the half-knitted cream scarf tightly against its chest, the knitting needles still in it, warm lamp light in the cozy bedroom, Gomgom's face above looking down at the scarf with a slightly worried look"
MOV[06]="Gomgom hugs the scarf tighter and then slowly loosens its grip with a small sigh, the camera rises from the paws holding the scarf up to Gomgom's face"
CH[06]="$GOM; Kong is not in this scene"; DUR[06]=4
IMG[07]="medium shot at a small bedside desk under a warm lamp, Gomgom holding a pencil and drawing on a small paper note a simple picture of a scarf and five small circles, no letters or numbers anywhere, tiny Kong standing on both little feet on the flat desk right beside an eraser, Kong is only as tall as the eraser and one third the width of Gomgom's head, a cup of warm milk, a little alarm clock with no numbers, a jar of pencils"
MOV[07]="Gomgom finishes drawing and puts the pencil down, tiny Kong leans over to peek at the note and nods, Kong stays standing on the desk with its wings folded, the camera slides sideways along the desk"
CH[07]="$GOM; $KONG"; DUR[07]=4
IMG[08]="medium shot of Gomgom kneeling on the bedroom rug beside a wicker knitting basket that is much smaller than Gomgom and sits on the floor, Gomgom pinning a small paper note onto the half-knitted cream scarf draped over the basket edge, the note shows a simple drawing of a scarf and five small circles with no letters, balls of colorful yarn inside the basket, warm bedside lamp light, the bed behind"
MOV[08]="Gomgom presses the pin into the scarf and gently pats the note flat with its paw, then nods to itself, the camera arcs slowly around the basket from the side without zooming in"
CH[08]="$GOM; Kong is not in this scene"; DUR[08]=4
IMG[09]="low angle shot on the wooden bedroom floor at night, tiny Kong pushing a round cream ball of yarn with both little wings toward the wicker basket, Kong is only half as tall as the ball of yarn, a loose trail of yarn behind, the basket a short distance ahead, the rug edge and slippers nearby, moonlight on the floor"
MOV[09]="tiny Kong waddles forward pushing the ball of yarn with its wings until the ball rolls up against the basket and stops, Kong keeps both feet on the floor and never jumps or flies, the yarn only moves because Kong pushes it, the camera follows along at floor height, no object moves by itself, everything that moves is moved by a character's paw or wing"
CH[09]="$KONG; Gomgom is not in this scene"; DUR[09]=4
IMG[10]="high angle shot of Gomgom fast asleep in the cozy felt bed with a peaceful smile and closed eyes, tiny Kong curled up asleep in the very center of the pillow beside Gomgom's head, Kong only one third the width of Gomgom's head, patchwork quilt, the wicker basket with the scarf and pinned note on the bedside table, stars through the round window"
MOV[10]="Gomgom breathes slowly and the quilt rises and falls gently, tiny Kong sleeps curled up on the pillow, the stars twinkle in the window, the camera slowly rises higher above the bed"
CH[10]="$GOM; $KONG"; DUR[10]=4
IMG[11]="wide shot from behind of Gomgom sitting by a sunny morning window in a little armchair, knitting the cream scarf again on its lap, tiny Kong sitting at the very top center of Gomgom's head between its two round ears, the window shows a bright felt village and blue sky, potted flowers on the sill, the wicker basket beside the chair, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[11]="seen from behind the whole time, Gomgom's paws move the knitting needles calmly, its head does not turn, tiny Kong sits still at the very top center of Gomgom's head looking out the window, sunlight glows, the camera stays directly behind Gomgom and only rises slowly straight up, it never circles around, no face is visible on the back of the head, Kong stays tiny"
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
