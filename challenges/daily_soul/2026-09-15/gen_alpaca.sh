#!/usr/bin/env bash
# 사용자가 하트한 알파카 구도(b_cine)를 Soul 2.0으로 보정 — 알파카 얼굴 보이게, 선생님 억지 미소, 벤치 보이게
cd "$(dirname "$0")"
LOG=gen_alpaca.log
log(){ echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
BASE="kindergarten class picture day in a sunny green schoolyard, about sixteen small children in matching white polo school uniforms with homemade paper crowns sitting in two rows on a clearly visible long wooden bench, their teacher in a white shirt and jeans standing beside the class holding a stiff forced posed smile for the camera with wide nervous eyes, a big fluffy white alpaca has just stolen the teacher's wide straw sun hat and is wearing it crooked on its head, the alpaca's funny face with big dark eyes, teeth and chewing mouth is clearly visible under the brim, children laughing, pointing and clapping with different expressions, crayons and paper crown pieces scattered on the grass"
TAIL="realistic candid photograph, on-camera flash mixed with bright natural daylight, rich detailed environment, natural anatomy with correct hands and legs, every face distinct and believable, no text, no watermark"
declare -A P
P[A]="wide 24mm lens, the alpaca very close in the foreground right side filling a third of the frame and looking straight into the camera, class behind it, dynamic slightly tilted angle, $BASE"
P[B]="wide 28mm lens, the alpaca right next to the teacher pulling the straw hat off her head with its teeth mid-action, hat half lifted, teacher still smiling stiffly toward the camera, class on the bench behind cracking up, $BASE"
P[C]="low angle from grass level with a 24mm lens looking up at the class photo, the alpaca's head wearing the straw hat poking into the frame from the lower left very close to the lens, $BASE"
P[D]="slightly high angle group photo composition with a 24mm lens, the alpaca wearing the straw hat walking across the front of the class photo and knocking over the tripod sign board, paper crowns flying in the air, $BASE"
for k in A B C D; do
  f="alp_${k}_soul2.png"; [ -s "$f" ] && { log "skip $f"; continue; }
  out=$(higgsfield generate create text2image_soul_v2 --prompt "${P[$k]}, $TAIL" --aspect_ratio 3:2 --quality 2k --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
  [ -z "$id" ] && { log "FAIL create $k: $(echo "$out"|tr -d '\n'|head -c 200)"; sleep 5; continue; }
  url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  curl -s -o "$f" "$url" && log "done $f id=$id" || log "FAIL download $k"
done
log "ALL DONE balance=$(higgsfield account status --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin)['credits'])")"
