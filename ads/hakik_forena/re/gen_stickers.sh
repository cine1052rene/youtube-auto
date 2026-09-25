#!/usr/bin/env bash
cd "$(dirname "$0")"
TAIL="single glossy 3D cartoon icon, cute rounded shapes, vivid saturated colors, soft studio lighting, centered with generous empty margin, isolated on a completely flat solid pure chroma green background #00FF00, no shadow on the background, no text, no letters, no numbers"
declare -A P
P[coins]="a tall stack of shiny gold coins next to a small pink piggy bank"
P[gift]="a red gift box with a big gold ribbon bow, green paper banknotes popping out of the box"
P[house]="a cute small white house with a blue roof and a big golden key in front of it"
P[sun]="a bright happy yellow sun with soft rays and a light blue wind swirl beside it"
P[train]="a cute front view of a blue and white subway train"
P[book]="a closed navy blue bank passbook booklet standing upright"
P[phone]="a golden retro telephone handset with ringing motion sparkles"
P[washer]="two white front loading washing machines standing side by side"
for k in coins gift house sun train book phone washer; do
  f="stk/$k.png"; [ -s "$f" ] && continue
  for t in 1 2 3; do
    out=$(higgsfield generate create seedream_v5_lite --prompt "${P[$k]}, $TAIL" --aspect_ratio 1:1 --quality high --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try: d=json.load(sys.stdin); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
    [ -n "$id" ] && break; echo "retry $k: $out" | head -c 300; sleep 30
  done
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && echo "done $k"
done
echo "STICKERS DONE"
