#!/usr/bin/env bash
cd /c/project/youtube/challenges/daily_soul
PY=/c/Users/cine1/AppData/Local/Programs/Python/Python312/python.exe
export PYTHONIOENCODING=utf-8
echo "[$(date +%T)] crawl continue (here)"; $PY tools/hof_crawl.py --here "Sep 14"
echo "[$(date +%T)] crawl newest"; $PY tools/hof_crawl.py "Nov 14"
echo "[$(date +%T)] share_fetch"; $PY tools/share_fetch.py
$PY tools/build_dataset.py; $PY tools/build_archive.py
git add data/*.jsonl data/*.csv tools && git commit -qm "아카이브 수집 이어서 $(date +%F)" && git push -q
echo "[$(date +%T)] ALL DONE"; $PY tools/front_ttapp.py
