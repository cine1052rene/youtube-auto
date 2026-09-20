# -*- coding: utf-8 -*-
"""1~4화 내레이션 전체를 받아쓰기로 검증 (영어 혼입·엉뚱한 음성 탐지)"""
import json, pathlib, re, difflib
from faster_whisper import WhisperModel
H = pathlib.Path(__file__).parent
model = WhisperModel("small", device="cpu", compute_type="int8")
def norm(s): return re.sub(r"[^가-힣a-zA-Z0-9]", "", s)
bad_all = []
for ep in ["ep01","ep02","ep03","ep04"]:
    lj = H/ep/"lines.json"
    aud = H/ep/"audio"/"luna"
    if not lj.exists() or not aud.exists():
        print(f"[{ep}] 건너뜀"); continue
    shots = json.load(open(lj, encoding="utf-8"))["shots"]
    bad = []
    for s in shots:
        f = aud/f"{s['id']}.mp3"
        if not f.exists():
            bad.append((s['id'],'파일없음','')); continue
        segs, info = model.transcribe(str(f), beam_size=5)
        heard = " ".join(x.text.strip() for x in segs).strip()
        r = difflib.SequenceMatcher(None, norm(heard), norm(s["narrator"])).ratio()
        if info.language != "ko" or r < 0.6:
            bad.append((s['id'], f"{info.language} {r:.2f}", heard))
    print(f"[{ep}] {len(shots)}줄 중 문제 {len(bad)}개")
    for b in bad:
        print(f"   !! {b[0]} [{b[1]}] {b[2]}")
    bad_all += [(ep,)+b for b in bad]
print("\n총 문제:", len(bad_all))
