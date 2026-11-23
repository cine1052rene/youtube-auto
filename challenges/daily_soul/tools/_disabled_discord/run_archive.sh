#!/usr/bin/env bash
# 전체 기록 수집: 당선 카드·링크 → 공유 페이지 프롬프트 → 우리 결과 URL·원본 → 기록 페이지 → 커밋 → ttapp 맨 앞으로
cd /c/project/youtube/challenges/daily_soul
PY=/c/Users/cine1/AppData/Local/Programs/Python/Python312/python.exe
export PYTHONIOENCODING=utf-8
echo "[$(date +%T)] crawl start"; $PY tools/hof_crawl.py "${1:-Sep 14}"
echo "[$(date +%T)] share_fetch"; $PY tools/share_fetch.py
for i in $(seq 1 60); do grep -q DONE /tmp/fetch_ours.log 2>/dev/null && break; sleep 30; done
echo "[$(date +%T)] fetch_ours"; $PY tools/fetch_ours.py
echo "[$(date +%T)] fetch_orig"; $PY tools/fetch_orig.py
$PY tools/build_dataset.py; $PY tools/build_archive.py
git add data/*.jsonl data/*.csv tools && git commit -qm "아카이브 수집 $(date +%F)" && git push -q
echo "[$(date +%T)] ALL DONE"; $PY tools/front_ttapp.py
