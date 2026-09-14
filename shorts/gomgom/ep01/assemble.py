# -*- coding: utf-8 -*-
"""
곰곰한 마음 1화 조립: 컷별 내레이션 길이에 맞춰 영상/그림을 이어 붙임
사용: python assemble.py luna|bear
출력: out/ep01_<voice>.mp4 (1080x1920), out/ep01_<voice>_preview.mp4 (540x960), out/timeline_<voice>.json
- 그림(S): 천천히 확대/축소(Ken Burns), 컷마다 방향 교대
- 영상(V): 대사가 클립보다 길면 최대 1.4배까지 느리게, 그래도 모자라면 마지막 프레임 유지
- 자막·배경음악 없음 (목소리 비교용)
"""
import json, subprocess, sys, pathlib, shutil

EP = pathlib.Path(__file__).parent
voice = sys.argv[1]
AUD = EP / "audio" / voice
OUT = EP / "out"; OUT.mkdir(exist_ok=True)
TMP = OUT / f"tmp_{voice}"
if TMP.exists():
    shutil.rmtree(TMP)
TMP.mkdir()

FPS, W, H = 30, 1080, 1920
LEAD, TAIL, MIN_S = 0.15, 0.30, 1.8
shots = json.load(open(EP / "lines.json", encoding="utf-8"))["shots"]
line_key = "narrator" if voice == "luna" else "bear"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG ERROR:", " ".join(map(str, cmd))[:400])
        print(r.stderr[-1200:])
        sys.exit(1)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def audio_file(sid):
    for ext in ("wav", "mp3"):
        p = AUD / f"{sid}.{ext}"
        if p.exists():
            return p
    sys.exit(f"오디오 없음: {AUD}/{sid}")


vlist, alist, timeline = [], [], []
t = 0.0
still_idx = 0
for s in shots:
    a = audio_file(s["id"])
    ad = dur(a)
    D = LEAD + ad + TAIL
    if s["type"] == "S":
        D = max(D, MIN_S)
    N = int(round(D * FPS))
    D = N / FPS
    src = EP / s["src"]
    vseg = TMP / f"v{s['id']}.mp4"

    if s["type"] == "S":
        zoom_in = still_idx % 2 == 0
        still_idx += 1
        z = f"1+0.07*on/{N}" if zoom_in else f"1.07-0.07*on/{N}"
        vf = (f"scale=2160:3840:flags=lanczos,"
              f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p")
        run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(src), "-vf", vf,
             "-frames:v", str(N), "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS), str(vseg)])
        how = "zoom in" if zoom_in else "zoom out"
    else:
        cd = dur(src)
        factor = min(max(D / cd, 1.0), 1.4)
        vf = (f"setpts=PTS*{factor:.4f},fps={FPS},scale={W}:{H}:flags=lanczos,"
              f"tpad=stop_mode=clone:stop_duration=5,format=yuv420p")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", vf, "-an",
             "-frames:v", str(N), "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS), str(vseg)])
        how = f"x{factor:.2f} speed" + (" +hold" if D > cd * 1.4 else "")

    aseg = TMP / f"a{s['id']}.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(a),
         "-af", f"adelay={int(LEAD * 1000)}:all=1,apad=whole_dur={D:.4f}",
         "-t", f"{D:.4f}", "-ar", "44100", "-ac", "2", str(aseg)])

    vlist.append(vseg.name)
    alist.append(aseg.name)
    timeline.append({"id": s["id"], "type": s["type"], "start": round(t, 3), "dur": round(D, 3),
                     "speech_start": round(t + LEAD, 3), "speech_end": round(t + LEAD + ad, 3),
                     "text": s[line_key]})
    print(f"{s['id']} {s['type']}  대사 {ad:4.2f}s → 컷 {D:4.2f}s  ({how})")
    t += D

(TMP / "v.txt").write_text("".join(f"file '{n}'\n" for n in vlist), encoding="utf-8")
(TMP / "a.txt").write_text("".join(f"file '{n}'\n" for n in alist), encoding="utf-8")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "v.txt"),
     "-c", "copy", str(TMP / "video.mp4")])
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "a.txt"),
     "-c", "pcm_s16le", str(TMP / "narr.wav")])

total = t
final = OUT / f"ep01_{voice}.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(TMP / "video.mp4"), "-i", str(TMP / "narr.wav"),
     "-vf", f"fade=t=in:st=0:d=0.3,fade=t=out:st={total - 0.5:.3f}:d=0.5",
     "-af", f"loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.2,afade=t=out:st={total - 0.5:.3f}:d=0.5",
     "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
     "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", "-shortest", str(final)])
preview = OUT / f"ep01_{voice}_preview.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-vf", "scale=540:960",
     "-c:v", "libx264", "-preset", "medium", "-crf", "30", "-c:a", "aac", "-b:a", "96k",
     "-movflags", "+faststart", str(preview)])

(OUT / f"timeline_{voice}.json").write_text(json.dumps({"voice": voice, "total": round(total, 3), "shots": timeline},
                                                      ensure_ascii=False, indent=1), encoding="utf-8")
shutil.rmtree(TMP)
print(f"완료: {final.name} {total:.2f}s ({final.stat().st_size // 1024}KB), preview {preview.stat().st_size // 1024}KB")
