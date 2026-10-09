#!/usr/bin/env bash
cd "$(dirname "$0")"; source env.sh
(cd ep07/prod && bash generate.sh img 02 08 12)
(cd ep08/prod && bash generate.sh img 07 08 10)
echo "그림 끝"
