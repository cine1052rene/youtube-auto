# -*- coding: utf-8 -*-
"""make_sample.py --premiere 결과(timeline.json + 소재)를 프리미어용 XML(Final Cut Pro 7 XML)로 변환
사용: python premiere_xml.py <premiere/epNN_tag 폴더>
트랙: V1 컷 영상 · V2 자막 PNG · V3 제목 카드 / A1 내레이션 · A2 배경음악 · A3 콩이 소리
"""
import json, math, pathlib, subprocess, sys
from urllib.parse import quote
from xml.sax.saxutils import escape

D = pathlib.Path(sys.argv[1]).resolve()
T = json.load(open(D / "timeline.json", encoding="utf-8"))
FPS, W, H = T["fps"], T["width"], T["height"]
RATE = f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"
_n = [0]


def url(p):
    return "file://localhost/" + quote(p.resolve().as_posix(), safe="/:")


def frames_of(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return math.ceil(float(r.stdout.strip()) * FPS)


def level(g):  # 프리미어 '오디오 레벨'(선형 배율)
    return (f"<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory>"
            f"<effecttype>audiolevel</effecttype><mediatype>audio</mediatype><parameter><parameterid>level</parameterid>"
            f"<name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax><value>{g:.4f}</value></parameter></effect></filter>")


def clip(path, start, n, kind, name=None, gain=None, src_frames=None, still=False):
    _n[0] += 1; i = _n[0]
    fd = src_frames or n
    if kind == "video":
        media = (f"<media><video><samplecharacteristics>{RATE}<width>{W}</width><height>{H}</height>"
                 f"<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></video></media>")
    else:
        media = "<media><audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio></media>"
    src = ("<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>" if kind == "audio" else "")
    return (f'<clipitem id="c{i}"><name>{escape(name or path.name)}</name><enabled>TRUE</enabled><duration>{fd}</duration>{RATE}'
            f"<start>{start}</start><end>{start + n}</end><in>0</in><out>{n}</out>"
            f'<file id="f{i}"><name>{escape(path.name)}</name><pathurl>{url(path)}</pathurl>{RATE}<duration>{fd}</duration>{media}</file>'
            f"{src}{level(gain) if gain is not None else ''}</clipitem>")


cuts = T["cuts"]
v1 = "".join(clip(D / "video" / f"{c['id']}.mp4", c["start"], c["frames"], "video", f"{c['id']} 영상") for c in cuts)
v2 = "".join(clip(D / "sub" / f"{c['id']}.png", c["start"], c["frames"], "video", f"{c['id']} 자막 · {c['text']}", src_frames=c["frames"]) for c in cuts)
v3 = ""
if T.get("hook"):
    h = T["hook"]; v3 = clip(D / h["file"], 0, h["frames"], "video", "제목 카드", src_frames=h["frames"])
a1 = "".join(clip(D / "narr" / f"{c['id']}.wav", c["start"], c["frames"], "audio", f"{c['id']} 내레이션", 1.0) for c in cuts)
a2 = clip(D / T["bgm"], 0, T["total"], "audio", "배경음악(음량 변화 포함)", 1.0) if T.get("bgm") else ""
a3 = ""
for s in T["sfx"]:
    p = D / "sfx" / s["file"]; n = frames_of(p)
    a3 += clip(p, s["start"], n, "audio", f"{s['cut']} {p.stem}", s["gain"], src_frames=n)

vt = "".join(f"<track>{t}</track>" for t in (v1, v2, v3) if t)
at = "".join(f"<track>{t}</track>" for t in (a1, a2, a3) if t)
xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4"><sequence id="seq1"><name>{escape(T['name'])}</name><duration>{T['total']}</duration>{RATE}
<timecode>{RATE}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>
<media><video><format><samplecharacteristics>{RATE}<width>{W}</width><height>{H}</height><anamorphic>FALSE</anamorphic>
<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>{vt}</video>
<audio><numOutputChannels>2</numOutputChannels><format><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics></format>{at}</audio>
</media></sequence></xmeml>
"""
out = D / f"{T['name']}.xml"
out.write_text(xml, encoding="utf-8")
print(out, f"컷 {len(cuts)} · 콩이 소리 {len(T['sfx'])} · {T['total'] / FPS:.1f}초")
