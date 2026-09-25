"""프로필·배너·헤더 합성 (gen/ 원본 → out/). 크레딧 0."""
from PIL import Image, ImageDraw
import os
B = os.path.dirname(os.path.abspath(__file__))
g = lambda n: Image.open(os.path.join(B, 'gen', n)).convert('RGB')
o = lambda n: os.path.join(B, 'out', n)

p = g('p1.png')
p.resize((800, 800), Image.LANCZOS).save(o('profile_800.png'))
p.resize((400, 400), Image.LANCZOS).save(o('profile_400.png'))
# 원형 미리보기
c = p.resize((400, 400), Image.LANCZOS); m = Image.new('L', (400, 400), 0); ImageDraw.Draw(m).ellipse((0, 0, 399, 399), fill=255)
bg = Image.new('RGB', (400, 400), 'white'); bg.paste(c, (0, 0), m); bg.save(o('check_profile_circle.png'))

def place(img, W, H, face_y, cx=0.5, fy=0.5):
    """얼굴 높이(face_y, 원본 비율)가 결과의 fy 지점에 오도록 확대·크롭"""
    s = max(W / img.width, H / img.height)
    s = max(s, (fy * H) / (face_y * img.height), ((1 - fy) * H) / ((1 - face_y) * img.height))
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    y = round(face_y * im.height - fy * H); x = round(cx * im.width - W / 2)
    y = min(max(y, 0), im.height - H); x = min(max(x, 0), im.width - W)
    return im.crop((x, y, x + W, y + H))

def yt(src, name, face_y, cx):
    im = place(g(src), 2560, 1440, face_y, cx, 0.5)
    im.save(o(name), quality=92)
    ck = im.copy(); d = ImageDraw.Draw(ck)
    d.rectangle((507, 508, 2053, 931), outline=(255, 0, 0), width=8)  # 모든 기기 노출 영역
    d.rectangle((0, 508, 2559, 931), outline=(255, 255, 0), width=4)   # 데스크톱 노출 영역
    ck.resize((1280, 720)).save(o('check_' + name), quality=85)

yt('b1.png', 'yt_banner_2560x1440.jpg', 0.5, 0.49)
yt('b3.png', 'yt_banner_alt_night_2560x1440.jpg', 0.47, 0.47)
place(g('b1.png'), 1500, 500, 0.45, 0.49, 0.5).save(o('x_header_1500x500.jpg'), quality=92)
place(g('b1.png'), 966, 300, 0.45, 0.49, 0.5).save(o('blog_title_966x300.jpg'), quality=92)
print('ok')
