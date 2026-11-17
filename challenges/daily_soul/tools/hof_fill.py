# 2차: hof_scan.jsonl에서 링크가 없는 카드만 찾아가서 카드 원본(뷰어 다운로드)·공유 링크(원래 게시물 점프)를 받는다.
# 화면의 카드는 그림 비교로 식별, 위치는 날짜 헤더를 보고 위/아래 방향을 정한다. 결과는 hof_scan.jsonl에 덮어씀.
import sys, os, re, json, time, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsc
from PIL import Image
import hof_scan_lib as H
ROOT = H.ROOT
SCAN = os.path.join(ROOT, 'data', 'hof_scan.jsonl')
rows = [json.loads(l) for l in open(SCAN, encoding='utf-8')]
# 날짜 붙이기: 카드 다음에 나오는 헤더가 그 카드의 날짜
buf = []
for r in rows:
    if r['type'] == 'card': buf.append(r)
    else:
        for b in buf: b['date'] = r['date']
        buf = []
def dkey(d):
    m = re.match(r'(\w+) (\d+)', d or ''); return (H.MONN.get(m.group(1), 0), int(m.group(2))) if m else (0, 0)
targets = [r for r in rows if r['type'] == 'card' and not r.get('link') and r.get('date')]
for t in targets: t['_th'] = H.thumb(Image.open(os.path.join(ROOT, t['card'])).convert('RGB'))
print('targets', len(targets), flush=True)
def save():
    with open(SCAN, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows: f.write(json.dumps({k: v for k, v in r.items() if k != '_th'}, ensure_ascii=False) + '\n')
if not os.environ.get("HERE"): H.go_bottom()
direction = 420; fails = {}; last_fill = time.time(); prevsig = None; same = 0
t_end = time.time() + 3 * 3600
while time.time() < t_end:
    todo = [t for t in targets if not t.get('link') and fails.get(id(t), 0) < 3]
    if not todo: break
    dsc.front(); p = dsc.cap('C:/tmp/_f.png'); im = Image.open(p).convert('RGB'); L, W = dsc.ocr(p)
    if not H.in_hof(L):
        dsc.clk(1876, 56); time.sleep(1); dsc.clk(24, 15); time.sleep(2); continue
    body = [l for l in L if 370 < l[0] < 1300 and 80 < l[1] < 960]
    if time.time() - last_fill > 1500: print('no progress 25min; stop', flush=True); break
    sig = tuple(l[4] for l in body[:6]); same = same + 1 if sig == prevsig else 0; prevsig = sig
    if same >= 4: direction = -direction; same = 0; print('flip', direction, flush=True)
    hit = None
    for l in body:
        if '@' in l[4] and 'daily' in l[4]:
            box = H.card_box(im, l[1] + l[3])
            if not box: continue
            th = H.thumb(im.crop(box))
            for t in todo:
                if H.dist(th, t['_th']) < 10:
                    ws = [w for w in W if 'daily' in w[4] and abs(w[1] - l[1]) < 8]
                    if ws: hit = (t, ws[0]); break
        if hit: break
    if hit:
        t, w = hit
        card = H.save_card(w, t['card'].split('/')[-1].replace('.png', '') + '_full')
        link, ok = H.get_link(w, t['user'])
        if link:
            t['link'] = link
            if card:
                newp = os.path.join(H.CARD_DIR, link.rstrip('/').split('/')[-1] + '.png'); os.replace(os.path.join(ROOT, card), newp)
                t['card'] = os.path.relpath(newp, ROOT).replace(os.sep, '/')
            print('FILLED', t['date'], t['user'], link, t['card'], flush=True); save(); last_fill = time.time()
        else:
            fails[id(t)] = fails.get(id(t), 0) + 1; print('fail', t['date'], t['user'], flush=True)
            if card and fails[id(t)] == 1: t['card_full'] = card; save()
        time.sleep(1); continue
    # 방향 결정: 화면의 날짜 헤더 vs 남은 대상 중 가장 가까운 날짜
    hd = [dkey(re.search(H.MON, l[4]).group(1) + ' ' + str(int(re.search(H.MON, l[4]).group(2)))) for l in body if re.search(H.MON, l[4]) and ('•' in l[4] or '·' in l[4]) and '@' not in l[4]]
    if hd:
        cur = max(hd); want = [dkey(t['date']) for t in todo]
        if all(k > cur for k in want): direction = -420   # 대상이 더 최신 → 아래로
        elif all(k < min(hd) for k in want): direction = 420  # 더 과거 → 위로
    dsc.scroll(1100, 500, direction); time.sleep(1.6)
save()
left = [t for t in targets if not t.get('link')]
print('END filled', len(targets) - len(left), 'left', len(left), flush=True)
