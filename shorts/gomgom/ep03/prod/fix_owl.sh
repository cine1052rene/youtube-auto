#!/usr/bin/env bash
# 부엉이 할아버지 색 통일(02번 갈색 부엉이 기준) — generate.sh 1차 실행이 끝난 뒤에 실행
# 빠진 그림(img/NN.png 없는 번호)만 새 부엉이 문장으로 다시 만들고, 이어서 generate.sh로 빠진 영상 생성
set -u
cd "$(dirname "$0")"
LOG=gen.log
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
REF=../../ref/gomgom_master.png
CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle closed-mouth smile with the mouth always closed; Kong, a tiny round yellow felt baby chick with a small orange beak"
OWL="Grandpa Owl, a kind old round chestnut-brown felt owl (a real owl with feathered head tufts, no bear ears) with a cream heart-shaped face, fluffy white eyebrows, big round thin black spectacles, a small yellow beak, a cream scalloped chest, a tiny green laurel wreath and a little white toga wrapped around its body"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
declare -A IMG
IMG[03]="medium side view of a simple rustic wooden table under a shady olive tree, a round crusty bread loaf and a clay water jug on the table, $OWL breaking the bread and sharing a piece with Gomgom, Kong hopping across the table toward the crumbs"
IMG[04]="macro close up on a rustic wooden table of a tiny round clay pot with a lid, a chestnut-brown feathered owl wing lifting the lid to reveal soft white cheese inside, Kong leaning over the rim peeking in with wide curious eyes, Gomgom softly blurred in the background under an olive tree"
IMG[05]="medium wide shot of a small joyful feast under an olive tree with only a little clay cheese pot, a bread loaf and a water jug on the wooden table, $OWL and Gomgom gently clinking small clay cups, Kong dancing happily on the table, warm dappled sunlight and a few round paper lanterns hanging from the branches"
for k in 03 04 05; do
  f="img/$k.png"; [ -s "$f" ] && continue
  log "부엉이 보정 그림 $k"
  id=$(higgsfield generate create seedream_v5_lite --prompt "${IMG[$k]}, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high --json </dev/null 2>&1 | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { log "실패 보정 그림 $k"; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && [ -s "$f" ] && log "완료 보정 $f" || log "다운로드 실패 보정 $k"
done
bash ./generate.sh
