#!/usr/bin/env bash
# 곰곰이·콩이 시그니처 소품 시안 (기준 이미지 참조, seedream_v5_lite)
set -u; cd "$(dirname "$0")"
REF=../gomgom_master.png
BASE="character reference sheet, full body front view of two handmade needle-felted wool characters standing side by side on a plain warm cream background with a soft floor shadow, "
GOM="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy felt texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle smile with no teeth visible"
KONG="Kong, a tiny round soft yellow needle-felted baby chick with a small orange beak and tiny orange feet, with ONE small bright green bean sprout with two round leaves growing from the top of its head"
TAIL="both characters look exactly like handmade felt dolls, high quality 3D render, soft warm studio light, cute and warm, no text, no letters, no logo"
declare -A P
P[a]="Gomgom wears a soft sage green hand-knitted scarf wrapped loosely around its neck with the two ends hanging in front"
P[b]="Gomgom wears a honey-yellow felt maple-leaf shaped brooch pinned on its chest and carries a tiny brown felt satchel bag across its body"
P[c]="Gomgom wears a mustard yellow hand-knitted scarf, and a tiny felt notebook with a pencil peeks out of a small sewn-on patch pocket on its tummy"
P[d]="Gomgom wears a tiny round acorn-cap beret made of brown felt tilted on its head between its ears"
for k in a b c d; do
  f=opt_$k.png; [ -s "$f" ] && continue
  out=$(higgsfield generate create seedream_v5_lite --prompt "$BASE$GOM, ${P[$k]}; $KONG. $TAIL" --image-references "$REF" --aspect_ratio 3:4 --quality high --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try: d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { echo "FAIL $k $(echo "$out"|head -c 200)"; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && echo "done $f"
done
