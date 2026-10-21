#!/usr/bin/env bash
cd "$(dirname "$0")"
bash ep09/prod/generate.sh img
bash ep10/prod/generate.sh img
echo ALLDONE
