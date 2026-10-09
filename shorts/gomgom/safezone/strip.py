# 한 컷 영상에서 여러 시점 프레임을 가로로 붙인 띠 이미지: python strip.py clip.mp4 out.jpg [n=6]
import subprocess, sys, io
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
ims = []
for i in range(n):
    t = min(d * i / (n - 1), d - 0.05)
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf", "scale=270:480", "-f", "image2pipe", "-vcodec", "mjpeg", "-"], capture_output=True).stdout
    ims.append(Image.open(io.BytesIO(b)).convert("RGB"))
o = Image.new("RGB", (280 * n, 480), "white")
for i, im in enumerate(ims): o.paste(im, (i * 280, 0))
o.save(out, quality=85); print(out)
