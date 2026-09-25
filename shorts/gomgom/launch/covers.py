"""1~3화 커버 합성: 9:16(쇼츠·릴스·클립) + 3:4(인스타 격자 확인용). 크레딧 0."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
BASE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(BASE, '..', 'fonts', 'GowunDodum-Regular.ttf')
EPS = [
    ('01', '../ep01/v3/img/02.png', ['쉬어도 쉬어도', '피곤한 이유']),
    ('02', '../ep02/prod/img/08.png', ['칭찬은 잊고', '지적은 남는 이유']),
    ('03', '../ep03/prod/img/10.png', ['에피쿠로스가 말한', '작은 행복']),
]
W, H = 1080, 1920
BROWN = (92, 60, 40)

def fit(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def cover(ep, src, lines):
    im = fit(Image.open(os.path.join(BASE, src)).convert('RGB'), W, H)
    # 인스타 격자(3:4)는 세로 중앙 1440px만 보임 → 글자는 y 240~ 안쪽에 둔다
    f = ImageFont.truetype(FONT, 104)
    fs = ImageFont.truetype(FONT, 44)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    lh = 128; top = 300
    widths = [d.textbbox((0, 0), t, font=f)[2] for t in lines]
    bw = max(widths) + 110; bh = lh * len(lines) + 150
    bx = (W - bw) // 2
    d.rounded_rectangle((bx, top, bx + bw, top + bh), radius=56, fill=(255, 248, 236, 225))
    tag = f'곰곰한 마음 · {int(ep)}화'
    tw = d.textbbox((0, 0), tag, font=fs)[2]
    d.text(((W - tw) // 2, top + 34), tag, font=fs, fill=(196, 120, 96))
    for i, t in enumerate(lines):
        d.text(((W - widths[i]) // 2, top + 100 + i * lh), t, font=f, fill=BROWN,
               stroke_width=2, stroke_fill=BROWN)
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(18)).point(lambda v: v * 0.35)
    im = im.convert('RGBA')
    im.paste((60, 40, 30, 255), (0, 0), Image.merge('L', [sh]))
    im = Image.alpha_composite(im, lay).convert('RGB')
    im.save(os.path.join(BASE, 'out', f'cover_ep{ep}_9x16.jpg'), quality=94)
    im.crop((0, 240, W, 240 + 1440)).save(os.path.join(BASE, 'out', f'cover_ep{ep}_grid_3x4_check.jpg'), quality=90)

for e in EPS:
    cover(*e)
print('ok')
