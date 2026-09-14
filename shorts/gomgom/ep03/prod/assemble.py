# -*- coding: utf-8 -*-
"""
곰곰한 마음 3화 조립 (13컷 전부 영상 + Luna 내레이션 + 고운돋움 자막 + 선택적 배경음악)
사용: python assemble.py
입력: v3/clips/NN.mp4, ep01/audio/luna/NN.mp3, ep01/lines.json(narrator), v3/bgm.mp3(있으면)
출력: v3/out/ep03.mp4 (1080x1920), v3/out/ep03_preview.mp4 (540x960), v3/out/timeline.json
컷 길이 = 0.15 + 대사 + 0.30초 (최소 2초)
- 클립이 길면: 카메라 움직임이 끝나는 뒷부분을 살리고, 최대 1.3배까지 빠르게
- 클립이 짧으면: 최대 1.4배까지 느리게, 그래도 모자라면 마지막 프레임 유지
"""
import json, subprocess, sys, pathlib, shutil
from PIL import Image, ImageDraw, ImageFont

V3 = pathlib.Path(__file__).parent
EP = V3.parent
ROOT = EP.parent
AUD = EP / "audio" / "luna"
OUT = V3 / "out"; OUT.mkdir(exist_ok=True)
TMP = OUT / "tmp"
shutil.rmtree(TMP, ignore_errors=True); TMP.mkdir()
FONT = ROOT / "fonts" / "GowunDodum-Regular.ttf"
BGM = V3 / "bgm.mp3"

FPS, W, H = 30, 1080, 1920
LEAD, TAIL, MIN_D = 0.15, 0.30, 2.0
MAX_FAST, MAX_SLOW = 1.3, 1.4
shots = json.load(open(EP / "lines.json", encoding="utf-8"))["shots"]
font = ImageFont.truetype(str(FONT), 66)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG ERROR:", " ".join(map(str, cmd))[:500]); print(r.stderr[-1500:]); sys.exit(1)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def wrap(text, maxw=880):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_sub(text, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = wrap(text)
    lh = 94
    total = lh * len(lines)
    y0 = 1540 - total // 2
    maxw = max(font.getlength(l) for l in lines)
    pad_x, pad_y = 46, 24
    d.rounded_rectangle([W / 2 - maxw / 2 - pad_x, y0 - pad_y, W / 2 + maxw / 2 + pad_x, y0 + total + pad_y - 8],
                        radius=44, fill=(58, 40, 28, 110))
    for i, l in enumerate(lines):
        x = W / 2 - font.getlength(l) / 2
        d.text((x, y0 + i * lh), l, font=font, fill=(255, 250, 240, 255), stroke_width=5, stroke_fill=(72, 50, 34, 255))
    img.save(path)


vlist, alist, timeline = [], [], []
t = 0.0
for s in shots:
    sid = s["id"]
    a = AUD / f"{sid}.mp3"
    clip = V3 / "clips" / f"{sid}.mp4"
    if not clip.exists():
        sys.exit(f"영상 없음: {clip}")
    ad = dur(a)
    D = max(LEAD + ad + TAIL, MIN_D)
    N = int(round(D * FPS)); D = N / FPS
    cd = dur(clip)
    if D <= cd:
        sp = min(cd / D, MAX_FAST)
        seg = D * sp
        start = max(cd - seg - 0.05, 0)
        vf = f"trim=start={start:.3f}:duration={seg:.3f},setpts=(PTS-STARTPTS)/{sp:.4f}"
        how = f"뒤 {seg:.2f}초 사용, x{sp:.2f} 속도"
    else:
        f = min(D / cd, MAX_SLOW)
        vf = f"setpts=(PTS-STARTPTS)*{f:.4f},tpad=stop_mode=clone:stop_duration=6"
        how = f"x{1 / f:.2f} 속도" + (" + 마지막 프레임 유지" if D > cd * MAX_SLOW else "")

    sub = TMP / f"sub{sid}.png"
    render_sub(s["narrator"], sub)
    vseg = TMP / f"v{sid}.mp4"
    fc = (f"[0:v]{vf},fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1[v];"
          f"[v][1:v]overlay=0:0,format=yuv420p[o]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-loop", "1", "-i", str(sub),
         "-filter_complex", fc, "-map", "[o]", "-frames:v", str(N), "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS), str(vseg)])

    aseg = TMP / f"a{sid}.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(a),
         "-af", f"adelay={int(LEAD * 1000)}:all=1,apad=whole_dur={D:.4f}",
         "-t", f"{D:.4f}", "-ar", "44100", "-ac", "2", str(aseg)])
    vlist.append(vseg.name); alist.append(aseg.name)
    timeline.append({"id": sid, "start": round(t, 3), "dur": round(D, 3), "clip_dur": round(cd, 3),
                     "speech": [round(t + LEAD, 3), round(t + LEAD + ad, 3)], "text": s["narrator"]})
    print(f"{sid}  대사 {ad:4.2f}s → 컷 {D:4.2f}s  (클립 {cd:4.2f}s, {how})")
    t += D

(TMP / "v.txt").write_text("".join(f"file '{n}'\n" for n in vlist), encoding="utf-8")
(TMP / "a.txt").write_text("".join(f"file '{n}'\n" for n in alist), encoding="utf-8")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "v.txt"), "-c", "copy", str(TMP / "video.mp4")])
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "a.txt"), "-c", "pcm_s16le", str(TMP / "narr.wav")])

total = t
final = OUT / "ep03.mp4"
vfade = f"fade=t=in:st=0:d=0.3,fade=t=out:st={total - 0.5:.3f}:d=0.5"
if BGM.exists():
    fc = (f"[0:v]{vfade}[v];"
          f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[n];"
          f"[2:a]aloop=loop=-1:size=2000000000,atrim=0:{total:.3f},volume=0.12,"
          f"afade=t=in:d=1.0,afade=t=out:st={total - 1.5:.3f}:d=1.5[b];"
          f"[n][b]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={total - 0.5:.3f}:d=0.5[a]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "video.mp4"), "-i", str(TMP / "narr.wav"), "-i", str(BGM),
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
         "-movflags", "+faststart", "-t", f"{total:.3f}", str(final)])
    music = "있음"
else:
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "video.mp4"), "-i", str(TMP / "narr.wav"),
         "-vf", vfade, "-af", f"loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.2,afade=t=out:st={total - 0.5:.3f}:d=0.5",
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-shortest", str(final)])
    music = "없음"

preview = OUT / "ep03_preview.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-vf", "scale=540:960",
     "-c:v", "libx264", "-preset", "medium", "-crf", "28", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(preview)])
(OUT / "timeline.json").write_text(json.dumps({"total": round(total, 3), "bgm": music, "shots": timeline},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
shutil.rmtree(TMP)
print(f"완료: {final.name} {total:.2f}초 ({final.stat().st_size // 1024}KB), 배경음악 {music}, preview {preview.stat().st_size // 1024}KB")
