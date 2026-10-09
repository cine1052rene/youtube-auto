# -*- coding: utf-8 -*-
"""지정한 줄만 내레이션 다시 녹음: 후보 3개 중 받아쓰기 일치율·단어 확신도 최고 선택. 이전 파일은 *_old1009.mp3
사용: python tts_redo.py 07:04 07:06 08:02 ..."""
import json, pathlib, re, subprocess, sys, time, difflib, shutil
from faster_whisper import WhisperModel
H = pathlib.Path(__file__).parent
HF = "C:/Users/cine1/AppData/Roaming/npm/higgsfield.cmd"
VOICE = "375a3398-e3b4-4f91-845d-42181e352899"
m = WhisperModel("small", device="cpu", compute_type="int8")
n = lambda s: re.sub(r"[^가-힣0-9]", "", s)
sh = lambda c: subprocess.run(c, capture_output=True, text=True, encoding="utf-8", errors="replace")

def score(path, want):
    segs, _ = m.transcribe(str(path), beam_size=5, language="ko", word_timestamps=True)
    segs = list(segs); heard = "".join(x.text for x in segs)
    words = [w for x in segs for w in x.words]
    low = min((w.probability for w in words), default=0)
    r = difflib.SequenceMatcher(None, n(want), n(heard)).ratio()
    return r + 0.3 * low, r, low, heard.strip()

def gen(text, path):
    for _ in range(6):
        r = sh([HF, "generate", "create", "text2speech_v2", "--prompt", text, "--variant", "elevenlabs", "--voice_id", VOICE, "--voice_type", "preset", "--json"])
        try: jid = json.loads(r.stdout)[0]; break
        except Exception: time.sleep(30)
    else: return False
    w = sh([HF, "generate", "wait", jid, "--json"])
    try: url = json.loads(w.stdout).get("result_url", "")
    except Exception: url = ""
    if not url:
        w = sh([HF, "generate", "get", jid, "--json"])
        try: url = json.loads(w.stdout).get("result_url", "")
        except Exception: url = ""
    if not url: return False
    sh(["curl", "-s", "-o", str(path), url]); return path.exists() and path.stat().st_size > 2000

for arg in [a for a in sys.argv[1:] if not a.startswith("--")]:
    ep, sid = arg.split(":")
    want = next(s["narrator"] for s in json.load(open(H / f"ep{ep}/lines.json", encoding="utf-8"))["shots"] if s["id"] == sid)
    f = H / f"ep{ep}/audio/luna/{sid}.mp3"; old = f.with_name(f"{sid}_old1009.mp3")
    if not old.exists(): shutil.copy(f, old)
    base = f if "--keep" in sys.argv else old
    best = (score(base, want), base); print(f"{ep}-{sid} 현재 {best[0][1]:.2f}/{best[0][2]:.2f} {best[0][3]}", flush=True)
    for i in range(3):
        c = f.with_name(f"{sid}_cand{i}{'k' if '--keep' in sys.argv else ''}.mp3")
        if not gen(want, c): print("   생성 실패", flush=True); continue
        sc = score(c, want); print(f"   후보{i} {sc[1]:.2f}/{sc[2]:.2f} {sc[3]}", flush=True)
        if sc[0] > best[0][0]: best = (sc, c)
        if sc[1] >= 0.97 and sc[2] >= 0.7: break
    shutil.copy(best[1], f); print(f"   → 선택 {best[1].name}", flush=True)
