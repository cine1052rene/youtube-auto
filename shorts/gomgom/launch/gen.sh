#!/usr/bin/env bash
# 채널 런칭용 프로필·배너 원본 생성 (이미 있으면 건너뜀)
set -u
cd "$(dirname "$0")"
REF=../ref/gomgom_master_s1.png
LOG=gen.log
CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm closed-mouth smile with no teeth visible, wearing a small matte coral pink felt heart badge on its chest (matte wool felt, no glow, no plastic shine) and a tiny brown felt satchel bag across its body; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head, Kong's round body only as big as Gomgom's head"
STYLE="handmade needle-felted miniature, soft warm golden light, cozy warm pastel palette, felt, knit and wood textures, high quality 3D animated film render, warm and cozy mood, no text, no letters, no logo"
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
gen(){ # name aspect prompt
  local f="gen/$1.png"; [ -s "$f" ] && { log "건너뜀 $f"; return; }
  log "생성 $1"
  local out id url
  out=$(higgsfield generate create seedream_v5_lite --prompt "$3, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio "$2" --quality high --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { log "오류 $1: $(echo $out | head -c 200)"; return; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  [ -n "$url" ] && curl -s -o "$f" "$url" && log "완료 $f" || log "다운로드 실패 $1"
}
gen p1 1:1 "channel profile portrait, front view close-up of Gomgom's face and upper body perfectly centered in the frame, Kong sitting on top of Gomgom's head, plain soft warm cream to peach gradient background with gentle bokeh, simple and clean, characters fill the middle of the frame with even margin all around for a circular crop"
gen p2 1:1 "channel profile portrait, Gomgom centered hugging Kong gently against its chest, both looking at the viewer, plain soft sage green background with soft light, simple clean icon-like composition centered for a circular crop"
gen p3 1:1 "channel profile portrait, Gomgom centered with its head slightly tilted in a thoughtful cozy pose, one paw on its chin, Kong perched on its shoulder, plain warm honey yellow background, simple and clean, centered for a circular crop"
gen b1 21:9 "ultra wide panoramic banner, a cozy felt village on rolling hills at golden hour with tiny glowing cottage windows, Gomgom and Kong sitting together on a small wooden bench exactly in the horizontal center of the image, small in frame, plenty of calm open sky on the left and right, soft clouds"
gen b2 21:9 "ultra wide panoramic banner, cozy felt living room with a round window at dusk, warm lamp light, bookshelves and knitted cushions, Gomgom sitting on a small sofa in the exact center of the image with a cup of tea, Kong on the armrest, calm and uncluttered on both sides"
gen b3 16:9 "wide banner scene, soft starry night sky over a gentle grassy felt hill, Gomgom and Kong seen from the side sitting together on the hill in the exact center, small in frame, a handmade felt village with glowing windows in the distance, lots of calm open sky"
log "끝"
