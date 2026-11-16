# 명예의 전당(hall-of-fame)을 아래(최신)→위(과거)로 훑으며 당선 카드마다 원래 게시물로 이동해 공유 링크를 복사
# 결과: data/hof_raw.jsonl  ({type:card,user,link,abs_y} / {type:header,text,abs_y})  — 재실행 시 이미 받은 링크는 건너뜀
import sys, os, re, json, time, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsc
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'hof_raw.jsonl')
HERE = '--here' in sys.argv
ARGS = [a for a in sys.argv[1:] if a != '--here']
STOP_DATE = ARGS[0] if ARGS else 'Sep 14'   # 이 날짜 헤더를 지나면 멈춤
MON = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*\d{1,2}'
seen_links = set(); seen_keys = set()
if os.path.exists(OUT):
    for l in open(OUT, encoding='utf-8'):
        r = json.loads(l)
        if r.get('link'): seen_links.add(r['link'])
def log(**r):
    with open(OUT, 'a', encoding='utf-8', newline='\n') as f: f.write(json.dumps(r, ensure_ascii=False) + '\n')
def in_hof(L):
    return any('hall-of-fame' in l[4] for l in L if l[1] < 75 and 300 < l[0] < 700)
def is_band(c): return c[2] > c[0] + 18 and c[2] > 55
CARD_DIR = os.path.join(ROOT, 'data', 'archive', 'winners_card'); os.makedirs(CARD_DIR, exist_ok=True)
def save_card(word, tag):
    import urllib.request
    dsc.front(); dsc.clk(word[0] + 150, word[1] + 170); time.sleep(2.0)
    L1, _ = dsc.ocr(dsc.cap('C:/tmp/_v.png'))
    if in_hof(L1):   # 뷰어가 안 열림
        return ''
    dsc.clk(1824, 56); time.sleep(1.2)
    L2, _ = dsc.ocr(dsc.cap('C:/tmp/_cm.png'))
    it = [l for l in L2 if l[0] > 1600 and l[1] < 300 and ('미디어' in l[4] or '링크' in l[4])]
    u = ''
    if it:
        dsc.clk(it[0][0] + it[0][2] // 2, it[0][1] + it[0][3] // 2); time.sleep(0.6); u = dsc.clip()
    dsc.clk(1876, 56); time.sleep(1.2)
    if 'cdn.discordapp' not in u: return ''
    try:
        d = urllib.request.urlopen(urllib.request.Request(u.split()[0], headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read()
        fp = os.path.join(CARD_DIR, tag + '.png'); open(fp, 'wb').write(d)
        return os.path.relpath(fp, ROOT).replace(os.sep, '/')
    except Exception as e:
        print('carderr', e, flush=True); return ''
def get_link(word):
    dsc.front(); dsc.clk(word[0] + word[2] // 2, word[1] + word[3] // 2)
    band = []
    for _ in range(12):
        time.sleep(0.4)
        p = dsc.cap('C:/tmp/_j.png'); im = Image.open(p).convert('RGB')
        band = [y for y in range(85, 960) if is_band(im.getpixel((1500, y)))]
        if band and not any('hall-of-fame' in t for t in []): break
    if band: time.sleep(0.6); p = dsc.cap('C:/tmp/_j.png')
    link = None
    if band:
        L, W = dsc.ocr(p)
        urls = [l for l in L if 'higgsfield' in l[4] and band[0] - 8 <= l[1] <= band[-1]]
        if urls:
            u = urls[0]; dsc.clk(u[0] + 40, u[1] + u[3] // 2, right=True); time.sleep(0.9)
            L2, _ = dsc.ocr(dsc.cap('C:/tmp/_m.png'))
            items = [l for l in L2 if '링크' in l[4] and ('하기' in l[4] or '복사하' in l[4]) and '메시지' not in l[4] and '매시지' not in l[4]]
            if items:
                it = items[0]; dsc.clk(it[0] + it[2] // 2, it[1] + it[3] // 2); time.sleep(0.4)
                c = dsc.clip()
                if 'higgsfield.ai/s/' in c: link = c.split()[0]
            if not link:
                m = re.search(r'higgsfield\.ai/s/(\S+)', u[4]); link = ('https://higgsfield.ai/s/' + m.group(1)) if m else None
                dsc.clk(1500, 500)  # 메뉴 닫기 (빈 곳)
    if not link:  # FAILSHOT
        import shutil; shutil.copy('C:/tmp/_j.png', 'C:/tmp/fail_%d.png' % int(time.time()))
    for _ in range(3):
        dsc.front(); dsc.clk(24, 15); time.sleep(1.8)
        L, _ = dsc.ocr(dsc.cap())
        if in_hof(L): break
    return link, bool(band)
dsc.front(); time.sleep(0.5)
L0, _ = dsc.ocr(dsc.cap())
if not in_hof(L0): dsc.clk(1876, 56); time.sleep(1.2)
dsc.clk(1500, 200); time.sleep(0.5)
L0, _ = dsc.ocr(dsc.cap())
if not in_hof(L0):
    side = [l for l in L0 if l[0] < 300 and 'hall-of-fame' in l[4]]
    if side: dsc.clk(side[0][0] + 40, side[0][1] + side[0][3] // 2); time.sleep(3)
dsc.clk(1500, 200); time.sleep(0.4)
for _ in range(0 if HERE else 6):
    Lb, _ = dsc.ocr(dsc.cap())
    bt = [l for l in Lb if '최근으로' in l[4]]
    if bt: dsc.clk(bt[0][0] + bt[0][2] // 2, bt[0][1] + bt[0][3] // 2); time.sleep(2.5); break
    dsc.scroll(1100, 500, -20000); time.sleep(1.2)
for _ in range(0 if HERE else 5):
    dsc.scroll(1100, 500, -20000); time.sleep(1.0)
time.sleep(2)
offset = 0; prev = None; stuck = 0; done = False; last = 'start'
while not done:
    L, W = dsc.ocr(dsc.cap())
    for _t in range(3):
        if in_hof(L): break
        dsc.front(); time.sleep(0.8); dsc.clk(1500, 200); time.sleep(0.3)
        if _t > 0: dsc.clk(24, 15); time.sleep(2)
        L, W = dsc.ocr(dsc.cap())
    if not in_hof(L):
        print('not in hall-of-fame; stop', flush=True); break
    body = [l for l in L if 370 < l[0] < 1300 and 80 < l[1] < 960]
    if prev is not None:
        d = [b[1] - a[1] for a in prev for b in body if a[4] == b[4] and len(a[4]) > 10]
        if d:
            md = statistics.median(d); offset += md
            if last == 'scroll': stuck = stuck + 1 if md == 0 else 0
        else: print('no overlap match; offset may drift', flush=True)
    prev = body
    items = []
    for l in body:
        if '@' in l[4] and 'daily' in l[4]:
            m = re.search(r'@\s*([^\s#]+)', l[4]); user = m.group(1) if m else '?'
            ws = [w for w in W if 'daily' in w[4] and abs(w[1] - l[1]) < 8 and l[0] <= w[0] <= l[0] + l[2]]
            if ws: items.append(('card', l[1], user, ws[0]))
        elif re.search(MON, l[4]) and ('·' in l[4] or '•' in l[4] or ' - ' in l[4]):
            items.append(('header', l[1], l[4], None))
    for kind, y, txt, w in sorted(items, key=lambda t: -t[1]):
        key = (kind, txt, round((y - offset) / 40))
        if key in seen_keys: continue
        seen_keys.add(key)
        if kind == 'header':
            log(type='header', text=txt, abs_y=y - offset); print('HEADER', txt, flush=True)
            if re.search(STOP_DATE.replace(' ', r'\s*') + r'\b', txt): done = True
        else:
            if y > 760:
                seen_keys.discard(key); dsc.front(); dsc.scroll(1100, 500, -360); time.sleep(1.5); last = 'card'; break
            card = save_card(w, 'tmp_%d' % int(time.time()))
            link, ok = get_link(w)
            if not link:
                time.sleep(1); L3, W3 = dsc.ocr(dsc.cap())
                w2 = [x for x in W3 if 'daily' in x[4] and abs(x[1] - w[1]) < 30]
                if w2: link, ok = get_link(w2[0])
            if link and link in seen_links: print('dup', txt, link, flush=True); continue
            if card and link:
                newp = os.path.join(CARD_DIR, link.rstrip('/').split('/')[-1] + '.png'); os.replace(os.path.join(ROOT, card), newp); card = os.path.relpath(newp, ROOT).replace(os.sep, '/')
            log(type='card', user=txt, link=link, card=card, abs_y=y - offset, band=ok); seen_links.add(link)
            print('CARD', txt, link, flush=True)
            last = 'card'
            break
    else:
        dsc.front(); dsc.scroll(1100, 500, 480); time.sleep(1.8); last = 'scroll'
        if stuck > 15: print('top reached', flush=True); break
        continue
    # 카드 하나 처리 후 같은 화면 다시 OCR (offset 유지 위해 prev 재설정)
    L2, _ = dsc.ocr(dsc.cap()); prev = [l for l in L2 if 370 < l[0] < 1300 and 80 < l[1] < 960]
print('END', flush=True)
