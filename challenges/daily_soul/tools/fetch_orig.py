# 원본 이미지 내려받기 (당선작 image_url, 우리 result_url) — 이미 있으면 건너뜀
# 결과: data/archive/winners_orig/<공유ID>.<확장자>, data/archive/ours_orig/<date>/<set>_<idx>.<확장자>
import os, json, urllib.request, concurrent.futures as cf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def jl(n):
    p = os.path.join(ROOT, 'data', n)
    return [json.loads(l) for l in open(p, encoding='utf-8')] if os.path.exists(p) else []
jobs = []
for r in jl('winners_share.jsonl'):
    if r.get('image_url'):
        ext = os.path.splitext(r['image_url'].split('?')[0])[1] or '.png'
        jobs.append((r['image_url'], os.path.join(ROOT, 'data', 'archive', 'winners_orig', r['id'] + ext)))
res = {r['job_id']: r for r in jl('our_results.jsonl')}
for r in jl('our_prompts.jsonl'):
    u = (res.get(r['job_id']) or {}).get('result_url')
    if u:
        ext = os.path.splitext(u.split('?')[0])[1] or '.png'
        name = f"{r['set'].replace('/', '_').replace('.', 'root')}_{r['idx']:02d}{ext}"
        jobs.append((u, os.path.join(ROOT, 'data', 'archive', 'ours_orig', r['date'], name)))
def dl(j):
    u, p = j
    if os.path.exists(p) and os.path.getsize(p) > 1000: return 'skip'
    os.makedirs(os.path.dirname(p), exist_ok=True)
    try:
        urllib.request.urlretrieve(u, p + '.part'); os.replace(p + '.part', p); return 'ok'
    except Exception as e:
        return 'err ' + str(e)[:60]
with cf.ThreadPoolExecutor(6) as ex:
    st = {}
    for i, r in enumerate(ex.map(dl, jobs)):
        k = r.split()[0]; st[k] = st.get(k, 0) + 1
        if i % 100 == 0: print(i, len(jobs), st, flush=True)
print('DONE', st, flush=True)
