#!/usr/bin/env bash
cd "$(dirname "$0")"
while ! grep -q ALLDONE /tmp/img0910.log; do sleep 20; done
PYTHONIOENCODING=utf-8 python tts_verify.py ep09
PYTHONIOENCODING=utf-8 python tts_verify.py ep10
echo TTSDONE
