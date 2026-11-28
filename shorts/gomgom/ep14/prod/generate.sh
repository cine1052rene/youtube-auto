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
STYLE="richly detailed handmade miniature world filling the whole background with layered foreground, midground and background full of cute tiny handmade props, never a plain empty wall, white haze or empty backdrop, detailed scenery receding deep into the distance, soft warm golden daylight, bright cheerful exposure, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette with natural soft leafy greens and clear natural water, handmade felt, knit, wood and ceramic textures with visible fuzzy wool fibers, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no dark shadows, no gloomy colors, no text, no letters"
VTAIL="the bear mouth may open softly but no teeth are ever visible, every character keeps exactly the same needle-felted wool texture, proportions, colors, accessories and body size from the first frame to the last and never turns into a cartoon or 2D character, nobody grows or shrinks during the shot, Kong stays tiny, smooth gentle camera motion with a clear change of viewpoint, bright airy pastel light, light cheerful colors, no dark shadows, no text"

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
IMG[01]="medium shot from the front of Gomgom stomping out of a felt cottage toward the camera, the open wooden door behind it, Gomgom's paws balled into little fists, cheeks flushed pink, a grumpy pouting closed-mouth face with furrowed brows, tiny Kong sitting at the very top center of Gomgom's head, a garden stone path, flower pots, a picket fence"
MOV[01]="Gomgom stomps forward along the stone path toward the camera with grumpy little steps, its feet on the ground, cheeks puffed, tiny Kong on its head sways, the camera moves slowly backward ahead of Gomgom at its height, Kong stays tiny"
CH[01]="$GOM; $KONG"; DUR[01]=4
IMG[02]="medium shot through a cottage window of a felt raccoon friend about as tall as Gomgom inside with its arms crossed and turned away with a pouty face, gingham curtains, a teapot on the table, potted plants on the sill"
MOV[02]="the raccoon turns its head away with a huff and keeps its arms crossed, the camera moves slowly from outside the window toward the glass"
CH[02]="a felt raccoon friend about as tall as Gomgom; Gomgom and Kong are not in this scene"; DUR[02]=4
IMG[03]="low angle shot at water level of Gomgom sitting on a mossy rock by a clear calm forest stream, raising one paw holding a small heavy grey river pebble about to throw it, a sulky gloomy face with droopy eyes, eyebrows slanting down sadly and a clearly downturned frowning closed mouth, absolutely not smiling, no smile at all, tiny Kong sitting at the very top center of Gomgom's head, the water surface calm with no splash and no ripples yet, nothing floating on the water, ferns, smooth river stones on the banks, dappled sunlight"
MOV[03]="Gomgom throws the small heavy grey river pebble forward into the stream, the pebble falls into the water with a small splash and immediately sinks under the water and disappears from sight, only round ripples spread on the surface, nothing floats or bounces on the water, the pebble never reappears, Gomgom lowers its paw and pouts, keeping a sulky downturned face the whole time and never smiling, the camera stays low near the water surface and slides slowly toward Gomgom, Kong stays tiny"
CH[03]="$GOM; $KONG"; DUR[03]=4
IMG[04]="spectacular close shot at water level of a clear stream flowing around a large smooth round rock, the water gently parting and curling around both sides of the rock, sparkling sunlight on the ripples, pebbles visible under the clear water, felt moss on the rock, behind the rock the stream winds back into a lush forest with layered trees, ferns and wildflowers on both banks and a tiny wooden footbridge far away, clear blue sky above"
MOV[04]="the water flows smoothly around the rock and joins again behind it, sparkles dance on the surface, the camera glides low over the water toward the rock and past it"
CH[04]="no characters in this scene; Gomgom and Kong are not in this scene"; DUR[04]=4
IMG[05]="spectacular bird's-eye view looking straight down at a winding sparkling forest stream curving around many smooth rocks, green moss, ferns and wildflowers along both banks, sunlight glittering on the water"
MOV[05]="the water keeps flowing and sparkling around the rocks, tiny Kong stands still on the mossy bank watching the water and tilts its head, the camera moves slowly downstream following the water from high above, no other animals or characters appear at any moment, Kong stays tiny"
CH[05]="no characters in this scene; Gomgom and Kong are not in this scene"; DUR[05]=4
IMG[06]="medium shot beside a forest stream, Gomgom and Grandpa Buffalo, a kind old felt water buffalo with soft grey wool, long white droopy eyebrows, small curved horns and a tiny cloth bundle tied on its back, both standing upright side by side on the same mossy bank at the same distance from the camera, Grandpa Buffalo is clearly a quarter head taller than Gomgom, never smaller than Gomgom and never twice as big, Grandpa Buffalo looking down kindly at Gomgom and gently pointing one hoof at the flowing water, Gomgom looking up at him listening, tiny Kong sitting at the very top center of Gomgom's head, ferns, river stones, bright soft daylight"
MOV[06]="Grandpa Buffalo gestures gently with one hoof toward the flowing water as it speaks, Gomgom lifts its head and listens, the camera glides slowly over the stream between them, Grandpa Buffalo stays only slightly taller than Gomgom, Kong stays tiny"
CH[06]="$GOM; Grandpa Buffalo, a kind old felt water buffalo with soft grey wool, long white droopy eyebrows, small curved horns and a tiny cloth bundle tied on its back, Grandpa Buffalo is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big; $KONG"; DUR[06]=4
IMG[07]="spectacular wide shot along a forest stream, a few tiny blue and brown felt sparrows (not yellow, not chicks) drinking at the water's edge, wildflowers and lush green grass growing thick wherever the water touches, a small felt deer drinking, butterflies, sunlight, no yellow chicks anywhere"
MOV[07]="the birds dip their beaks to drink, the flowers sway, butterflies flutter, the camera moves slowly sideways along the stream"
CH[07]="tiny blue and brown felt sparrows and a small felt deer; Gomgom and Kong are not in this scene"; DUR[07]=4
IMG[08]="close shot of Gomgom's paws gently placing a small bright yellow folded paper boat onto the surface of the clear stream, Gomgom's soft closed-mouth smile visible above, river stones and moss, behind Gomgom the sparkling stream winds far into the distance through a flowery meadow and layered forest trees, a tiny wooden footbridge and little felt cottages on the far bank"
MOV[08]="Gomgom slowly lets go of the paper boat and it begins to float, the camera starts close on Gomgom's paws at water level and tilts up and rises to Gomgom's gently smiling face"
CH[08]="$GOM; Kong is not in this scene"; DUR[08]=4
IMG[09]="medium shot at water level of a small bright yellow folded paper boat floating down the stream with tiny Kong standing at the front of the boat with its wings folded, Kong only as tall as the paper boat's pointed sail, Kong one third the width of Gomgom's head, Gomgom walking on the dry grassy bank beside the stream with both feet on the grass and never in the water, ferns, rocks, sparkling water, behind them the winding stream stretches far into the distance through a flowery meadow and layered forest trees, a small wooden footbridge downstream and little felt cottages on the far bank"
MOV[09]="the paper boat floats along and turns gently around a rock, tiny Kong sways happily at the bow with its little wings folded close to its body, never spreading its wings, Gomgom walks beside it on the bank with its feet on the ground, the camera tracks alongside the boat at water level, Kong stays tiny"
CH[09]="$GOM; $KONG"; DUR[09]=4
IMG[10]="low angle shot from under a small wooden footbridge over the stream, a felt raccoon friend about as tall as Gomgom standing on the bridge deck with both feet firmly on the wooden planks, leaning over the railing and holding a small bright yellow folded paper boat it just scooped out of the water, the raccoon is not jumping and not flying, smiling down at Gomgom, Gomgom standing on the grassy bank below waving shyly, tiny Kong sitting at the very top center of Gomgom's head, flowers, sunlight"
MOV[10]="the raccoon stays standing on the bridge with both feet on the wooden planks, never jumping, holds up the paper boat and smiles, Gomgom waves shyly with a closed-mouth smile, the camera looks up from under the bridge and rises slowly"
CH[10]="$GOM; $KONG; a felt raccoon friend about as tall as Gomgom"; DUR[10]=4
IMG[11]="wide shot from directly behind of Gomgom and a felt raccoon friend about as tall as Gomgom sitting side by side on the stream bank at sunset, BOTH seen completely from behind, the raccoon's grey back and its ringed striped tail facing the camera, no faces visible at all, both looking forward toward the sunset, tiny Kong sitting at the very top center of Gomgom's head also seen from behind, the stream flows in front of them away from the camera toward the glowing sunset, a small bright yellow folded paper boat floating small in the distance on the stream ahead of them between them and the sunset, the water glowing gold and pink, ferns and reeds silhouetted, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[11]="they sit still side by side with their backs to the camera watching the small paper boat drift away into the sunset, the boat floats slowly farther away, the sunset light glitters on the water, the camera stays close directly behind them and only drifts slowly upward a little, it never pulls back and never reveals new areas, no other animal or character ever appears, no faces are visible on the backs of their heads, Kong stays tiny"
CH[11]="$GOM; $KONG; a felt raccoon friend about as tall as Gomgom"; DUR[11]=6

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
    id=$(create_job veo3_1_lite --prompt "${MOV[$k]}, $SIZE, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration ${DUR[$k]} --generate_audio false) || true
    if [ -n "$id" ] && fetch "$id" "$f"; then log "완료 $f"; else log "실패 영상 $k"; fi
  fi
done
log "끝($STAGE)"
