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
STYLE="richly detailed handmade miniature world with layered foreground, midground and background full of cute tiny handmade props, bright airy high-key lighting, soft diffused morning daylight, light fluffy pastel colors like a sunny storybook, creamy mint green, soft sky blue, butter yellow and peach tones, light pastel water, no dark shadows, no dark forest, no deep vignette, no moody contrast, soft and dreamy, handmade felt, knit, wood and ceramic textures with visible fuzzy wool fibers, high quality 3D animated film render, vertical 9:16, cheerful cozy mood, no text, no letters"
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
IMG[01]="Gomgom sitting alone in the corner of a bright sunny felt workshop with empty paws, looking down at the floor, head drooping and shoulders slumped, a sulky gloomy face with droopy eyes and a small downturned pouting closed mouth, not smiling at all, tiny Kong sitting at the very top center of Gomgom's head looking down worriedly, light wooden shelves with pastel spools of yarn, wood shavings on the floor, big bright window light"
MOV[01]="Gomgom lets out a small sigh and its shoulders sink a little more, tiny Kong on its head peeks down at Gomgom's face, the camera slowly moves in from low in front, Kong stays tiny"
CH[01]="$GOM; $KONG"; DUR[01]=4
IMG[02]="high angle shot looking down at a light wooden worktable covered with messy unfinished pastel felt crafts, half-sewn pieces, tangled yarn and scattered buttons, Gomgom resting its chin on one paw staring blankly at them with a sulky gloomy face, droopy eyes, eyebrows slanting down sadly and a clearly downturned frowning closed mouth, absolutely not smiling, no smile at all, tiny Kong standing on both little feet on the flat tabletop right beside a spool of thread, Kong only as tall as the spool and one third the width of Gomgom's head, bright daylight"
MOV[02]="Gomgom picks up an unfinished piece, looks at it, and sets it down again with a small sigh, tiny Kong looks at the pile, the camera looks straight down from directly above the table and slowly rotates, Kong stays tiny"
CH[02]="$GOM; $KONG"; DUR[02]=4
IMG[03]="spectacular wide view through a round workshop window onto a busy sunny pastel miniature felt village, exactly one felt squirrel pushing a little cart full of acorns, exactly one felt hedgehog fixing a cottage roof on a short ladder, exactly one felt rabbit hanging laundry, only these three animals and no other animals, flower boxes, cobblestone lanes, tiny rooftops, the window frame and a bit of Gomgom's shoulder in the near foreground"
MOV[03]="the friends keep busy, the squirrel pushes its cart along, the hedgehog taps the roof with a little hammer, the laundry sways in the breeze, the camera pushes slowly out through the window toward the village"
CH[03]="a felt squirrel, a felt hedgehog and a felt rabbit, each about as tall as Gomgom; $GOM seen only as a small part of its shoulder; Kong is not in this scene"; DUR[03]=4
IMG[04]="spectacular extreme low angle shot looking up from the forest floor at a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber towering over a mossy forest clearing, Gomgom standing small at the base of the trunk looking up at it, tiny Kong sitting at the very top center of Gomgom's head, sunbeams through the leaves, ferns, mushrooms, fallen leaves"
MOV[04]="Gomgom slowly tilts its head back to look up at the huge crooked tree, leaves sway gently in the breeze, the camera starts at the roots and rises up along the twisted trunk toward the wide branches, Kong stays tiny"
CH[04]="$GOM; $KONG"; DUR[04]=4
IMG[05]="storybook-like warm scene in the same forest clearing, three felt beaver carpenters (real beavers, not bears: dark brown felt beavers with a wide flat scaly paddle-shaped tail clearly visible, small round ears, a blunt rounded snout and two small orange front teeth) wearing little work aprons and carrying small wooden tool boxes and saws on their shoulders walking past a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber, the beavers glancing at the crooked trunk and shaking their heads, soft bright light, ferns, a forest path"
MOV[05]="the three beavers glance at the crooked tree, shake their heads and wave a paw dismissively, then keep walking along the path with their feet on the ground, the camera tracks alongside them at their height"
CH[05]="three felt beaver carpenters each about as tall as Gomgom; Gomgom and Kong are not in this scene"; DUR[05]=4
IMG[06]="wide shot of a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber alone in a felt meadow, shown in four seasons at once as a seamless panorama from left to right: pink spring blossoms, bright green summer leaves, red and gold autumn leaves, and white winter snow, the tree itself stays exactly the same crooked shape, rolling felt hills behind"
MOV[06]="time passes gently, falling blossoms, fluttering leaves and soft snowflakes drift down through the air, the tree stays exactly the same, the camera slowly circles around the tree, absolutely no animals and no characters appear at any moment, the meadow stays empty, only the tree, blossoms, leaves and snow"
CH[06]="no characters in this scene; Gomgom and Kong are not in this scene"; DUR[06]=4
IMG[07]="medium shot under the shade of a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber, Grandpa Turtle, a kind old felt turtle with olive green felt skin on its face, arms and legs (not cream, not a bear), a dark green felt shell on its back, a long soft white beard and a small woven straw conical hat, standing upright, Grandpa Turtle is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big standing beside Gomgom and talking kindly, Gomgom listening with a gentle closed-mouth smile, tiny Kong sitting at the very top center of Gomgom's head, dappled sunlight, moss, roots, a small stone bench"
MOV[07]="Grandpa Turtle raises one hand and points up at the crooked tree as it explains, Gomgom nods slowly, the camera glides slowly between the two of them, Grandpa Turtle stays only slightly taller than Gomgom, Kong stays tiny"
CH[07]="$GOM; Grandpa Turtle, a kind old felt turtle with olive green felt skin on its face, arms and legs (not cream, not a bear), a dark green felt shell on its back, a long soft white beard and a small woven straw conical hat, standing upright, Grandpa Turtle is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big; $KONG"; DUR[07]=4
IMG[08]="spectacular high angle wide shot of the cool shade under a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber on a bright sunny day, many felt animal friends resting in the shade, a squirrel napping on a root, a hedgehog and a rabbit sharing a picnic on a checkered blanket, a little fox reading a book, sunbeams flickering through the leaves, wildflowers"
MOV[08]="a breeze stirs the leaves and the dappled sunlight dances, the friends stretch lazily and smile, the camera descends slowly from high in the branches down into the shade"
CH[08]="a felt squirrel, a felt hedgehog, a felt rabbit and a small felt fox, each about as tall as Gomgom; Gomgom and Kong are not in this scene"; DUR[08]=4
IMG[09]="close shot of Grandpa Turtle, a kind old felt turtle with olive green felt skin on its face, arms and legs (not cream, not a bear), a dark green felt shell on its back, a long soft white beard and a small woven straw conical hat, standing upright, Grandpa Turtle is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big gently resting one hand on the thick twisted trunk of a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber and smiling up at it, rough bark texture, moss, small mushrooms, sunlight on the leaves, the turtle's whole face is olive green felt like its arms, its face is NOT cream and NOT white, only the beard is white"
MOV[09]="Grandpa Turtle pats the trunk softly and looks up with a warm smile, the camera arcs around from behind the trunk to the side and ends close on Grandpa Turtle's smiling face, one single continuous shot with no cuts, no sudden zoom and no jump, the camera moves smoothly the whole time"
CH[09]="Grandpa Turtle, a kind old felt turtle with olive green felt skin on its face, arms and legs (not cream, not a bear), a dark green felt shell on its back, a long soft white beard and a small woven straw conical hat, standing upright, Grandpa Turtle is slightly taller than Gomgom, about a quarter head taller, never shorter than Gomgom and never twice as big; Gomgom and Kong are not in this scene"; DUR[09]=4
IMG[10]="medium shot of Gomgom sitting in the shade under a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber with a peaceful closed-mouth smile, tiny Kong sitting on Gomgom's lap, Kong one third the width of Gomgom's head, a felt squirrel and a felt hedgehog leaning comfortably against Gomgom on each side, dappled sunlight, roots, wildflowers"
MOV[10]="Gomgom looks around at its resting friends with a warm smile, tiny Kong tilts its head, the friends snuggle closer, the camera starts low and close behind the squirrel's shoulder and swings around in a half circle to the front of the group, Kong stays tiny"
CH[10]="$GOM; $KONG; a felt squirrel and a felt hedgehog, each about as tall as Gomgom"; DUR[10]=4
IMG[11]="wide shot from behind of Gomgom sitting at the foot of a huge ancient gnarled oak tree with a thick twisted crooked trunk and wide spreading crooked branches, covered in soft felt leaves, clearly bent and knotted so it could never be cut into straight lumber at sunset, tiny Kong sitting at the very top center of Gomgom's head, a soft peach and pink pastel sunset sky, long soft shadows, rolling felt hills, the huge crooked tree silhouetted against the glowing sky, seen from behind so the star badge on Gomgom's chest is hidden and NOT visible, Gomgom's back is plain cream fuzzy wool with only the thin brown satchel strap crossing it"
MOV[11]="Gomgom sits still gazing at the sunset with tiny Kong on its head, the sunset glow slowly deepens and leaves sway gently, the camera stays close directly behind Gomgom and only drifts slowly upward a little, it never pulls back and never reveals new areas, only Gomgom and tiny Kong are in the scene the whole time, no other animal or character ever appears, no face is visible on the back of the head, Kong stays tiny"
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
    id=$(create_job veo3_1_lite --prompt "${MOV[$k]}, $SIZE, $VTAIL" --start-image "img/$k.png" --aspect_ratio 9:16 --duration ${DUR[$k]} --generate_audio false) || true
    if [ -n "$id" ] && fetch "$id" "$f"; then log "완료 $f"; else log "실패 영상 $k"; fi
  fi
done
log "끝($STAGE)"
