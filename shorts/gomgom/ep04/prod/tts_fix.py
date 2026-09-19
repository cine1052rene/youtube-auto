# -*- coding: utf-8 -*-
# 길이가 이상한 내레이션만 다시 생성 (한 줄씩 순차, stdin 안 먹음)
import json, subprocess, pathlib, re, sys, time
H = pathlib.Path(__file__).parent
AUD = H.parent / "audio" / "luna"; AUD.mkdir(parents=True, exist_ok=True)
HF = "C:/Users/cine1/AppData/Roaming/npm/higgsfield.cmd"
VOICE = "375a3398-e3b4-4f91-845d-42181e352899"
shots = json.load(open(H.parent / "lines.json", encoding="utf-8"))["shots"]

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)

def dur(p):
    r = sh(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)])
    try: return float(r.stdout.strip())
    except Exception: return 0.0

def gen(text, path):
    for _ in range(4):
        r = sh([HF,"generate","create","text2speech_v2","--prompt",text,"--variant","elevenlabs",
                "--voice_id",VOICE,"--voice_type","preset","--json"])
        try: jid = json.loads(r.stdout)[0]
        except Exception:
            time.sleep(20); continue
        w = sh([HF,"generate","wait",jid,"--json"])
        try: url = json.loads(w.stdout).get("result_url","")
        except Exception: url = ""
        if not url: time.sleep(10); continue
        sh(["curl","-s","-o",str(path),url])
        if path.exists() and dur(path) > 0.3: return dur(path)
        time.sleep(5)
    return 0.0

for s in shots:
    f = AUD / f"{s['id']}.mp3"
    text = s["narrator"]
    n = len(re.sub(r"[^가-힣0-9a-zA-Z]", "", text))
    need = n * 0.12          # 글자수 대비 최소 길이
    d = dur(f) if f.exists() else 0.0
    if d >= need:
        print(f"{s['id']} OK {d:.2f}s (필요 {need:.2f}s)"); continue
    print(f"{s['id']} 재생성 (현재 {d:.2f}s < {need:.2f}s): {text}")
    nd = gen(text, f)
    ok = "✔" if nd >= need else "✖"
    print(f"   → {nd:.2f}s {ok}")
