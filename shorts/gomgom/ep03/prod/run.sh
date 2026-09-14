#!/usr/bin/env bash
# 1) 2화 마무리 컷(13) 재생성: 곰곰이 입 다물고 앉은 채, 별과 콩이만 날아오름
# 2) 3화 생성
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
EP2="$HERE/../../ep02/prod"
LOG="$HERE/gen.log"
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

VTAIL="Kong is lively and expressive, Gomgom keeps its mouth closed with a gentle closed-mouth smile, both characters keep exactly the same appearance and colors and stay cute with bright open eyes, smooth cinematic camera motion, warm cozy mood, soft warm light, no text"
P13="Gomgom stays seated on the grassy hilltop the whole time and gently opens the jar, the glowing stars float up into the sunset sky, Kong flies up among the stars, Gomgom turns its head to look back with a gentle closed-mouth smile, Gomgom never leaves the ground and keeps its cream color, the camera slowly rises and pulls back to reveal the whole glowing town"

if [ -f "$EP2/clips/13_old.mp4" ] && [ -s "$EP2/clips/13.mp4" ]; then
  log "2화 13 이미 수정됨 — 건너뜀"
else
  [ -f "$EP2/clips/13_old.mp4" ] || cp "$EP2/clips/13.mp4" "$EP2/clips/13_old.mp4"
  log "2화 13 재생성 (Wan 5초)"
  out=$(cd "$EP2" && higgsfield generate create wan2_7 --prompt "$P13, $VTAIL" --start-image img/13.png --aspect_ratio 9:16 --duration 5 --resolution 720p --json </dev/null 2>&1)
  id=$(echo "$out" | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')" 2>/dev/null)
  if [ -z "$id" ]; then
    log "2화 13 생성 오류: $(echo "$out" | tr -d '\n' | head -c 200) — 기존 영상 유지"
  else
    url=$(higgsfield generate wait "$id" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))" 2>/dev/null)
    if [ -n "$url" ] && curl -s -o "$EP2/clips/13_new.mp4" "$url" && [ -s "$EP2/clips/13_new.mp4" ]; then
      mv -f "$EP2/clips/13_new.mp4" "$EP2/clips/13.mp4"
      log "완료 2화 13 교체 (기존은 13_old.mp4)"
    else
      log "2화 13 다운로드 실패 ($id) — 기존 영상 유지"
    fi
  fi
fi

log "3화 생성 시작"
bash "$HERE/generate.sh"
