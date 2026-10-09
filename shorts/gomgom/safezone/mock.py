# 쇼츠·릴스 화면 메뉴(대략 영역) 위에 현재/수정안 자막 위치를 겹쳐 보는 점검 이미지
import json, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
G = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(G / "speed_test"))
FONT = G / "fonts" / "GowunDodum-Regular.ttf"
W, H = 1080, 1920
font = ImageFont.truetype(str(FONT), 66); small = ImageFont.truetype(str(FONT), 34)

def wrap(text, maxw):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def sub(im, text, yc, maxw):
    d = ImageDraw.Draw(im, "RGBA"); lines = wrap(text, maxw); lh = 94; total = lh * len(lines); y0 = yc - total // 2
    mw = max(font.getlength(l) for l in lines)
    d.rounded_rectangle([W/2-mw/2-46, y0-24, W/2+mw/2+46, y0+total+16], radius=44, fill=(58,40,28,110))
    for i, l in enumerate(lines):
        d.text((W/2-font.getlength(l)/2, y0+i*lh), l, font=font, fill=(255,250,240,255), stroke_width=5, stroke_fill=(72,50,34,255))

def ui(im, kind):
    lay = Image.new("RGBA", im.size, (0,0,0,0)); d = ImageDraw.Draw(lay)
    if kind == "yt":   # 유튜브 쇼츠: 아래 제목·채널·음악 줄, 오른쪽 좋아요·댓글·공유 버튼
        d.rectangle([0, 1440, W, H], fill=(255, 40, 40, 95)); d.rectangle([925, 860, W, 1440], fill=(255, 40, 40, 95))
        d.text((30, 1460), "유튜브: 채널명·제목·음악", font=small, fill=(255,255,255,255), stroke_width=3, stroke_fill=(0,0,0,255))
    else:              # 인스타 릴스: 아래 계정·캡션, 오른쪽 버튼
        d.rectangle([0, 1500, W, H], fill=(60, 90, 255, 95)); d.rectangle([945, 1000, W, 1500], fill=(60, 90, 255, 95))
        d.text((30, 1520), "인스타: 계정·캡션", font=small, fill=(255,255,255,255), stroke_width=3, stroke_fill=(0,0,0,255))
    im.alpha_composite(lay)

ln = json.load(open(G / "ep03/lines.json", encoding="utf-8"))["shots"]
txt = ln[0]["narrator"]
base = Image.open(G / "ep03/prod/img/01.png").convert("RGBA").resize((W, H))
tiles = []
for kind in ("yt", "ig"):
    for title, yc, mw in (("지금 (높이 1540)", 1540, 880), ("수정안 (높이 1200, 폭 좁힘)", 1200, 740)):
        im = base.copy(); sub(im, txt, yc, mw); ui(im, kind)
        ImageDraw.Draw(im).text((30, 60), title, font=ImageFont.truetype(str(FONT), 54), fill=(255,255,255,255), stroke_width=4, stroke_fill=(0,0,0,255))
        tiles.append(im.resize((540, 960)))
out = Image.new("RGB", (540*4+60, 960), (255,255,255))
for i, t in enumerate(tiles): out.paste(t, (i*(540+20), 0))
p = G / "safezone" / "safezone_ep03.jpg"; out.save(p, quality=88); print(p)
