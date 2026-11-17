# 명예의 전당을 클릭 없이 스크롤만 하며 순서대로 훑는다 (위치가 흔들리지 않음).
# 화면의 당선 카드 그림을 이미 받아 둔 카드 PNG(data/archive/winners_card)와 그림 비교로 맞춰 링크를 찾고,
# 날짜 헤더(… • Nov 14)와 그 아래 'Today's Winners' 명단을 기록한다.
# 결과: data/hof_scan.jsonl  ({type:header,text,date,winners} / {type:card,user,link,card,dist,score})  아래(최신)→위(과거) 순서
import sys, os, re, json, time, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsc
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'hof_scan.jsonl')
CARD_DIR = os.path.join(ROOT, 'data', 'archive', 'winners_card')
UNM = os.path.join(ROOT, 'data', 'archive', 'winners_card_scan'); os.makedirs(UNM, exist_ok=True)
STOP = sys.argv[1] if len(sys.argv) > 1 else 'Sep 14'
MON = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2})'
TS = (32, 22)
def thumb(im):
    w, h = im.size; m = 0.05
    im = im.crop((int(w * m), int(h * m), int(w * (1 - m)), int(h * (1 - m))))
    return list(ImageOps.grayscale(im).resize(TS, Image.BILINEAR).get_flattened_data())
def dist(a, b): return sum(abs(x - y) for x, y in zip(a, b)) / len(a)
LINKS = {}
for l in open(os.path.join(ROOT, 'data', 'hof_raw.jsonl'), encoding='utf-8'):
    r = json.loads(l)
    if r.get('card') and r.get('link'): LINKS[os.path.basename(r['card'])] = r['link']
REF = []
for p in glob.glob(os.path.join(CARD_DIR, '*.png')):
    try:
        _im = Image.open(p)
        if _im.size == (1920, 1080): continue
        REF.append((os.path.basename(p), thumb(Image.open(p).convert('RGB'))))
    except Exception as e: print('bad', p, e)
print('refs', len(REF), flush=True)
def near(a, b, t=10): return all(abs(x - y) <= t for x, y in zip(a, b))
def card_box(im, y_m):
    """멘션 줄 아래 카드 그림의 경계 (x0,y0,x1,y1) — 화면 안에 다 보이지 않으면 None"""
    H = 965
    bg = lambda y: im.getpixel((1600, y))
    y = y_m + 14
    while y < H and near(im.getpixel((520, y)), bg(y)) and near(im.getpixel((420, y)), bg(y)): y += 1
    if y >= H - 60 or y - y_m > 60: return None
    y0 = y; run = 0
    while y < H:
        if all(near(im.getpixel((x, y)), bg(y)) for x in (400, 470, 560, 650)): run += 1
        else: run = 0
        if run >= 8: break
        y += 1
    if y >= H: return None
    y1 = y - 8
    if y1 - y0 < 120: return None
    ys = list(range(y0 + 4, y1 - 4, 6))
    colbg = lambda x: all(near(im.getpixel((x, yy)), bg(yy)) for yy in ys)
    x = 430; run = 0
    while x < 1500:
        run = run + 1 if colbg(x) else 0
        if run >= 6: break
        x += 1
    x0 = 382
    return (x0, y0, x - 5, y1)
def log(**r):
    with open(OUT, 'a', encoding='utf-8', newline='\n') as f: f.write(json.dumps(r, ensure_ascii=False) + '\n')
# 시작: 맨 아래로
dsc.front(); time.sleep(0.5); dsc.clk(1300, 300); time.sleep(0.4)
_prev = None; _same = 0
for _ in range(80):
    dsc.front(); Lb, _ = dsc.ocr(dsc.cap())
    bt = [l for l in Lb if '최근으로' in l[4]]
    if bt: dsc.clk(bt[0][0] + bt[0][2] // 2, bt[0][1] + bt[0][3] // 2); time.sleep(3); continue
    sg = tuple(l[4] for l in Lb if 370 < l[0] < 1300 and 80 < l[1] < 960)
    _same = _same + 1 if sg == _prev else 0; _prev = sg
    if _same >= 3: break
    dsc.scroll(1100, 500, -20000); time.sleep(1.5)
print('bottom', _same, flush=True)
time.sleep(2)
seen_cards, seen_hdr, unm = set(), set(), []
retry = 0
step = 0; same = 0; prevsig = None; done = False
while not done and step < 1500:
    step += 1
    dsc.front(); p = dsc.cap('C:/tmp/_s.png'); im = Image.open(p).convert('RGB')
    L, W = dsc.ocr(p)
    if os.environ.get('DBG'): im.save('C:/tmp/frames/f%03d.png' % step)
    if not any('hall-of-fame' in l[4] for l in L if l[1] < 75 and 300 < l[0] < 700):
        print('not hall; fix', flush=True); dsc.clk(1876, 56); time.sleep(1); dsc.clk(24, 15); time.sleep(2); continue
    body = sorted([l for l in L if 370 < l[0] < 1300 and 80 < l[1] < 960], key=lambda l: -l[1])
    sig = tuple(l[4] for l in body[:6])
    same = same + 1 if sig == prevsig else 0; prevsig = sig
    if same >= 8: print('top reached', flush=True); break
    need_retry = False
    for l in body:   # 아래→위
        t = l[4]
        m = re.search(MON, t)
        if m and ('•' in t or '·' in t) and '@' not in t:
            date = f'{m.group(1)} {int(m.group(2))}'
            if date in seen_hdr: continue
            wl = [x[4] for x in body if 0 < x[1] - l[1] < 130 and '@' in x[4] and 'daily' not in x[4]]
            seen_hdr.add(date); log(type='header', text=t, date=date, winners=wl)
            print('HEADER', date, '|', t, '|', wl, flush=True)
            if re.fullmatch(STOP.replace(' ', r'\s*'), date.replace(' ', '')) or date == STOP: done = True
        elif '@' in t and 'daily' in t:
            mu = re.search(r'@\s*([^\s#]+)', t); user = mu.group(1) if mu else '?'
            box = card_box(im, l[1] + l[3])
            if os.environ.get('DBG'): print('  m', step, l[1], user, box, flush=True)
            if not box:
                if l[1] < 520 and retry < 2: need_retry = True
                continue
            th = thumb(im.crop(box))
            best = sorted(((dist(th, rt), n) for n, rt in REF))[:4]
            d0, n0 = best[0]
            ok = [b for b in best if b[0] < 14]
            wl_ = [b for b in ok if LINKS.get(b[1])]
            if wl_: d0, n0 = wl_[0]
            if ok:
                if n0 in seen_cards: continue
                seen_cards.add(n0)
                log(type='card', user=user, link=LINKS.get(n0), card='data/archive/winners_card/' + n0, dist=round(d0, 1), box=box)
                print('CARD', user, n0, round(d0, 1), flush=True)
            else:
                if any(dist(th, u) < 10 for u in unm): continue
                unm.append(th); fn = 'scan_%04d.png' % len(unm)
                im.crop(box).save(os.path.join(UNM, fn))
                log(type='card', user=user, link=None, card='data/archive/winners_card_scan/' + fn, dist=round(d0, 1), best=n0, box=box)
                print('UNMATCHED', user, fn, round(d0, 1), n0, flush=True)
    if need_retry:
        retry += 1; time.sleep(1.5); continue
    retry = 0
    dsc.scroll(1100, 500, 420); time.sleep(1.6)
print('END', step, flush=True)
