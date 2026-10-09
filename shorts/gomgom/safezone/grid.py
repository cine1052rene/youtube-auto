# 마스터에서 일정 간격 프레임을 뽑아 쇼츠 메뉴 대략 영역(빨강 반투명)을 겹친 격자 이미지
import subprocess, sys, pathlib
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; times = [float(t) for t in sys.argv[3].split(",")]
tiles = []
for t in times:
    p = pathlib.Path(out).with_suffix(f".{int(t*10)}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", str(p)], check=True)
    im = Image.open(p).convert("RGBA"); lay = Image.new("RGBA", im.size, (0,0,0,0)); d = ImageDraw.Draw(lay)
    d.rectangle([0, 1440, 1080, 1920], fill=(255,40,40,80)); d.rectangle([925, 860, 1080, 1440], fill=(255,40,40,80))
    im.alpha_composite(lay); tiles.append(im.convert("RGB").resize((270, 480))); p.unlink()
cols = 6; rows = (len(tiles)+cols-1)//cols
g = Image.new("RGB", (cols*280, rows*490), "white")
for i, t in enumerate(tiles): g.paste(t, ((i%cols)*280, (i//cols)*490))
g.save(out, quality=85); print(out)
