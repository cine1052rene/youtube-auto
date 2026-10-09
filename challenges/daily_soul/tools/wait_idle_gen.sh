#!/usr/bin/env bash
# 사용: wait_idle_gen.sh <date/sub> [idle_min]
# 다른 프로젝트의 Higgsfield 작업이 끝날 때까지(진행 중 0개 + 마지막 작업 생성 후 idle_min분 경과) 기다렸다가 gen_daily.sh 실행
SUB=$1; IDLE=${2:-6}
cd /c/project/youtube/challenges/daily_soul
while true; do
  st=$(higgsfield generate list --json </dev/null 2>/dev/null | python -c "
import sys,json,datetime
d=json.load(sys.stdin); it=d if isinstance(d,list) else d.get('items') or d.get('jobs') or d.get('data') or []
busy=any(j.get('status') in ('in_progress','queued','pending') for j in it[:10])
t=max(datetime.datetime.fromisoformat(j['created_at'].replace('Z','+00:00')) for j in it[:10])
age=(datetime.datetime.now(datetime.timezone.utc)-t).total_seconds()/60
print('busy' if busy else ('idle' if age>=$IDLE else 'recent'), round(age,1))
" 2>/dev/null)
  echo "[$(date +%H:%M:%S)] $st"
  case "$st" in idle*) break;; esac
  sleep 60
done
echo "[$(date +%H:%M:%S)] 유휴 확인 → 생성 시작"
bash gen_daily.sh "$SUB"
echo "[$(date +%H:%M:%S)] FINISHED"
