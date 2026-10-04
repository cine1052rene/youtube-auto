#!/usr/bin/env bash
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
for ep in 02 03; do
  python make_sample.py $ep 1.25 C2_end --hook --end 2.0
  python make_sample.py $ep 1.25 H_peep_end --hook --sfx --sfxset peep --end 2.0
done
echo "ALL DONE"
