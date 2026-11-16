# data/our_prompts.jsonl 의 job_id 마다 higgsfield generate get → 원본/축소본 URL·시드 기록 + 축소본(webp) 저장
# 결과: data/our_results.jsonl, data/archive/ours/<date>/<set>_<idx>.webp  (이미 있으면 건너뜀 → 재실행 안전)
import os, json, subprocess, urllib.request, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HF = os.path.join(os.environ.get('APPDATA', ''), 'npm', 'higgsfield.cmd')
src = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'our_prompts.jsonl'), encoding='utf-8')]
outp = os.path.join(ROOT, 'data', 'our_results.jsonl')
done = {}
if os.path.exists(outp):
    for l in open(outp, encoding='utf-8'):
        r = json.loads(l); done[r['job_id']] = r
with open(outp, 'a', encoding='utf-8', newline='\n') as out:
    for n, r in enumerate(src):
        jid = r['job_id']
        if not jid or jid in done:
            continue
        try:
            j = json.loads(subprocess.run([HF, 'generate', 'get', jid, '--json'], capture_output=True, text=True, encoding='utf-8', timeout=60, stdin=subprocess.DEVNULL).stdout)
        except Exception as e:
            print('ERR', jid, e, flush=True); continue
        rec = {'job_id': jid, 'status': j.get('status'), 'result_url': j.get('result_url'), 'min_result_url': j.get('min_result_url'),
               'seed': (j.get('params') or {}).get('seed'), 'created_at': j.get('created_at')}
        thumb = ''
        if rec['min_result_url']:
            d = os.path.join(ROOT, 'data', 'archive', 'ours', r['date']); os.makedirs(d, exist_ok=True)
            thumb = os.path.join(d, f"{r['set'].replace('/', '_').replace('.', 'root')}_{r['idx']:02d}.webp")
            if not os.path.exists(thumb):
                try:
                    urllib.request.urlretrieve(rec['min_result_url'], thumb)
                except Exception as e:
                    print('DLERR', jid, e, flush=True); thumb = ''
        rec['thumb'] = os.path.relpath(thumb, ROOT).replace('\\', '/') if thumb else ''
        out.write(json.dumps(rec, ensure_ascii=False) + '\n'); out.flush()
        if n % 50 == 0:
            print(n, '/', len(src), time.strftime('%H:%M:%S'), flush=True)
print('DONE', flush=True)
