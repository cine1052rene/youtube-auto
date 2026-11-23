#!/usr/bin/env bash
# 스캔 완료 후: 링크 없는 카드 채우기 → 공유 페이지 → 데이터셋·기록 페이지 → 커밋 → ttapp 앞으로
cd /c/project/youtube/challenges/daily_soul
PY=/c/Users/cine1/AppData/Local/Programs/Python/Python312/python.exe
export PYTHONIOENCODING=utf-8
echo "[$(date +%T)] fill"; HERE=1 $PY -u tools/hof_fill.py
echo "[$(date +%T)] share_fetch"; $PY tools/share_fetch.py
$PY tools/build_dataset.py; $PY tools/build_archive.py
git add data/*.jsonl data/*.csv tools && git commit -qm "명예의 전당 스크롤 스캔으로 당선작 날짜 재정리 + 누락 카드 보충 $(date +%F)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q
echo "[$(date +%T)] ALL DONE"; $PY tools/front_ttapp.py
