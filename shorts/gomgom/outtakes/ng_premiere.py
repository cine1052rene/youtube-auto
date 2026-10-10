# -*- coding: utf-8 -*-
"""시즌1 마무리 NG 모음 — 프리미어 미리보기용 세팅(마스터 렌더 안 함)
출력: speed_test/premiere/ng_s1/  (video·sub·narr·bgm + ng_s1.xml, 쇼츠 1080x1920 30fps)
트랙: V1 NG 컷 · V2 자막 PNG · V3 제목 카드 / A1 소리 NG(원래 내레이션) · A2 배경음악
사용: python outtakes/ng_premiere.py   → 프리미어에서 파일 > 가져오기로 ng_s1.xml
"""
import math, pathlib, shutil, subprocess
from urllib.parse import quote
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

G = pathlib.Path(__file__).resolve().parent.parent
D = G / "speed_test" / "premiere" / "ng_s1"
FPS, W, H = 30, 1080, 1920
SUBY, SUBW = 1320, 740
font = ImageFont.truetype(str(G / "fonts" / "GowunDodum-Regular.ttf"), 66)
hfont = ImageFont.truetype(str(G / "fonts" / "GowunDodum-Regular.ttf"), 104)

# (이름, 원본, 시작초, 끝초, 자막 리스트[(자막, 컷 안 시작 비율)], 소리 NG 파일)
NG = [
    ("00 훅 관객석에 사람", "ep08/prod/clips/08_old1009.mp4", 1.0, 4.0, [("곰곰이 공연에… 누가 오셨죠?", 0)], None),
    ("01 뒤돌았더니 다른 곰", "outtakes/ng/ep02_13_만화곰으로변신.mp4", 1.2, 3.6, [("뒤돌았더니… 다른 곰?", 0)], None),
    ("02 곰곰이 퇴근", "outtakes/ng/ep01_13_하늘로사라짐.mp4", 2.0, 5.0, [("곰곰이 퇴근합니다", 0)], None),
    ("03 콩이 날개 거대", "outtakes/ng/ep04_13_곰곰이가날아감.mp4", 1.8, 4.0, [("콩이 날개… 이렇게 컸나?", 0)], None),
    ("04 곰곰이가 둘", "ep07/prod/clips/08_old1009.mp4", 0.6, 2.8, [("분명 혼자였는데", 0)], None),
    ("05 벽돌이 머리에", "ep07/prod/clips/06_try1.mp4", 0.5, 3.3, [("지붕은 거기 아니야", 0)], None),
    ("06 토끼 둥둥", "ep08/prod/clips/06_try1010a.mp4", 1.4, 3.9, [("긴장하면 뜹니다", 0)], None),
    ("07 형광 하트", "outtakes/ng/ep04_01_형광플라스틱하트.mp4", 2.0, 4.0, [("펠트예요… 펠트", 0)], None),
    ("08a 부엉이 2배", "outtakes/alt/ep04_04_부엉이가2배.mp4", 0.5, 2.3, [("할아버지 키가…", 0)], None),
    ("08b 부엉이 작음", "outtakes/alt/ep04_05_부엉이가작음.mp4", 0.5, 2.3, [("왜 이래요?", 0)], None),
    ("09 뒤통수에 얼굴", "ep07/prod/clips/12_old1009.mp4", 1.2, 3.4, [("…뒤에도 얼굴이?", 0)], None),
    ("10 소리 운고미", "ep08/prod/clips/02.mp4", 0.0, None, [("“운고미도…”", 0)], "ep08/audio/luna/02_old1009.mp3"),
    ("11 소리 몽고미", "ep08/prod/clips/11.mp4", 0.0, None, [("“몽고미는…” 제 이름은 곰곰이예요", 0)], "ep08/audio/luna/11_old1009.mp3"),
    ("12 마무리", "ep08/prod/clips/10.mp4", 0.0, 4.0, [("실수해도 괜찮아요. 다시 하면 되니까", 0), ("어떤 NG가 제일 웃겼나요?", 0.55)], None),
]
HOOK_TXT, HOOK_SEC = ["곰곰이 촬영장", "NG 모음"], 3.0
BGM, BGM_GAIN = "ep05/prod/bgm.mp3", 0.35


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def wrap(text):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if font.getlength(t) <= SUBW: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def render_sub(text, path):  # make_sample.py 자막과 같은 모양·위치
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lines = wrap(text); lh = 94; total = lh * len(lines); y0 = SUBY - total // 2
    mw = max(font.getlength(l) for l in lines)
    d.rounded_rectangle([W / 2 - mw / 2 - 46, y0 - 24, W / 2 + mw / 2 + 46, y0 + total + 16], radius=44, fill=(58, 40, 28, 110))
    for i, l in enumerate(lines):
        d.text((W / 2 - font.getlength(l) / 2, y0 + i * lh), l, font=font, fill=(255, 250, 240, 255), stroke_width=5, stroke_fill=(72, 50, 34, 255))
    img.save(path)


def render_hook(lines, path):  # 위쪽 제목 카드
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lh = int(104 * 1.34); total = lh * len(lines); y0 = 330 - total // 2
    mw = max(hfont.getlength(l) for l in lines)
    d.rounded_rectangle([W / 2 - mw / 2 - 64, y0 - 44, W / 2 + mw / 2 + 64, y0 + total + 24], radius=60, fill=(255, 248, 236, 228))
    for i, l in enumerate(lines):
        d.text((W / 2 - hfont.getlength(l) / 2, y0 + i * lh), l, font=hfont, fill=(74, 52, 36, 255))
    img.save(path)


def url(p):
    return "file://localhost/" + quote(p.resolve().as_posix(), safe="/:")


RATE = f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"
_n = [0]


def clip(path, start, n, kind, name, gain=None, src=None):
    _n[0] += 1; i = _n[0]; fd = src or n
    media = (f"<media><video><samplecharacteristics>{RATE}<width>{W}</width><height>{H}</height><pixelaspectratio>square</pixelaspectratio></samplecharacteristics></video></media>"
             if kind == "video" else "<media><audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media>")
    st = "<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>" if kind == "audio" else ""
    lv = (f"<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory><effecttype>audiolevel</effecttype>"
          f"<mediatype>audio</mediatype><parameter><parameterid>level</parameterid><name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax><value>{gain:.4f}</value></parameter></effect></filter>") if gain is not None else ""
    return (f'<clipitem id="c{i}"><name>{escape(name)}</name><enabled>TRUE</enabled><duration>{fd}</duration>{RATE}<start>{start}</start><end>{start + n}</end><in>0</in><out>{n}</out>'
            f'<file id="f{i}"><name>{escape(path.name)}</name><pathurl>{url(path)}</pathurl>{RATE}<duration>{fd}</duration>{media}</file>{st}{lv}</clipitem>')


def main():
    shutil.rmtree(D, ignore_errors=True)
    for s in ("video", "sub", "narr"): (D / s).mkdir(parents=True)
    t, v1, v2, a1 = 0, "", "", ""
    for k, (name, src, a, b, subs, snd) in enumerate(NG):
        srcp = G / src
        if snd:  # 소리 NG: 내레이션 길이 + 여백 0.4초만큼 영상
            sp = G / snd; ad = dur(sp); b = min(dur(srcp), ad + 0.4)
            wav = D / "narr" / f"{k:02d}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sp), "-ar", "48000", "-ac", "2", str(wav)], check=True)
        n = round((b - a) * FPS)
        vf = D / "video" / f"{k:02d}.mp4"
        speed = (b - a) / (n / FPS)
        vfilt = f"scale={W}:{H}:flags=lanczos,fps={FPS}"
        if snd and dur(srcp) < (dur(G / snd) + 0.4):  # 영상이 짧으면 마지막 프레임을 늘려 소리 끝까지
            vfilt += f",tpad=stop_mode=clone:stop_duration={dur(G / snd) + 0.4 - dur(srcp):.2f}"
            n = round((dur(G / snd) + 0.4) * FPS)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(srcp), "-t", f"{n / FPS:.3f}", "-vf", vfilt,
                        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(vf)], check=True)
        v1 += clip(vf, t, n, "video", name)
        for j, (txt, r) in enumerate(subs):
            sp = D / "sub" / f"{k:02d}_{j}.png"; render_sub(txt, sp)
            s0 = t + round(n * r); s1 = t + (round(n * subs[j + 1][1]) if j + 1 < len(subs) else n)
            v2 += clip(sp, s0, s1 - s0, "video", f"자막 · {txt}", src=s1 - s0)
        if snd:
            a1 += clip(D / "narr" / f"{k:02d}.wav", t, n, "audio", f"소리 NG · {name}", 1.0)
        t += n
    hp = D / "sub" / "hook.png"; render_hook(HOOK_TXT, hp)
    hn = round(HOOK_SEC * FPS)
    v3 = clip(hp, 0, hn, "video", "제목 카드", src=hn)
    bg = D / "bgm.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(G / BGM), "-t", f"{t / FPS:.3f}", "-af", f"afade=t=out:st={t / FPS - 1.5:.2f}:d=1.5",
                    "-ar", "48000", "-ac", "2", str(bg)], check=True)
    a2 = clip(bg, 0, t, "audio", "배경음악(볼륨 0.35)", BGM_GAIN)
    vt = "".join(f"<track>{x}</track>" for x in (v1, v2, v3))
    at = "".join(f"<track>{x}</track>" for x in (a1, a2))
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4"><sequence id="seq1"><name>곰곰한마음 NG모음 시즌1 (쇼츠 1080x1920)</name><duration>{t}</duration>{RATE}
<timecode>{RATE}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>
<media><video><format><samplecharacteristics>{RATE}<width>{W}</width><height>{H}</height><anamorphic>FALSE</anamorphic>
<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>{vt}</video>
<audio><numOutputChannels>2</numOutputChannels><format><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics></format>{at}</audio>
</media></sequence></xmeml>
"""
    out = D / "ng_s1.xml"; out.write_text(xml, encoding="utf-8")
    print(out, f"{len(NG)}컷 · {t / FPS:.1f}초")


if __name__ == "__main__":
    main()
