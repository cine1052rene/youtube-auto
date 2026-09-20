# -*- coding: utf-8 -*-
"""내레이션 mp3를 받아쓰기해서 대본과 일치하는지 검사"""
import json, pathlib, sys, re
from faster_whisper import WhisperModel

H = pathlib.Path(__file__).parent
AUD = H / "audio" / "luna"
shots = json.load(open(H / "lines.json", encoding="utf-8"))["shots"]

model = WhisperModel("small", device="cpu", compute_type="int8")

def norm(s):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", s)

bad = []
for s in shots:
    f = AUD / f"{s['id']}.mp3"
    segs, info = model.transcribe(str(f), language=None, beam_size=5)
    text = " ".join(x.text.strip() for x in segs).strip()
    lang = info.language
    want = s["narrator"]
    ok = lang == "ko" and norm(text)[:6] and (norm(text) in norm(want) or norm(want)[:6] in norm(text) or norm(text)[:6] in norm(want))
    mark = "OK " if ok else "!! "
    print(f"{mark}{s['id']} [{lang} {info.language_probability:.2f}] 들린말: {text}")
    print(f"      대본  : {want}")
    if not ok:
        bad.append(s["id"])
print("\n문제 컷:", bad if bad else "없음")
