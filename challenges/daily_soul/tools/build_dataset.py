# 우리 생성 데이터 모으기: 날짜/세트/번호/모델/작업ID/프롬프트 → data/our_prompts.jsonl (+ csv 요약)
# 사용: python tools/build_dataset.py   (daily_soul 폴더에서)
import os, re, json, glob, csv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = []
for day in sorted(glob.glob(os.path.join(ROOT, '2026-*'))):
    date = os.path.basename(day)
    sets = [day] + sorted(d for d in glob.glob(os.path.join(day, '*')) if os.path.isdir(d))
    for s in sets:
        pf = os.path.join(s, 'prompts.txt')
        if not os.path.exists(pf):
            continue
        prompts = [l for l in open(pf, encoding='utf-8', errors='ignore').read().split('\n') if l.strip()]
        model = open(os.path.join(s, 'model.txt')).read().strip() if os.path.exists(os.path.join(s, 'model.txt')) else 'text2image_soul_v2'
        ids, fails = {}, set()
        lg = os.path.join(s, 'gen.log')
        if os.path.exists(lg):
            for l in open(lg, encoding='utf-8', errors='ignore'):
                m = re.search(r'(done|FAIL) cand_(\d+)\.png id=([0-9a-f-]{36})', l)
                if m:
                    ids[int(m.group(2))] = m.group(3)
                    if m.group(1) == 'FAIL':
                        fails.add(int(m.group(2)))
        for i, p in enumerate(prompts, 1):
            png = os.path.join(s, f'cand_{i:02d}.png')
            rows.append({'date': date, 'set': os.path.relpath(s, day).replace('\\', '/') if s != day else '.',
                         'idx': i, 'model': model, 'job_id': ids.get(i, ''), 'failed': i in fails,
                         'png_local': os.path.exists(png), 'prompt': p})
os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
with open(os.path.join(ROOT, 'data', 'our_prompts.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(os.path.join(ROOT, 'data', 'our_prompts.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f); w.writerow(['date', 'set', 'idx', 'model', 'job_id', 'failed', 'png_local', 'prompt_head'])
    for r in rows:
        w.writerow([r['date'], r['set'], r['idx'], r['model'], r['job_id'], r['failed'], r['png_local'], r['prompt'][:120]])
print(len(rows), 'rows;', sum(1 for r in rows if r['job_id']), 'with job_id;', len({r['date'] for r in rows}), 'days')
