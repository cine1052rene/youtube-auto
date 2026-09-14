#!/usr/bin/env bash
# 스타일 테스트: 4방향 × 3장면 = 12장 (Soul 2.0 @ 0.12cr = 1.44cr)
set -u
OUT="/c/project/youtube/episodes/ep01/style"

# ── 스타일 4방향 ──────────────────────────────────────────────
SA="traditional East Asian ink wash painting, sumi-e, monochrome black ink on textured rice paper, soft bleeding washes, generous negative space, economical brushstrokes, faint indigo tint, quiet and contemplative"
SB="oil painting with thick impasto brushstrokes, Edward Hopper influence, deep prussian blue night palette with one warm amber light source, visible canvas weave, melancholic stillness, painterly edges"
SC="risograph print, strictly limited 3-color palette of deep indigo, fluorescent coral and bone white, visible halftone grain, slight misregistration, flat graphic shapes, bold negative space, contemporary poster art"
SD="painterly cinematic still, digital matte painting, sits between photography and painting, deep teal-blue night, volumetric light haze, soft focus falloff, subtle film grain, atmospheric depth"

# ── 장면 3종 (에피소드가 실제로 필요로 하는 샷 타입) ──────────
P1="silhouette of a lone person sitting at a window ledge at 3am, vast city lights beyond the glass, seen from behind, face not visible, alone"
P2="empty dark bedroom viewed from the bed looking up, faint stripes of streetlight falling across the ceiling, rumpled sheets, no people"
P3="abstract visualization of nocturnal anxiety, one small human figure dissolving into vast dark negative space, surreal, faceless, overwhelming scale"

declare -A S=( [A]="$SA" [B]="$SB" [C]="$SC" [D]="$SD" )
declare -A P=( [1]="$P1" [2]="$P2" [3]="$P3" )

echo "=== 제출 시작 $(date +%H:%M:%S) ==="
: > "$OUT/jobs.txt"
for s in A B C D; do
  for n in 1 2 3; do
    id=$(higgsfield generate create text2image_soul_v2 \
        --prompt "${P[$n]}, ${S[$s]}" \
        --aspect_ratio "16:9" --quality "2k" --json 2>&1 \
      | python -c "import sys,json;d=json.load(sys.stdin);print(d.get('id') or d.get('job_id') or '')" 2>/dev/null)
    if [ -n "$id" ]; then
      echo "$s$n $id" >> "$OUT/jobs.txt"; echo "  제출 $s$n -> $id"
    else
      echo "  ❌ 실패 $s$n"
    fi
  done
done
echo "=== 제출 완료: $(wc -l < "$OUT/jobs.txt")건 ==="
