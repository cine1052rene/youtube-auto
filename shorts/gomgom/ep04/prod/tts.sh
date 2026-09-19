#!/usr/bin/env bash
# 4화 Luna 내레이션 생성 (있는 파일은 건너뜀)
set -u
cd "$(dirname "$0")"
OUT=../audio/luna
VOICE=375a3398-e3b4-4f91-845d-42181e352899
mkdir -p "$OUT"
python - <<'PY' > /tmp/ep04_lines.tsv
import json
d=json.load(open("../lines.json",encoding="utf-8"))
for s in d["shots"]:
    print(s["id"]+"\t"+s["narrator"])
PY
while IFS=$'\t' read -r id text; do
  f="$OUT/$id.mp3"
  [ -s "$f" ] && { echo "건너뜀 $f"; continue; }
  for try in 1 2 3 4 5; do
    jid=$(higgsfield generate create text2speech_v2 --prompt "$text" --variant elevenlabs --voice_id "$VOICE" --voice_type preset --json </dev/null 2>&1 | python -c "import sys,json
try:
  d=json.loads(sys.stdin.read()); print(d[0] if isinstance(d,list) else '')
except Exception: print('')")
    [ -n "$jid" ] && break
    sleep 20
  done
  [ -z "$jid" ] && { echo "실패 $id"; continue; }
  url=$(higgsfield generate wait "$jid" --json </dev/null 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('result_url',''))")
  [ -n "$url" ] && curl -s -o "$f" "$url" && echo "완료 $f" || echo "다운로드 실패 $id"
done < /tmp/ep04_lines.tsv
echo "TTS DONE"
