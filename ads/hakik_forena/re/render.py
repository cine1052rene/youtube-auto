# 레퍼런스 스타일 합성 엔진 — 더빙 완성본 위에 패널·자막·스티커·카드·전환을 프레임 단위로 입힘
# 사용: python render.py [--preview t1,t2,...]   (preview는 해당 시각 프레임만 jpg로 저장)
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import timeline as T

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC = "../out/학익포레나숏3_더빙_Emily.mp4"
OUT = "../out/학익포레나숏3_레퍼런스스타일.mp4"
FW, FH, FPS, DUR = 1080, 1920, 30000 / 1001, 59.692967
TOP, BOT = 330, 1740                 # 원본 상단 번호 배너 아래 ~ 하단 로고 위
BAND = (760, 1420)                   # 가운데 띠
CAP_Y = 1000                         # 자막 중심
F_BIG = "fonts/BlackHanSans-Regular.ttf"
F_SMALL = "C:/Windows/Fonts/malgunbd.ttf"
YEL, RED, WHITE = (255, 216, 61), (255, 70, 70), (255, 255, 255)


def ease_out_back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def clamp01(x):
    return max(0.0, min(1.0, x))


# ---------------- 자막 ----------------
def parse(line):
    segs, cur, col = [], "", WHITE
    for ch in line:
        if ch in "[{":
            if cur: segs.append((cur, col))
            cur, col = "", (YEL if ch == "[" else RED)
        elif ch in "]}":
            if cur: segs.append((cur, col))
            cur, col = "", WHITE
        else:
            cur += ch
    if cur: segs.append((cur, col))
    return segs


def make_caption(text, size=112):
    lines = [parse(l) for l in text.split("\n")]
    while True:
        font = ImageFont.truetype(F_BIG, size)
        widths = [sum(font.getlength(s) for s, _ in l) for l in lines]
        if max(widths) <= 1000 or size < 60: break
        size -= 6
    st = max(8, size // 9)
    lh = int(size * 1.18)
    w, h = int(max(widths)) + st * 2 + 20, lh * len(lines) + st * 2 + 20
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        x = (w - widths[i]) / 2
        y = st + 10 + i * lh
        for s, col in l:
            d.text((x, y), s, font=font, fill=col, stroke_width=st, stroke_fill=(0, 0, 0))
            x += font.getlength(s)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda a: a * 0.6))
    out = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    out.alpha_composite(sh, (12, 12)); out.alpha_composite(img, (0, 0))
    return out


CAPS = [(a, b, make_caption(t)) for a, b, t in T.CAPS]


def draw_caption(fr, t):
    for a, b, im in CAPS:
        if a <= t < b:
            p = clamp01((t - a) / 0.18)
            s = 0.55 + 0.45 * ease_out_back(p) if p < 1 else 1.0
            c = im if s == 1.0 else im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
            if p < 0.4:
                c = c.copy(); c.putalpha(c.getchannel("A").point(lambda v: int(v * p / 0.4)))
            fr.alpha_composite(c, (FW // 2 - c.width // 2, CAP_Y - c.height // 2))


# ---------------- 패널 ----------------
def region(mode):
    return (0, BAND[0], FW, BAND[1]) if mode == "BAND" else (0, TOP, FW, BOT)


PANELS = []
for a, b, mode, path, cx, cy, z0, z1 in T.PANELS:
    x0, y0, x1, y1 = region(mode)
    w, h = x1 - x0, y1 - y0
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    ar = w / h
    cw, ch = (im.width, im.width / ar) if im.width / im.height < ar else (im.height * ar, im.height)
    k = (w * 1.25) / cw  # 미리 줄여서 프레임당 리사이즈 비용을 낮춤
    if k < 1:
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS); cw, ch = cw * k, ch * k
    PANELS.append(dict(a=a, b=b, mode=mode, im=im, cw=cw, ch=ch, cx=cx, cy=cy, z0=z0, z1=z1,
                       box=(x0, y0, w, h), cut=any(abs(p[1] - a) < 1e-3 for p in T.PANELS)))


def draw_panel(fr, t):
    for P in PANELS:
        if not (P["a"] <= t < P["b"]): continue
        x0, y0, w, h = P["box"]
        u = (t - P["a"]) / (P["b"] - P["a"])
        z = P["z0"] + (P["z1"] - P["z0"]) * u
        im = P["im"]
        cw, ch = min(P["cw"] / z, im.width), min(P["ch"] / z, im.height)
        l = min(max(P["cx"] * im.width - cw / 2, 0), im.width - cw)
        tp = min(max(P["cy"] * im.height - ch / 2, 0), im.height - ch)
        pic = im.resize((w, h), Image.BILINEAR, box=(l, tp, l + cw, tp + ch))
        p = 1.0 if P["cut"] else clamp01((t - P["a"]) / 0.22)
        e = 1 - (1 - p) ** 3
        if P["mode"] == "BAND":
            vh = max(2, int(h * e)); off = (h - vh) // 2
            fr.paste(pic.crop((0, off, w, off + vh)), (x0, y0 + off))
            if e > 0.2:
                d = ImageDraw.Draw(fr)
                d.rectangle((0, y0 + off - 6, FW, y0 + off - 1), fill=WHITE)
                d.rectangle((0, y0 + off + vh, FW, y0 + off + vh + 5), fill=WHITE)
        else:
            vw = max(2, int(w * e))
            fr.paste(pic.crop((0, 0, vw, h)), (x0, y0))
        return


# ---------------- 84타입 카드 ----------------
def build_card():
    w, h = FW, BOT - TOP
    g = np.linspace(0, 1, h)[:, None]
    top, bot = np.array([10, 28, 72]), np.array([24, 62, 140])
    arr = (top * (1 - g) + bot * g)[:, None, :].repeat(w, 1).astype(np.uint8)
    bg = Image.fromarray(arr.reshape(h, w, 3)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    for x in range(0, w, 60): d.line((x, 0, x, h), fill=(255, 255, 255, 14))
    for y in range(0, h, 60): d.line((0, y, w, y), fill=(255, 255, 255, 14))
    f1 = ImageFont.truetype(F_BIG, 70); f2 = ImageFont.truetype(F_BIG, 210)
    d.text((w / 2, 170), "지금 보시는 타입", font=f1, fill=WHITE, anchor="mm")
    d.text((w / 2, 360), "84 TYPE", font=f2, fill=YEL, anchor="mm", stroke_width=6, stroke_fill=(8, 20, 50))
    d.rounded_rectangle((140, 490, w - 140, 500), 5, fill=(255, 216, 61, 180))
    return bg


CARD_BG = build_card()
F_ITEM = ImageFont.truetype(F_BIG, 76)


def draw_card(fr, t):
    a, b = T.CARD
    if not (a <= t < b): return
    card = CARD_BG.copy(); d = ImageDraw.Draw(card)
    for i, (ti, txt) in enumerate(T.CARD_ITEMS):
        if t < ti: continue
        p = 1 - (1 - clamp01((t - ti) / 0.2)) ** 3
        y = 610 + i * 150; x = 170 - int(120 * (1 - p)); al = int(255 * p)
        d.ellipse((x, y - 38, x + 76, y + 38), fill=(255, 216, 61, al))
        d.line((x + 18, y, x + 33, y + 17, x + 60, y - 18), fill=(10, 28, 72, al), width=10)
        d.text((x + 110, y), txt, font=F_ITEM, fill=(255, 255, 255, al), anchor="lm")
    e = 1 - (1 - clamp01((t - a) / 0.22)) ** 3
    vw = max(2, int(FW * e))
    fr.alpha_composite(card.crop((0, 0, vw, card.height)), (0, TOP))


# ---------------- 스티커 ----------------
def key_green(path, size, ban):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w, _ = a.shape
    corners = np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3), a[-40:, :40].reshape(-1, 3), a[-40:, -40:].reshape(-1, 3)])
    bgc = np.median(corners, 0)
    dist = np.sqrt(((a - bgc) ** 2).sum(-1))
    alpha = np.clip((dist - 45) * 255 / 55, 0, 255).astype(np.uint8)   # 배경색에서 45 이내 → 투명
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    near = dist < 140                                                  # 가장자리만 초록 번짐 제거
    g = np.where(near & (g > np.maximum(r, b)), np.maximum(r, b), g)
    rgb = np.stack([r, g, b], -1).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(np.dstack([rgb, alpha]), "RGBA")
    m = im.getchannel("A").point(lambda v: 255 if v > 128 else 0).filter(ImageFilter.MinFilter(9))
    im = im.crop(m.getbbox())
    k = size / max(im.size)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    # 흰 테두리 스티커 효과
    m = im.getchannel("A").filter(ImageFilter.MaxFilter(15))
    pad = Image.new("RGBA", (im.width + 20, im.height + 20), (0, 0, 0, 0))
    border = Image.new("RGBA", im.size, (255, 255, 255, 255)); border.putalpha(m)
    pad.alpha_composite(border, (10, 10)); pad.alpha_composite(im, (10, 10))
    if ban:
        d = ImageDraw.Draw(pad); W_, H_ = pad.size; r0 = min(W_, H_) * 0.46
        c = (W_ / 2, H_ / 2)
        d.ellipse((c[0] - r0, c[1] - r0, c[0] + r0, c[1] + r0), outline=(230, 30, 30, 255), width=26)
        o = r0 * 0.70
        d.line((c[0] - o, c[1] - o, c[0] + o, c[1] + o), fill=(230, 30, 30, 255), width=26)
    return pad


STK = []
for a, b, name, cx, cy, size, ban in T.STICKERS:
    p = f"stk/{name}.png"
    if os.path.exists(p): STK.append((a, b, key_green(p, size, ban), cx, cy))
    else: print("스티커 없음:", p)


def draw_stickers(fr, t):
    for a, b, im, cx, cy in STK:
        if not (a <= t < b): continue
        p = clamp01((t - a) / 0.3)
        s = ease_out_back(p) if p < 1 else 1.0
        ang = 5 * math.sin((t - a) * 5)
        bob = 12 * math.sin((t - a) * 6)
        c = im.rotate(ang, Image.BILINEAR, expand=True)
        if s != 1.0:
            c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.BILINEAR)
        fr.alpha_composite(c, (int(cx - c.width / 2), int(cy + bob - c.height / 2)))


# ---------------- 전환·화살표·면책 ----------------
_glow = Image.new("L", (FW, 240), 0)
ImageDraw.Draw(_glow).rectangle((0, 114, FW, 126), fill=255)
GLOW = Image.merge("RGBA", [_glow.filter(ImageFilter.GaussianBlur(3)).point(lambda v: min(255, v * 2))] * 3 +
                   [ImageOps.autocontrast(_glow.filter(ImageFilter.GaussianBlur(28)))])
GLOW_TINT = Image.new("RGBA", GLOW.size, (120, 180, 255, 0))


def draw_streak(fr, t):
    a, b = T.STREAK
    if not (a <= t < b): return
    u = (t - a) / (b - a)
    black = int(255 * min(1, u / 0.15, (1 - u) / 0.2 if u > 0.8 else 1))
    fr.alpha_composite(Image.new("RGBA", (FW, BOT - TOP + 180), (0, 0, 0, black)), (0, TOP))
    w = max(2, int(FW * clamp01(u / 0.55)))
    g = GLOW.resize((w, GLOW.height))
    g.putalpha(g.getchannel("A").point(lambda v: int(v * (1 if u < 0.8 else (1 - u) / 0.2))))
    fr.alpha_composite(g, ((FW - w) // 2, 1035 - GLOW.height // 2))


F_ARROW = ImageFont.truetype(F_BIG, 60)


def draw_arrow(fr, t):
    a, b = T.ARROW
    if not (a <= t < b): return
    y = 380 + int(22 * abs(math.sin((t - a) * 6)))
    d = ImageDraw.Draw(fr)
    for cx in (220, 860):
        pts = [(cx, y), (cx - 70, y + 80), (cx - 30, y + 80), (cx - 30, y + 150), (cx + 30, y + 150), (cx + 30, y + 80), (cx + 70, y + 80)]
        d.polygon(pts, fill=YEL, outline=(0, 0, 0), width=6)


_dfont = ImageFont.truetype(F_SMALL, 22)
DISC = Image.new("RGBA", (FW, 40), (0, 0, 0, 0))
ImageDraw.Draw(DISC).text((FW / 2, 20), T.DISCLAIMER, font=_dfont, fill=(255, 255, 255, 210),
                          anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 200))


def compose(fr, t):
    if t < 1.0: return fr
    fr = fr.convert("RGBA")
    draw_panel(fr, t)
    draw_card(fr, t)
    draw_streak(fr, t)
    draw_stickers(fr, t)
    draw_caption(fr, t)
    draw_arrow(fr, t)
    fr.alpha_composite(DISC, (0, BOT - 52))
    return fr.convert("RGB")


def frames():
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = FW * FH * 3; i = 0
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n: break
        yield i, Image.frombuffer("RGB", (FW, FH), buf, "raw", "RGB", 0, 1)
        i += 1


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        ts = [float(x) for x in sys.argv[2].split(",")]
        os.makedirs("pv", exist_ok=True)
        for t in ts:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", SRC, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            compose(Image.frombuffer("RGB", (FW, FH), raw, "raw", "RGB", 0, 1).copy(), t).save(f"pv/{t:05.2f}.jpg", quality=85)
        print("preview done"); return
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}",
                            "-r", "30000/1001", "-i", "-", "-i", SRC, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest",
                            "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i, fr in frames():
        enc.stdin.write(compose(fr.copy(), i / FPS).tobytes())
        if i % 150 == 0: print(f"frame {i} ({i / FPS:.1f}s)", flush=True)
    enc.stdin.close(); enc.wait()
    print("RENDER DONE", OUT)


if __name__ == "__main__":
    main()
