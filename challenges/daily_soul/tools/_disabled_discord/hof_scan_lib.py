# hof_scan / hof_fill 공용 함수
import sys, os, re, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dsc
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_DIR = os.path.join(ROOT, 'data', 'archive', 'winners_card')
MON = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2})'
MONN = {m: i for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 1)}
TS = (32, 22)
def thumb(im):
    w, h = im.size; m = 0.05
    im = im.crop((int(w * m), int(h * m), int(w * (1 - m)), int(h * (1 - m))))
    return list(ImageOps.grayscale(im).resize(TS, Image.BILINEAR).get_flattened_data())
def dist(a, b): return sum(abs(x - y) for x, y in zip(a, b)) / len(a)
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
def in_hof(L):
    return any('hall-of-fame' in l[4] for l in L if l[1] < 75 and 300 < l[0] < 700)
def is_band(c): return (c[2] > c[0] + 18 and c[2] > 55) or (36 <= c[0] <= 60 and abs(c[0] - c[2]) <= 8 and abs(c[0] - c[1]) <= 6)
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
def get_link(word, user=None):
    dsc.front(); dsc.clk(word[0] + word[2] // 2, word[1] + word[3] // 2)
    band = []
    time.sleep(0.3); dsc.u.SetCursorPos(200, 1000)   # 마우스 올림 회색 강조와 구분
    for _ in range(12):
        time.sleep(0.4)
        p = dsc.cap('C:/tmp/_j.png'); im = Image.open(p).convert('RGB')
        ys = [y for y in range(125, 960) if is_band(im.getpixel((1500, y)))]
        runs, cur = [], []
        for y in ys:
            if cur and y != cur[-1] + 1: runs.append(cur); cur = []
            cur.append(y)
        if cur: runs.append(cur)
        band = max(runs, key=len) if runs and len(max(runs, key=len)) > 40 else []
        if band and not any('hall-of-fame' in t for t in []): break
    if band: time.sleep(0.6); p = dsc.cap('C:/tmp/_j.png')
    link = None
    if band:
        L, W = dsc.ocr(p)
        urls = sorted([l for l in L if 'higgsfield' in l[4] and band[0] - 8 <= l[1] <= band[-1] and l[0] < 420], key=lambda l: l[1])
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
    if not link and user:   # 강조 띠가 없을 때: 카드 주인 이름으로 원래 게시물 찾기
        key = re.sub(r'[^a-z0-9]', '', user.lower())[:4]
        time.sleep(0.8); p = dsc.cap('C:/tmp/_j.png'); L, W = dsc.ocr(p)
        au = [l for l in L if 370 < l[0] < 900 and key and key in re.sub(r'[^a-z0-9]', '', l[4].lower()) and 'higgsfield' not in l[4]]
        for a in au:
            urls = [l for l in L if 'higgsfield' in l[4] and 0 < l[1] - a[1] < 70]
            if not urls: continue
            u = urls[0]; dsc.clk(u[0] + 40, u[1] + u[3] // 2, right=True); time.sleep(0.9)
            L2, _ = dsc.ocr(dsc.cap('C:/tmp/_m.png'))
            items = [l for l in L2 if '링크' in l[4] and ('하기' in l[4] or '복사하' in l[4]) and '메시지' not in l[4] and '매시지' not in l[4]]
            if items:
                it = items[0]; dsc.clk(it[0] + it[2] // 2, it[1] + it[3] // 2); time.sleep(0.4)
                c = dsc.clip()
                if 'higgsfield.ai/s/' in c: link = c.split()[0]
            if not link:
                m = re.search(r'higgsfield\.ai/s/(\S+)', u[4]); link = ('https://higgsfield.ai/s/' + m.group(1)) if m else None
                dsc.clk(1500, 500)
            if link: print('  name-match', user, link, flush=True); break
    if not link:  # FAILSHOT
        import shutil; shutil.copy('C:/tmp/_j.png', 'C:/tmp/fail_%d.png' % int(time.time()))
    for _ in range(3):
        dsc.front(); dsc.clk(24, 15); time.sleep(1.8)
        L, _ = dsc.ocr(dsc.cap())
        if in_hof(L): break
    return link, bool(band)
def go_bottom():
    dsc.front(); time.sleep(0.5); dsc.clk(1300, 300); time.sleep(0.4)
    _prev = None; _same = 0
    for _ in range(80):
        dsc.front(); Lb, _ = dsc.ocr(dsc.cap())
        bt = [l for l in Lb if '최근으로' in l[4]]
        if bt: dsc.clk(1210, 919); time.sleep(2)
        sg = tuple(l[4] for l in Lb if 370 < l[0] < 1300 and 80 < l[1] < 960)
        _same = _same + 1 if (sg == _prev and not bt) else 0; _prev = sg
        if _same >= 3: break
        dsc.scroll(1100, 500, -20000); time.sleep(1.5)
    print('bottom', _same, flush=True)
    time.sleep(2)
