# 기록 페이지 생성: data/archive/index.html + data/archive/days/YYYY-MM-DD.html
# 당선작(이미지·프롬프트·모델·공유 링크) + 우리 생성물(이미지·프롬프트·모델·원본 링크·작업ID) + 그날 concepts.md(채점·메모)
import os, re, json, html, glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'data', 'archive'); os.makedirs(os.path.join(A, 'days'), exist_ok=True)
def jl(name):
    p = os.path.join(ROOT, 'data', name)
    return [json.loads(l) for l in open(p, encoding='utf-8')] if os.path.exists(p) else []
MON = {m: i for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}
def hdr_date(t):
    m = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2})', t)
    return f'2026-{MON[m.group(1)]:02d}-{int(m.group(2)):02d}' if m else None
# --- 당선작: 크롤 순서(아래→위)에서 카드 다음에 나오는 헤더가 그 카드들의 날짜
share = {r['link']: r for r in jl('winners_share.jsonl') if r.get('link')}
win, buf, themes, wlist = {}, [], {}, {}
SCAN = jl('hof_scan.jsonl')
if SCAN:   # 스크롤 스캔(클릭 없이 순서 그대로) 결과 우선
    for r in SCAN:
        if r['type'] == 'card': buf.append(r)
        else:
            d = hdr_date(r.get('date') or r['text'])
            if d and d not in win:
                names = [re.sub(r'[^a-z0-9]', '', n.lower())[:4] for n in re.findall(r'@\s*([^\s@모]+)', ' '.join(r.get('winners') or []))]
                if names and len(buf) > len(names):   # 발표 명단에 없는 맨 아래쪽 카드 = 다음 날(헤더가 스레드에만 올라온 날)
                    ok = lambda c: re.sub(r'[^a-z0-9]', '', c['user'].lower())[:4] in names
                    k = 0
                    while k < len(buf) and not ok(buf[k]): k += 1
                    if k:
                        nd = (datetime.date.fromisoformat(d) + datetime.timedelta(days=1)).isoformat()
                        win.setdefault(nd, []).extend(buf[:k]); themes.setdefault(nd, '(발표 헤더가 스레드에만 있음)'); buf = buf[k:]
                themes[d] = re.sub(r'\s*[·•\-]\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*', '', r['text']).strip()
                wlist[d] = ' '.join(r.get('winners') or [])
                win[d] = buf
            buf = []
else:
    for r in jl('hof_raw.jsonl'):
        if r['type'] == 'card':
            if r.get('link') and all(b.get('link') != r['link'] for b in buf): buf.append(r)
        else:
            d = hdr_date(r['text'])
            if d:
                themes[d] = re.sub(r'\s*[·•\-]\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*', '', r['text']).strip()
                seen = {x['link'] for x in win.get(d, [])}
                win.setdefault(d, []).extend(b for b in buf if b['link'] not in seen)
            buf = []
for d in win: win[d] = list(reversed(win[d]))   # 화면 위→아래(발표 순서)
# 당선 점수 줄(JUDGING.md)
judg = open(os.path.join(ROOT, 'winners', 'JUDGING.md'), encoding='utf-8').read() if os.path.exists(os.path.join(ROOT, 'winners', 'JUDGING.md')) else ''
def judging_line(d):
    md = f'{int(d[5:7])}/{int(d[8:10])} '
    return [l for l in judg.splitlines() if l.startswith('| ' + md)]
# --- 우리 것
res = {r['job_id']: r for r in jl('our_results.jsonl')}
ours = {}
for r in jl('our_prompts.jsonl'):
    ours.setdefault(r['date'], []).append({**r, **res.get(r['job_id'], {})})
CSS = '''body{font-family:system-ui,'Malgun Gothic',sans-serif;background:#111;color:#ddd;margin:0;padding:16px;max-width:1400px}
a{color:#7cf}h1,h2{color:#fff}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.c{background:#1c1c1f;border-radius:10px;padding:10px}.c img{width:100%;border-radius:6px;display:block}
.m{font-size:12px;color:#aaa;margin:6px 0}.p{font-size:12px;white-space:pre-wrap;max-height:160px;overflow:auto;background:#0b0b0d;padding:6px;border-radius:6px}
pre{white-space:pre-wrap;font-size:12px;background:#0b0b0d;padding:10px;border-radius:8px;overflow:auto}
.win{border:2px solid #e8c547}.tag{display:inline-block;background:#333;border-radius:4px;padding:1px 6px;margin-right:4px}'''
def card(img, title, meta, prompt, links, win=False):
    im = f'<a href="{html.escape(links[0][1] or img)}" target="_blank"><img loading="lazy" src="{html.escape(img)}"></a>' if img else '<div class="m">(이미지 없음)</div>'
    ln = ' · '.join(f'<a href="{html.escape(u)}" target="_blank">{t}</a>' for t, u in links if u)
    return f'<div class="c{" win" if win else ""}">{im}<div><b>{html.escape(title)}</b></div><div class="m">{meta}</div><div class="m">{ln}</div><div class="p">{html.escape(prompt or "")}</div></div>'
days = sorted(set(ours) | set(win))
idx = []
for d in days:
    cm = os.path.join(ROOT, d, 'concepts.md')
    concepts = open(cm, encoding='utf-8').read() if os.path.exists(cm) else ''
    m0 = re.match(r'#\s*\S+\s+(.*)', concepts.splitlines()[0]) if concepts else None
    theme = (m0.group(1) if m0 else '') or themes.get(d, '')
    W = win.get(d, []); O = ours.get(d, [])
    parts = [f'<p><a href="../index.html">← 목차</a></p><h1>{d} {html.escape(theme)}</h1>']
    parts.append(f'<h2>🏆 당선작 ({len(W)})</h2>')
    if wlist.get(d): parts.append(f'<div class="m">발표 명단(OCR): {html.escape(wlist[d])}</div>')
    for jline in judging_line(d): parts.append(f'<pre>{html.escape(jline)}</pre>')
    parts.append('<div class="grid">')
    for w in W:
        s = share.get(w.get('link'), {})
        img = ('../' + w['card'].split('archive/', 1)[1]) if w.get('card') else (('../' + s['thumb'].split('archive/', 1)[1]) if s.get('thumb') else s.get('image_url', ''))
        parts.append(card(img, '@' + w['user'], f'<span class="tag">{html.escape(s.get("model", ""))}</span>', s.get('prompt', ''), [('공유 페이지(프롬프트·원본)', w.get('link') or ''), ('카드 원본(PC)', img if w.get('card') else '')], True))
    parts.append('</div>')
    parts.append(f'<h2>🎨 우리 생성물 ({len(O)})</h2><div class="grid">')
    for o in O:
        img = '../' + o['thumb'].split('archive/', 1)[1] if o.get('thumb') else (o.get('min_result_url') or '')
        meta = f'<span class="tag">{o["set"]}#{o["idx"]}</span><span class="tag">{o["model"]}</span>' + ('<span class="tag">실패</span>' if o.get('failed') else '') + f' job {o["job_id"][:8]}'
        loc = f"../ours_orig/{d}/{o['set'].replace('/', '_').replace('.', 'root')}_{o['idx']:02d}.png"
        parts.append(card(img, f'{o["set"]} #{o["idx"]}', meta, o['prompt'], [('원본 링크(온라인)', o.get('result_url') or ''), ('원본 파일(PC)', loc if os.path.exists(os.path.join(A, loc[3:])) else '')]))
    parts.append('</div>')
    if concepts: parts.append(f'<h2>📝 기획·채점·하트 기록 (concepts.md)</h2><pre>{html.escape(concepts)}</pre>')
    open(os.path.join(A, 'days', d + '.html'), 'w', encoding='utf-8').write(f'<!doctype html><meta charset="utf-8"><title>{d}</title><style>{CSS}</style>' + ''.join(parts))
    won = '🏆' if any(w['user'].lower().startswith('t100roxy') for w in W) else ''
    idx.append(f'<tr><td><a href="days/{d}.html">{d}</a></td><td>{html.escape(theme)} {won}</td><td>{len(W)}</td><td>{len(O)}</td></tr>')
open(os.path.join(A, 'index.html'), 'w', encoding='utf-8').write(
    f'<!doctype html><meta charset="utf-8"><title>Daily Soul 기록</title><style>{CSS} td,th{{padding:4px 10px;border-bottom:1px solid #333;text-align:left}}</style>'
    f'<h1>Higgsfield Daily Soul 기록 (T100roxy / cinesilver)</h1><p class="m">생성 {datetime.datetime.now():%Y-%m-%d %H:%M} · 당선작은 공유 페이지에서 원본 확인, 우리 것은 원본 이미지 링크</p>'
    '<table><tr><th>날짜</th><th>주제</th><th>당선작</th><th>우리 생성물</th></tr>' + ''.join(reversed(idx)) + '</table>')
print(len(days), 'days;', sum(len(v) for v in win.values()), 'winners;', sum(len(v) for v in ours.values()), 'ours')
