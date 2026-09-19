#!/usr/bin/env bash
# 2차 시안: 배지 3종(+가방), 모자 4종(+가방). 베레모 제외(폼폼푸린 유사)
set -u; cd "$(dirname "$0")"
REF=../gomgom_master.png
BASE="character reference sheet, full body front view of two handmade needle-felted wool characters standing side by side on a plain warm cream background with a soft floor shadow, "
GOM="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy felt texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle smile with no teeth visible"
BAG="and carries a tiny brown felt satchel bag with a thin strap across its body"
KONG="Kong, a tiny round soft yellow needle-felted baby chick with a small orange beak and tiny orange feet, with ONE small bright green bean sprout with two round leaves growing from the top of its head"
TAIL="both characters look exactly like handmade felt dolls, high quality 3D render, soft warm studio light, cute and warm, no text, no letters, no logo"
declare -A P
P[honey]="Gomgom wears a small round golden honey-drop shaped felt badge pinned on its chest $BAG"
P[daisy]="Gomgom wears a small white and yellow daisy flower felt badge pinned on its chest $BAG"
P[star]="Gomgom wears a small soft yellow five-pointed star felt badge pinned on its chest $BAG"
P[straw]="Gomgom wears a small woven straw sun hat with a sage green ribbon, its round ears poking out from under the brim, $BAG"
P[bobble]="Gomgom wears a cozy oatmeal knitted bobble hat with two holes so its round ears poke through the top, $BAG"
P[bucket]="Gomgom wears a small soft sage green felt bucket hat sitting behind its round ears, $BAG"
P[rain]="Gomgom wears a small glossy yellow rain hat with a wide back brim, its round ears poking out, $BAG"
for k in honey daisy star straw bobble bucket rain; do
  f=v2_$k.png; [ -s "$f" ] && continue
  out=$(higgsfield generate create seedream_v5_lite --prompt "$BASE$GOM, ${P[$k]}; $KONG. $TAIL" --image-references "$REF" --aspect_ratio 3:4 --quality high --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try: d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { echo "FAIL $k $(echo "$out"|head -c 200)"; sleep 20; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && echo "done $f"
done
