#!/usr/bin/env bash
# Daily Soul Challenge 2026-09-15 "Smile for the Camera" — 장면 4개 × (Soul 2.0, Soul Cinematic)
cd "$(dirname "$0")"
LOG=gen.log
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
TAIL="everyone keeps a big frozen posed smile for the camera while total chaos happens around them, realistic candid photograph, on-camera flash mixed with natural daylight, wide 24mm lens, dynamic slightly tilted angle, mid-action motion with flying details frozen sharp, every person has a distinct believable expression and natural anatomy with correct hands, rich detailed environment, no text, no watermark"
declare -A P
P[a]="a lakeside wedding group portrait on a wooden pier at golden hour, the bride and groom in the center with bridesmaids and groomsmen in a neat row, at the exact moment the old pier planks snap and the whole right side of the wedding party drops toward the water, one groomsman already half splashing into the lake holding his smile, bouquet and hats flying, the photographer's framing still perfect"
P[b]="a kindergarten class picture day photo in a sunny schoolyard, twenty small children in matching uniforms on low benches with their teacher standing proudly at the side, while a fluffy white alpaca has pushed its head into the frame from behind and is chewing the teacher's wide straw sun hat right off her head, a few kids pointing and giggling, crayons and paper crowns scattered in the grass"
P[c]="a family christmas card portrait in a cozy living room, three generations in matching red knitted sweaters posed on a sofa in front of a tall decorated christmas tree, at the moment the tree topples forward over them with ornaments bursting into the air, a startled ginger cat launching off the top of the tree through the frame, grandpa still holding the posed thumbs up"
P[d]="an amateur neighborhood cycling race award ceremony photo on a small outdoor podium with the three winners holding medals and a giant trophy, at the moment the wobbly wooden podium tips sideways and a champagne bottle erupts in a huge foam spray across all three faces, confetti cannon firing at the wrong angle, crowd behind with phones raised"
for k in a b c d; do
  for m in text2image_soul_v2 soul_cinematic; do
    tag=$([ $m = soul_cinematic ] && echo cine || echo soul2)
    f="${k}_${tag}.png"; [ -s "$f" ] && { log "skip $f"; continue; }
    out=$(higgsfield generate create $m --prompt "${P[$k]}, $TAIL" --aspect_ratio 3:2 --quality 2k --json </dev/null 2>&1)
    id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
    [ -z "$id" ] && { log "FAIL create $f: $(echo "$out"|tr -d '\n'|head -c 200)"; sleep 5; continue; }
    url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
    ext="${url##*.}"; f2="${k}_${tag}.${ext:-png}"
    curl -s -o "$f2" "$url" && log "done $f2 id=$id" || log "FAIL download $f"
  done
done
log "ALL DONE balance=$(higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin)['credits'])")"
