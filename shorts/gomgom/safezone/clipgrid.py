# 한 화의 컷 영상마다 프레임 5장씩 가로로, 컷은 세로로 쌓은 점검표: python clipgrid.py 08 out.jpg [시작번호 끝번호]
import subprocess, sys, io, pathlib
from PIL import Image, ImageDraw, ImageFont
ep, out = sys.argv[1], sys.argv[2]; a, b = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1, 99)
G = pathlib.Path(__file__).resolve().parent.parent
f = ImageFont.truetype(str(G / "fonts/GowunDodum-Regular.ttf"), 34)
clips = [p for p in sorted((G / f"ep{ep}/prod/clips").glob("[0-9][0-9].mp4")) if a <= int(p.stem) <= b]
W, Hh, N = 180, 320, 5
o = Image.new("RGB", (60 + N * (W + 6), len(clips) * (Hh + 8)), "white"); d = ImageDraw.Draw(o)
for r, p in enumerate(clips):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
    d.text((6, r * (Hh + 8) + 140), p.stem, font=f, fill=(200, 0, 0))
    for i in range(N):
        t = min(dur * i / (N - 1), dur - 0.05)
        bb = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(p), "-frames:v", "1", "-vf", f"scale={W}:{Hh}", "-f", "image2pipe", "-vcodec", "mjpeg", "-"], capture_output=True).stdout
        o.paste(Image.open(io.BytesIO(bb)).convert("RGB"), (60 + i * (W + 6), r * (Hh + 8)))
o.save(out, quality=80); print(out)
