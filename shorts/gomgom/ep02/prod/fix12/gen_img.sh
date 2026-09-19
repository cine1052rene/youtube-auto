#!/usr/bin/env bash
# 2화 12 시작 그림 재생성 후보 2장 (저울 정확히 수평 + 곰곰이 입 다묾)
set -u; cd "$(dirname "$0")"
REF=../../../ref/gomgom_master.png
CHAR="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle closed-mouth smile with the mouth always closed; Kong, a tiny round yellow felt baby chick with a small orange beak"
STYLE="richly detailed handmade miniature world with layered foreground, midground and background, soft warm golden light, gentle depth of field that keeps the detailed background readable, cozy warm pastel palette, handmade felt, knit, wood and ceramic textures, high quality 3D animated film render, cinematic composition, vertical 9:16, warm and cozy mood, no text, no letters"
P="straight-on front view at eye level of a large handmade wooden balance scale standing on a table in a cozy felt workshop, one tall central post with ONE STRAIGHT HORIZONTAL BEAM on top, two identical round wooden pans hanging on thin chains from the two ends of the beam, the beam is PERFECTLY LEVEL and BOTH PANS HANG AT EXACTLY THE SAME HEIGHT in perfect balance, the LEFT pan holds a small glass jar with three softly glowing felt stars, the RIGHT pan holds one small white fluffy felt cloud, Gomgom and Kong standing side by side on the table in front of the scale looking up at it happily, Gomgom with a gentle closed-mouth smile, spools of pastel yarn, little tools and warm lamps in the background"
for n in a b; do
  f=12_$n.png; [ -s "$f" ] && continue
  out=$(higgsfield generate create seedream_v5_lite --prompt "$P, $CHAR, $STYLE" --image-references "$REF" --aspect_ratio 9:16 --quality high --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try: d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { echo "FAIL $n: $(echo "$out"|head -c 200)"; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && echo "done $f"
done
