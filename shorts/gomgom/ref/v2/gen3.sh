#!/usr/bin/env bash
# 3차 시안: 보터햇 3종(리본 색), 시즌1 배지 후보 3종 — 전부 갈색 가방 포함
set -u; cd "$(dirname "$0")"
REF=../gomgom_master.png
BASE="character reference sheet, full body front view of two handmade needle-felted wool characters standing side by side on a plain warm cream background with a soft floor shadow, "
GOM="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy felt texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle smile with no teeth visible"
BAG="and carries a tiny brown felt satchel bag with a thin strap across its body"
KONG="Kong, a tiny round soft yellow needle-felted baby chick with a small orange beak and tiny orange feet, with ONE small bright green bean sprout with two round leaves growing from the top of its head"
TAIL="both characters look exactly like handmade felt dolls, high quality 3D render, soft warm studio light, cute and warm, no text, no letters, no logo"
BOAT="Gomgom wears a small classic straw boater hat with a FLAT round top crown and a FLAT stiff straight brim, sitting neatly on top of its head between its two round ears so both ears stay fully visible"
declare -A P
P[boat_sage]="$BOAT, with a sage green band ribbon, $BAG"
P[boat_honey]="$BOAT, with a honey yellow band ribbon, $BAG"
P[boat_navy]="$BOAT, with a navy blue and white striped band ribbon, $BAG"
P[s1_heart]="Gomgom wears a soft coral pink felt heart shaped badge pinned on its chest, clearly visible, $BAG"
P[s1_pot]="Gomgom wears a fairly large round golden honey pot shaped felt badge pinned on its chest, clearly visible, $BAG"
P[s1_clover]="Gomgom wears a bright green four-leaf clover felt badge pinned on its chest, clearly visible, $BAG"
for k in boat_sage boat_honey boat_navy s1_heart s1_pot s1_clover; do
  f=v3_$k.png; [ -s "$f" ] && continue
  for t in 1 2 3; do
    out=$(higgsfield generate create seedream_v5_lite --prompt "$BASE$GOM, ${P[$k]}; $KONG. $TAIL" --image-references "$REF" --aspect_ratio 3:4 --quality high --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try: d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
    [ -n "$id" ] && break; echo "retry $k"; sleep 30
  done
  [ -z "$id" ] && { echo "FAIL $k"; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && echo "done $f"
done
echo ALLDONE
