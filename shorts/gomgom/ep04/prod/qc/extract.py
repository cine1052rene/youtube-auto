# -*- coding: utf-8 -*-
import subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

H = pathlib.Path(__file__).parent
CLIPS = H.parent / "clips"
FR = H / "frames"
SH = H / "sheets"

def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],
                        capture_output=True, text=True)
    return float(r.stdout.strip())

def extract(clip, n=5):
    d = dur(clip)
    times = [round(d * i / (n - 1), 2) if n > 1 else 0 for i in range(n)]
    times = [min(x, d - 0.3) for x in times]
    times = [max(x, 0) for x in times]
    imgs = []
    for i, t in enumerate(times):
        out = FR / f"{clip.stem}_{i}.jpg"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{t:.2f}","-i",str(clip),
                         "-frames:v","1","-q:v","3","-pix_fmt","yuvj420p", str(out)], check=True)
        imgs.append((t, out))
    return imgs

order = [f"{i:02d}" for i in range(1, 14)]
font = None
try:
    font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
except Exception:
    font = ImageFont.load_default()

# build sheet: 2 clips per row-group (each clip = 1 row of 5 thumbs + label)
COLS = 5
TH_W, TH_H = 300, 533
rows = []
for cid in order:
    clip = CLIPS / f"{cid}.mp4"
    n = 6 if cid == "13" else 5
    imgs = extract(clip, n=n)
    rows.append((cid, imgs))

# paginate: 4 clip-rows per sheet
PER_SHEET = 4
for pg in range(0, len(rows), PER_SHEET):
    chunk = rows[pg:pg+PER_SHEET]
    maxcols = max(len(r[1]) for r in chunk)
    sheet_w = maxcols * TH_W
    sheet_h = len(chunk) * (TH_H + 40)
    sheet = Image.new("RGB", (sheet_w, sheet_h), (20,20,20))
    d = ImageDraw.Draw(sheet)
    for ri, (cid, imgs) in enumerate(chunk):
        y0 = ri * (TH_H + 40)
        d.text((10, y0 + 5), f"cut {cid}", fill=(255,255,0), font=font)
        for ci, (t, imgpath) in enumerate(imgs):
            im = Image.open(imgpath).resize((TH_W, TH_H))
            sheet.paste(im, (ci*TH_W, y0+40))
            d.text((ci*TH_W+5, y0+40+5), f"{t:.1f}s", fill=(255,255,255), font=font)
    outp = SH / f"sheet_{pg//PER_SHEET+1}.jpg"
    sheet.save(outp, quality=85)
    print("saved", outp)
