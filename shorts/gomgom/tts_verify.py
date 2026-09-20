# -*- coding: utf-8 -*-
"""
내레이션 생성 + 받아쓰기 검증 (모든 화 공용)

ElevenLabs가 한국어 대본에 엉뚱한 영어 음성을 돌려주는 사고가 있어(4화 01·09),
길이가 아니라 '실제로 뭐라고 말하는지'로 검사한다.

사용:
  python tts_verify.py ep05          # 없는 줄 생성 + 전체 검증
  python tts_verify.py ep05 --check  # 생성 없이 검사만
"""
import json, pathlib, re, subprocess, sys, time, difflib
from faster_whisper import WhisperModel

H = pathlib.Path(__file__).parent
HF = "C:/Users/cine1/AppData/Roaming/npm/higgsfield.cmd"
VOICE = "375a3398-e3b4-4f91-845d-42181e352899"
MIN_RATIO = 0.6
MAX_TRY = 4

ep = sys.argv[1] if len(sys.argv) > 1 else "ep05"
check_only = "--check" in sys.argv
EP = H / ep
AUD = EP / "audio" / "luna"
AUD.mkdir(parents=True, exist_ok=True)
shots = json.load(open(EP / "lines.json", encoding="utf-8"))["shots"]
model = WhisperModel("small", device="cpu", compute_type="int8")


def norm(s):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", s)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", stdin=subprocess.DEVNULL)


def judge(path, want):
    """(통과여부, 언어, 들린말, 일치율)"""
    if not path.exists() or path.stat().st_size < 2000:
        return False, "-", "(없음)", 0.0
    segs, info = model.transcribe(str(path), beam_size=5)
    heard = " ".join(x.text.strip() for x in segs).strip()
    ratio = difflib.SequenceMatcher(None, norm(heard), norm(want)).ratio()
    return (info.language == "ko" and ratio >= MIN_RATIO), info.language, heard, ratio


def regen(text, path):
    r = sh([HF, "generate", "create", "text2speech_v2", "--prompt", text,
            "--variant", "elevenlabs", "--voice_id", VOICE, "--voice_type", "preset", "--json"])
    try:
        jid = json.loads(r.stdout)[0]
    except Exception:
        return False
    w = sh([HF, "generate", "wait", jid, "--json"])
    try:
        url = json.loads(w.stdout).get("result_url", "")
    except Exception:
        url = ""
    if not url:
        return False
    sh(["curl", "-s", "-o", str(path), url])
    return path.exists() and path.stat().st_size > 2000


bad = []
for s in shots:
    f = AUD / f"{s['id']}.mp3"
    ok, lang, heard, ratio = judge(f, s["narrator"])
    print(f"{'OK ' if ok else '!! '}{s['id']} [{lang} {ratio:.2f}] {heard}", flush=True)
    if ok or check_only:
        if not ok:
            bad.append(s["id"])
        continue
    for t in range(MAX_TRY):
        print(f"   생성 {t+1}회차...", flush=True)
        if not regen(s["narrator"], f):
            time.sleep(20)
            continue
        ok, lang, heard, ratio = judge(f, s["narrator"])
        print(f"   → [{lang} {ratio:.2f}] {heard}", flush=True)
        if ok:
            break
        time.sleep(5)
    if not ok:
        bad.append(s["id"])

total = 0.0
for s in shots:
    f = AUD / f"{s['id']}.mp3"
    if f.exists():
        r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)])
        try:
            total += float(r.stdout.strip())
        except Exception:
            pass
print(f"\n{ep} 내레이션 합계 {total:.1f}초 · 남은 문제:", bad if bad else "없음")
sys.exit(1 if bad else 0)
