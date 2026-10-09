#!/usr/bin/env bash
# 콩이를 작게 그린 시즌2 기준 이미지 시안 3장
cd "$(dirname "$0")"
GOM="Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm closed-mouth smile, wearing a small matte yellow felt star badge on its chest with no glow and no plastic shine and a tiny brown felt satchel bag across its body"
KONG="Kong, a tiny round yellow needle-felted baby chick with a small orange beak, small folded wings and one small green bean sprout with two round leaves on top of its head"
SIZE="exact scale: Kong is very small, Kong's whole round body is only about one third the width of Gomgom's head, like a little ornament, Kong is much smaller than Gomgom's head"
BASE="character reference sheet photo, plain soft cream studio background, soft even light, full body visible, high quality 3D needle felt doll photography, vertical 3:4, no text, no letters"
P1="$GOM standing front view, $KONG sitting on Gomgom's left shoulder, $SIZE, $BASE"
P2="$GOM standing three-quarter view, $KONG perched on top of Gomgom's head between its ears, $SIZE, $BASE"
P3="$GOM standing front view, $KONG standing on the floor beside Gomgom's foot, Kong only reaches Gomgom's knee, $SIZE, $BASE"
i=1
for P in "$P1" "$P2" "$P3"; do
  out=$(higgsfield generate create seedream_v5_lite --prompt "$P" --image-references ../gomgom_master_s2.png --aspect_ratio 3:4 --quality high --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json;d=json.loads(sys.stdin.read());print(d[0] if isinstance(d,list) else '')" 2>/dev/null)
  [ -z "$id" ] && { echo "실패 $i $out"; i=$((i+1)); continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  [ -z "$url" ] && url=$(higgsfield generate get "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o cand$i.png "$url" && echo "완료 cand$i.png"
  i=$((i+1))
done
