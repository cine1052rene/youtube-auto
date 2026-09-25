# -*- coding: utf-8 -*-
"""Emily 목소리로 15줄 생성 + 받아쓰기 검증(한국어·일치율 0.55 미만이면 재생성)"""
import json, pathlib, re, subprocess, time, difflib
from faster_whisper import WhisperModel
H = pathlib.Path(__file__).parent
HF = "C:/Users/cine1/AppData/Roaming/npm/higgsfield.cmd"
VOICE = "6b3e3642-f7b7-4cb8-9688-51e233c4b92f"  # Emily
lines = json.load(open(H/"lines.json", encoding="utf-8"))
model = WhisperModel("small", device="cpu", compute_type="int8")
norm = lambda s: re.sub(r"[^가-힣0-9]", "", s)
def sh(c): return subprocess.run(c, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
def dur(p): return float(sh(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).stdout.strip() or 0)
def judge(p, want):
    if not p.exists() or p.stat().st_size < 2000: return False, 0, "(없음)"
    s, i = model.transcribe(str(p), beam_size=5)
    heard = " ".join(x.text.strip() for x in s)
    r = difflib.SequenceMatcher(None, norm(heard), norm(want)).ratio()
    return (i.language == "ko" and r >= 0.55), r, heard
def gen(text, p):
    r = sh([HF,"generate","create","text2speech_v2","--prompt",text,"--variant","elevenlabs","--voice_id",VOICE,"--voice_type","preset","--json"])
    try: jid = json.loads(r.stdout)[0]
    except Exception: return False
    w = sh([HF,"generate","wait",jid,"--json"])
    try: url = json.loads(w.stdout).get("result_url","")
    except Exception: url = ""
    if not url: return False
    sh(["curl","-s","-o",str(p),url]); return p.exists()
for i, t in enumerate(lines, 1):
    p = H/"tts"/f"{i:02d}.mp3"
    ok, r, heard = judge(p, t)
    tries = 0
    while not ok and tries < 4:
        tries += 1
        if not gen(t, p): time.sleep(15); continue
        ok, r, heard = judge(p, t)
    print(f"{'OK' if ok else '!!'} {i:02d} {dur(p):4.2f}s r={r:.2f} | {heard}", flush=True)
