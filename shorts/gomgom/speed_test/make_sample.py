# -*- coding: utf-8 -*-
"""
말 속도·훅·효과음 비교 샘플 조립기 (원본 assemble.py와 같은 소재를 쓰고 출력만 따로 저장)
사용: python make_sample.py <ep:02|03> <speed> <tag> [--hook] [--sfx] [--bgm 경로|none]
- speed: 내레이션 배속(음높이 유지, atempo). 1.0이면 원래 속도
- 컷 길이 = 앞 0.05초(첫 컷 0) + 대사/배속 + 뒤 0.15초 (최소 1.5초)  ← 원본은 0.15 + 대사 + 0.30, 최소 2초
- --hook: 0~1.8초 화면 가운데 큰 제목 카드 + 첫 목소리 0초 시작
- --sfx : 컷별 효과음(sound/sfx) 살짝 깔기
출력: speed_test/out/ep{ep}_{tag}.mp4 (540x960 미리보기 화질)
"""
import json, subprocess, sys, pathlib, shutil, argparse
from PIL import Image, ImageDraw, ImageFont

G = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("ep"); ap.add_argument("speed", type=float); ap.add_argument("tag")
ap.add_argument("--hook", action="store_true"); ap.add_argument("--sfx", action="store_true")
ap.add_argument("--bgm", default="")
ap.add_argument("--sfxset", default="old")  # old | peep
ap.add_argument("--sfxgain", type=float, default=1.0)  # 효과음 전체 배율
ap.add_argument("--lead", type=float, default=0.05)  # 대사 앞 여백(초)
ap.add_argument("--tail", type=float, default=0.15)  # 대사 뒤 여백(초)
ap.add_argument("--hookdur", type=float, default=1.8)  # 첫 제목 카드 길이(초)
ap.add_argument("--end", type=float, default=0.0)  # 마지막 컷 뒤 여운(초)
ap.add_argument("--full", action="store_true")  # 업로드용 1080x1920 고화질(crf18·오디오 192k)
ap.add_argument("--premiere", action="store_true")  # 프리미어용 소재(자막 안 구운 컷·자막 PNG·트랙별 소리)+timeline.json 저장
ap.add_argument("--loop", action="store_true")  # 쇼츠 반복재생용: 검은 화면 페이드 없음, 음악은 처음 크기로 끝냄
A = ap.parse_args()

EP = G / f"ep{A.ep}"; PROD = EP / ("v3" if A.ep == "01" else "prod"); AUD = EP / "audio" / "luna"
OUT = G / "speed_test" / "out"; OUT.mkdir(parents=True, exist_ok=True)
TMP = OUT / f"tmp_{A.ep}_{A.tag}"; shutil.rmtree(TMP, ignore_errors=True); TMP.mkdir()
PR = G / "speed_test" / "premiere" / f"ep{A.ep}_{A.tag}"
if A.premiere:
    shutil.rmtree(PR, ignore_errors=True)
    for d in ("video", "sub", "narr", "sfx"):
        (PR / d).mkdir(parents=True)
TL = {"fps": 30, "width": 1080, "height": 1920, "cuts": [], "sfx": [], "bgm": None, "hook": None}
FONT = G / "fonts" / "GowunDodum-Regular.ttf"
SFXD = G / "sound" / "sfx_n"
BGM = pathlib.Path(A.bgm) if A.bgm and A.bgm != "none" else (PROD / "bgm.mp3" if A.bgm != "none" else None)

FPS, W, H = 30, 1080, 1920
LEAD, TAIL, MIN_D, MAX_FAST, MAX_SLOW = A.lead, A.tail, 1.5, 1.5, 1.4
HOOK_D = A.hookdur
HOOK = {"01": ["쉬어도 쉬어도", "피곤한 이유"], "02": ["칭찬은 잊고", "지적은 남는 이유"], "03": ["쾌락주의자가", "원한 건 빵 한 조각?"],
        "04": ["비교하면", "마음이 작아지는 이유"], "05": ["걱정을", "내려놓고 싶을 때"], "06": ["별일 아닌데", "괜히 서운할 때"],
        "07": ["왜 늘 계획보다", "오래 걸릴까?"], "08": ["다들 나만", "보는 것 같을 때"],
        "d01": ["“쉴 때 스트레칭하면", "개운해집니다~”"], "d02": ["콩이의", "작은 반짝임"]}
# (컷 id, 효과음, 컷 시작 후 몇 초, 볼륨)
PEEP = {
    "02": [("01", "peep_q", .9, .30), ("03", "peep1", .5, .28), ("05", "peep2", .8, .30), ("08", "peep1", .6, .30),
           ("09", "peep2", .4, .28), ("12", "peep_happy", .4, .30), ("13", "peep_sleepy", 1.2, .25)],
    "03": [("01", "peep_happy", .8, .28), ("02", "peep2", .4, .28), ("03", "peep1", .7, .30), ("05", "peep_happy", .5, .28),
           ("06", "peep_q", .4, .30), ("08", "peep1", .5, .28), ("09", "peep2", .6, .30), ("11", "peep_sleepy", 1.0, .25)],
}
CHICK = {
    "02": [("01", "chick2", .9, .6), ("03", "chick1", .5, .6), ("05", "chick_happy", .7, .55), ("08", "chick1", .6, .6),
           ("09", "chick2", .4, .55), ("12", "chick_happy", .4, .55), ("13", "chick_group", 1.2, .4)],
    "03": [("01", "chick_happy", .8, .55), ("02", "chick2", .4, .55), ("03", "chick1", .7, .6), ("05", "chick_happy", .5, .55),
           ("06", "chick1", .4, .6), ("08", "chick2", .5, .55), ("09", "chick1", .6, .6), ("11", "chick_group", 1.0, .4)],
}
REAL = {  # Pixabay 실제 녹음 (사용자 선택: footsteps1·door2·rain1·teacup1·wind3·page2·sparkle3·pop1)
    "02": [("02", "r_pop", .5, .35), ("03", "r_wind", .2, .35), ("04", "r_rain", 0, .22), ("06", "r_wind", .3, .35),
           ("07", "r_footsteps", .3, .4), ("08", "r_rain", 0, .28), ("11", "r_page", .1, .45), ("11", "r_sparkle", 1.0, .35),
           ("12", "r_pop", .5, .3)],
    "03": [("01", "r_sparkle", .2, .3), ("02", "r_footsteps", .2, .4), ("04", "r_pop", .3, .35), ("05", "r_teacup", .4, .5),
           ("06", "r_pop", .4, .4), ("07", "r_wind", .2, .3), ("08", "r_door", .1, .4)],
}
# 콩이 소리만 (Pixabay 실제 병아리·콩콩 녹음). 위치 "v+x" = 그 컷 대사가 끝난 뒤 x초(말과 안 겹치게)
KONG = {
    "02": [("01", "k_two", "v+0.0", .40), ("02", "k_fast", "v-0.1", .35), ("03", "k_slow", "v+0.0", .45),
           ("04", "k_hop2", "v+0.0", .60), ("05", "k_hop3", "v+0.0", .60), ("08", "k_slow", "v+0.0", .45),
           ("11", "k_hop2", "v+0.0", .60), ("12", "k_fast2", "v-0.1", .35), ("13", "k_slow", "v+0.3", .40)],
    "03": [("01", "k_two", "v+0.0", .40), ("02", "k_fast", "v-0.1", .35), ("03", "k_hop3", "v+0.0", .60),
           ("04", "k_slow", "v+0.0", .45), ("05", "k_fast2", "v-0.1", .35), ("06", "k_two", "v+0.0", .40),
           ("09", "k_hop2", "v+0.0", .60), ("10", "k_slow", "v+0.0", .40), ("11", "k_two", "v+0.3", .40)],
}
CUES = {
    "02": [("01", "pop", 0.0, .5), ("03", "whoosh", .2, .35), ("05", "hop", .6, .45), ("08", "drizzle", .1, .35),
           ("11", "chime", .3, .4), ("12", "hop", .5, .45), ("13", "twinkle", .2, .35)],
    "03": [("01", "pop", 0.0, .5), ("02", "whoosh", .3, .35), ("03", "hop", .6, .45), ("05", "clink", .5, .5),
           ("06", "hop", .4, .45), ("07", "chime", .4, .35), ("09", "hop", .7, .45), ("11", "twinkle", .2, .35)],
}
shots = json.load(open(EP / "lines.json", encoding="utf-8"))["shots"]
font = ImageFont.truetype(str(FONT), 66)
hfont = ImageFont.truetype(str(FONT), 112)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG ERROR:", " ".join(map(str, cmd))[:400]); print(r.stderr[-1200:]); sys.exit(1)


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
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lines = wrap(text); lh = 94; total = lh * len(lines); y0 = 1540 - total // 2
    maxw = max(font.getlength(l) for l in lines)
    d.rounded_rectangle([W / 2 - maxw / 2 - 46, y0 - 24, W / 2 + maxw / 2 + 46, y0 + total + 16], radius=44, fill=(58, 40, 28, 110))
    for i, l in enumerate(lines):
        d.text((W / 2 - font.getlength(l) / 2, y0 + i * lh), l, font=font, fill=(255, 250, 240, 255), stroke_width=5, stroke_fill=(72, 50, 34, 255))
    img.save(path)


def render_hook(lines, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    hf = hfont; size = 112
    while max(hf.getlength(l) for l in lines) > W - 200 and size > 70:  # 긴 줄은 화면 안에 들어오게 글자 축소
        size -= 4; hf = ImageFont.truetype(str(FONT), size)
    lh = int(size * 1.34); total = lh * len(lines); y0 = 330 - total // 2
    maxw = max(hf.getlength(l) for l in lines)
    d.rounded_rectangle([W / 2 - maxw / 2 - 64, y0 - 44, W / 2 + maxw / 2 + 64, y0 + total + 24], radius=60, fill=(255, 248, 236, 228))
    for i, l in enumerate(lines):
        d.text((W / 2 - hf.getlength(l) / 2, y0 + i * lh), l, font=hf, fill=(74, 52, 36, 255))
    img.save(path)


vlist, alist, starts, vend = [], [], {}, {}
t = 0.0
for i, s in enumerate(shots):
    sid = s["id"]; a = AUD / f"{sid}.mp3"; clip = PROD / "clips" / f"{sid}.mp4"
    lead = 0.0 if i == 0 else LEAD
    ad = dur(a) / A.speed
    D = max(lead + ad + TAIL, MIN_D) + (A.end if i == len(shots) - 1 else 0); N = int(round(D * FPS)); D = N / FPS
    cd = dur(clip)
    if D <= cd:
        sp = min(cd / D, MAX_FAST); seg = D * sp; st = max(cd - seg - 0.05, 0)
        vf = f"trim=start={st:.3f}:duration={seg:.3f},setpts=(PTS-STARTPTS)/{sp:.4f}"
    else:
        f = min(D / cd, MAX_SLOW)
        vf = f"setpts=(PTS-STARTPTS)*{f:.4f},tpad=stop_mode=clone:stop_duration=6"
    sub = TMP / f"sub{sid}.png"; render_sub(s["narrator"], sub)
    vseg = TMP / f"v{sid}.mp4"
    ins = ["-i", str(clip), "-loop", "1", "-i", str(sub)]
    fc = f"[0:v]{vf},fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1[v];[v][1:v]overlay=0:0[s]"
    if False:  # 훅은 완성 영상 위에 얹음(아래 최종 단계)
        hk = TMP / "hook.png"; render_hook(HOOK[A.ep], hk)
        ins += ["-loop", "1", "-i", str(hk)]
        fc += f";[2:v]format=rgba,fade=t=out:st={HOOK_D - 0.3:.2f}:d=0.3:alpha=1[h];[s][h]overlay=0:0:enable='lt(t,{HOOK_D})',format=yuv420p[o]"
    else:
        fc += ";[s]format=yuv420p[o]"
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc, "-map", "[o]", "-frames:v", str(N), "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS), str(vseg)])
    aseg = TMP / f"a{sid}.wav"
    atempo = f"atempo={A.speed:.3f}," if abs(A.speed - 1) > 1e-3 else ""
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(a),
         "-af", f"{atempo}adelay={int(lead * 1000)}:all=1,apad=whole_dur={D:.4f}", "-t", f"{D:.4f}", "-ar", "44100", "-ac", "2", str(aseg)])
    if A.premiere:  # 자막 없이 같은 길이·같은 배속으로 고화질 컷
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vf", f"{vf},fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p",
             "-frames:v", str(N), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", str(FPS), str(PR / "video" / f"{sid}.mp4")])
        shutil.copy(sub, PR / "sub" / f"{sid}.png"); shutil.copy(aseg, PR / "narr" / f"{sid}.wav")
        TL["cuts"].append({"id": sid, "start": round(t * FPS), "frames": N, "text": s["narrator"]})
    vlist.append(vseg.name); alist.append(aseg.name); starts[sid] = t; vend[sid] = t + lead + ad
    t += D

(TMP / "v.txt").write_text("".join(f"file '{n}'\n" for n in vlist), encoding="utf-8")
(TMP / "a.txt").write_text("".join(f"file '{n}'\n" for n in alist), encoding="utf-8")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "v.txt"), "-c", "copy", str(TMP / "video.mp4")])
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "a.txt"), "-c", "pcm_s16le", str(TMP / "narr.wav")])
total = t
T0 = (total - A.end) if A.end else total + 99   # 여운 시작(대사 끝) 시점
VF = 1.2 if A.end else 0.5   # 영상 페이드아웃 길이
AF = 1.3 if A.end else 0.5   # 소리 페이드아웃 길이

ins = ["-i", str(TMP / "video.mp4"), "-i", str(TMP / "narr.wav")]
vin = "[0:v]"
if A.hook:
    hk = TMP / "hook.png"; render_hook(HOOK[A.ep], hk)
    if A.premiere:
        shutil.copy(hk, PR / "hook.png"); TL["hook"] = {"file": "hook.png", "frames": round(HOOK_D * FPS)}
    ins += ["-loop", "1", "-t", f"{HOOK_D:.2f}", "-i", str(hk)]
    fc = (f"[2:v]format=rgba,fade=t=out:st={HOOK_D - 0.4:.2f}:d=0.4:alpha=1[h];"
          f"[0:v][h]overlay=0:0:eof_action=pass[hv];")
    vin = "[hv]"
else:
    fc = ""
vfx = "" if A.loop else f"fade=t=in:st=0:d=0.2,fade=t=out:st={total - VF:.3f}:d={VF},"
fc += f"{vin}{vfx}" + ("format=yuv420p[v];" if A.full else "scale=540:960[v];") + f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[n]"
mix = ["[n]"]; k = 3 if A.hook else 2
if BGM:
    ins += ["-i", str(BGM)]
    if A.loop:  # 대사 끝나면 살짝 올라갔다가 마지막 0.6초 동안 처음 크기(0.12)로 돌아옴 → 다시 시작해도 음악 크기가 같음
        bvol = (f"volume='if(lt(t,{T0:.3f}),0.12,if(lt(t,{total - 0.6:.3f}),0.12+0.2*min((t-{T0:.3f})/0.4,1),0.12+0.2*max(({total:.3f}-t)/0.6,0)))':eval=frame,"
                f"afade=t=in:d=0.03,afade=t=out:st={total - 0.06:.3f}:d=0.06")
    else:
        bvol = (f"volume='if(gt(t,{T0:.3f}),0.12+0.38*min((t-{T0:.3f})/0.5,1),0.12)':eval=frame,afade=t=in:d=0.6,"
                f"afade=t=out:st={total - (AF if A.end else 1.5):.3f}:d={AF if A.end else 1.5}")
    fc += f";[{k}:a]aloop=loop=-1:size=2000000000,atrim=0:{total:.3f},{bvol}[b]"
    if A.premiere:  # 음량 변화(여운 상승·루프 복귀)까지 넣은 배경음악 한 덩어리
        run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(BGM), "-af", bvol, "-t", f"{total:.3f}",
             "-ar", "48000", "-ac", "2", str(PR / "bgm.wav")])
        TL["bgm"] = "bgm.wav"
    mix.append("[b]"); k += 1
if A.sfx:
    for cid, name, off, vol in {"peep": PEEP, "chick": CHICK, "real": REAL, "kong": KONG}.get(A.sfxset, CUES)[A.ep]:
        f = next(SFXD.glob(f"{name}.*"), None)
        if not f or cid not in starts:
            continue
        at = vend[cid] + float(off[1:]) if isinstance(off, str) else starts[cid] + off
        ms = int(max(at, 0) * 1000)
        if A.premiere:
            shutil.copy(f, PR / "sfx" / f.name)
            TL["sfx"].append({"cut": cid, "file": f.name, "start": round(max(at, 0) * FPS), "dur": dur(f), "gain": round(vol * A.sfxgain, 3)})
        ins += ["-i", str(f)]
        fc += f";[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={vol * A.sfxgain:.3f},adelay={ms}:all=1[x{k}]"
        mix.append(f"[x{k}]"); k += 1
fc += f";{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,afade=t=out:st={total - (0.06 if A.loop else AF):.3f}:d={0.06 if A.loop else AF}[a]"
final = OUT / f"ep{A.ep}_{A.tag}.mp4"
run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
     "-c:v", "libx264", "-preset", "slow" if A.full else "medium", "-crf", "18" if A.full else "30", "-c:a", "aac", "-b:a", "192k" if A.full else "96k", "-movflags", "+faststart",
     "-t", f"{total:.3f}", str(final)])
shutil.rmtree(TMP)
if A.premiere:
    TL.update(name=f"gomgom_ep{A.ep}_{A.tag}", total=round(total * FPS))
    json.dump(TL, open(PR / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"ep": A.ep, "tag": A.tag, "speed": A.speed, "hook": A.hook, "sfx": A.sfx, "bgm": BGM.name if BGM else None,
           "total": round(total, 2)}, open(OUT / f"ep{A.ep}_{A.tag}.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"{final.name} {total:.1f}초 {final.stat().st_size // 1024}KB")
