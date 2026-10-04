#!/usr/bin/env bash
# 2·3화 비교 샘플 10개 조립 (크레딧 0) — 음악 생성이 끝날 때까지 기다린 뒤 시작
set -u
cd "$(dirname "$0")"
for i in $(seq 1 60); do ls ../sound/bgm/bgm_b.* >/dev/null 2>&1 && break; sleep 10; done
BA=$(ls ../sound/bgm/bgm_a.* | head -1); BB=$(ls ../sound/bgm/bgm_b.* 2>/dev/null | head -1)
for ep in 02 03; do
  cp ../ep$ep/prod/out/ep${ep}_preview.mp4 out/ep${ep}_A_orig.mp4
  python make_sample.py $ep 1.15 B_115 --hook
  python make_sample.py $ep 1.25 C_125 --hook
  python make_sample.py $ep 1.35 D_135 --hook
  python make_sample.py $ep 1.25 E_125_sfx --hook --sfx
  python make_sample.py $ep 1.25 F_125_sfx_bgmA --hook --sfx --bgm "$BA"
  [ -n "$BB" ] && python make_sample.py $ep 1.25 G_125_sfx_bgmB --hook --sfx --bgm "$BB"
done
echo "ALL DONE"
