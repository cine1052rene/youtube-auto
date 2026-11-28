# 수동 수집 반영: 수동수집/YYYY-MM-DD/ 폴더 → data/hof_manual.jsonl + 카드 이미지 + 발표 링크
# 폴더 안:  링크.txt  (발표 줄 1개 + 당선자 줄 최대 5개)  /  카드 이미지 1.png ~ 5.png (링크.txt 당선자 순서)
# 링크.txt 예)
#   주제 Where Lost Things Go
#   발표 https://discord.com/channels/.../.../...
#   @AlezZ https://higgsfield.ai/s/hP4Opm1irNM
#   @willeyumz https://higgsfield.ai/s/baZXmXZbwRc
# 사용: python tools/manual_import.py   (매번 전체를 다시 읽어 hof_manual.jsonl 을 새로 만든다)
import os, re, json, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, '수동수집')
CARD = os.path.join(ROOT, 'data', 'archive', 'winners_card'); os.makedirs(CARD, exist_ok=True)
OUT = os.path.join(ROOT, 'data', 'hof_manual.jsonl')
ANNF = os.path.join(ROOT, 'data', 'announce_links.json')
ann = json.load(open(ANNF, encoding='utf-8')) if os.path.exists(ANNF) else {}
EXT = ('.png', '.jpg', '.jpeg', '.webp')
recs, report = [], []
for d in sorted(os.listdir(INBOX)) if os.path.isdir(INBOX) else []:
    p = os.path.join(INBOX, d)
    if not (os.path.isdir(p) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', d)): continue
    lf = os.path.join(p, '링크.txt')
    lines = open(lf, encoding='utf-8-sig').read().splitlines() if os.path.exists(lf) else []
    people = []
    for ln in lines:
        ln = ln.strip()
        if not ln or ln.startswith('#'): continue
        if ln.startswith('주제'):
            recs.append({'type': 'theme', 'date': d, 'text': ln[2:].strip(' :')}); continue
        disc = re.search(r'https://(?:ptb\.|canary\.)?discord(?:app)?\.com/channels/\S+', ln)
        if disc and ('발표' in ln or not re.search(r'higgsfield\.ai/s/', ln)):
            ann[d] = disc.group(0); continue
        hf = re.search(r'https://higgsfield\.ai/s/[\w\-]+', ln)
        user = re.search(r'@\s*([^\s]+)', ln)
        if hf or user:
            people.append({'user': (user.group(1) if user else '').strip(), 'link': hf.group(0) if hf else ''})
    imgs = sorted([f for f in os.listdir(p) if f.lower().endswith(EXT)], key=lambda f: (not f.split('.')[0].isdigit(), int(f.split('.')[0]) if f.split('.')[0].isdigit() else 0, f))
    n = max(len(people), len(imgs))
    for i in range(n):
        pe = people[i] if i < len(people) else {'user': '', 'link': ''}
        card = ''
        if i < len(imgs):
            sid = pe['link'].rstrip('/').split('/')[-1] if pe['link'] else f'manual_{d}_{i+1}'
            dst = os.path.join(CARD, sid + '.png')
            Image.open(os.path.join(p, imgs[i])).convert('RGB').save(dst)
            card = os.path.relpath(dst, ROOT).replace('\\', '/')
        recs.append({'type': 'card', 'user': pe['user'] or f'(이름없음{i+1})', 'link': pe['link'], 'card': card, 'date': d, 'manual': True})
    report.append(f'{d}: 당선자 {len(people)}명 · 카드 이미지 {len(imgs)}장 · 발표 링크 {"있음" if d in ann else "없음"}')
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    for r in recs: f.write(json.dumps(r, ensure_ascii=False) + '\n')
json.dump(dict(sorted(ann.items())), open(ANNF, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
sys.stdout.reconfigure(encoding='utf-8')
print('\n'.join(report) or '수동수집 폴더에 날짜 폴더가 없습니다'); print(f"→ 수동 카드 {sum(r['type'] == 'card' for r in recs)}건 반영")
