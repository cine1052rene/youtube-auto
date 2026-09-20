# -*- coding: utf-8 -*-
"""
내레이션 mp3를 받아쓰기로 검증하고, 대본과 다르면 다시 생성한다.
ElevenLabs가 한국어 대본에 엉뚱한 영어 음성을 돌려주는 사고가 있어 만듦(4화 01·09).

사용:
  python tts_verify.py            # 전체 검사만
  python tts_verify.py --fix      # 문제 있는 줄만 재생성 + 재검증
"""
import json, pathlib, re, subprocess, sys, time, difflib
from faster_whisper import WhisperModel

H = pathlib.Path(__file__).parent
AUD = H / "audio" / "luna"
HF = "C:/Users/cine1/AppData/Roaming/npm/higgsfield.cmd"
VOICE = "375a3398-e3b4-4f91-845d-42181e352899"
MIN_RATIO = 0.6          # 대본과의 글자 일치율 하한
MAX_TRY = 4

shots = json.load(open(H / "lines.json", encoding="utf-8"))["shots"]
model = WhisperModel("small", device="cpu", compute_type="int8")


def norm(s):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", s)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", stdin=subprocess.DEVNULL)


def listen(path):
    """(언어, 들린 문장) 반환"""
    segs, info = model.transcribe(str(path), beam_size=5)
    return info.language, " ".join(x.text.strip() for x in segs).strip()


def judge(path, want):
    if not path.exists():
        return False, "ko", "(파일 없음)", 0.0
    lang, heard = listen(path)
    ratio = difflib.SequenceMatcher(None, norm(heard), norm(want)).ratio()
    ok = (lang == "ko") and (ratio >= MIN_RATIO)
    return ok, lang, heard, ratio


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


fix = "--fix" in sys.argv
bad = []
for s in shots:
    f = AUD / f"{s['id']}.mp3"
    ok, lang, heard, ratio = judge(f, s["narrator"])
    print(f"{'OK ' if ok else '!! '}{s['id']} [{lang} 일치율 {ratio:.2f}] {heard}")
    if ok:
        continue
    bad.append(s["id"])
    if not fix:
        continue
    for t in range(MAX_TRY):
        print(f"   재생성 {t+1}회차...")
        if not regen(s["narrator"], f):
            time.sleep(15)
            continue
        ok, lang, heard, ratio = judge(f, s["narrator"])
        print(f"   → [{lang} {ratio:.2f}] {heard}")
        if ok:
            bad.remove(s["id"])
            break
        time.sleep(5)

print("\n남은 문제:", bad if bad else "없음")
sys.exit(1 if bad else 0)
