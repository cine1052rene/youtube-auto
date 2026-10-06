# -*- coding: utf-8 -*-
"""시즌1 마스터(1.15배·간격K·제목카드·루프) 기준 컷별 점검 페이지 — 4·6화
컷 시간은 make_sample.py와 같은 공식으로 계산(앞 0.15/첫 컷 0, 대사/1.15, 뒤 0.45, 최소 1.5초, 마지막 +1.2초, 30fps 반올림)"""
import base64, json, pathlib, subprocess, sys
from build import G, OUT, PKG, NOTES, REGEN, ANALYSIS, CHECKS, CSS, frame_b64

SPEED, LEAD, TAIL, MIN_D, END, FPS = 1.15, 0.15, 0.45, 1.5, 1.2, 30


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def plan(n):
    shots = json.load(open(G / f"ep{n}" / "lines.json", encoding="utf-8"))["shots"]
    t, out = 0.0, []
    for i, s in enumerate(shots):
        lead = 0.0 if i == 0 else LEAD
        d = max(lead + dur(G / f"ep{n}" / "audio" / "luna" / f"{s['id']}.mp3") / SPEED + TAIL, MIN_D) + (END if i == len(shots) - 1 else 0)
        d = round(d * FPS) / FPS
        out.append({"id": s["id"], "text": s["narrator"], "model": s.get("model", "seedance1_5"), "start": t, "dur": d})
        t += d
    return out, t


def build(n, idx):
    e = PKG[idx]
    master = G / f"ep{n}" / "prod" / "out" / f"ep{n}_master_s1.mp4"
    prev = G / "speed_test" / "out_s" / f"ep{n}_master_s1_prev.mp4"
    cuts, total = plan(n)
    real = dur(master)
    vid = base64.b64encode(prev.read_bytes()).decode()
    cards = []
    for s in cuts:
        sec = s["model"].split(":")[1] if ":" in s["model"] else "4"
        rg = REGEN.get(n, {}).get(s["id"])
        mdl = f'<div class="md">그림 Seedream 5 Lite<br>영상 Seedance 1.5 · {sec}초' + (f'<br><span class="rg">{rg}</span>' if rg else '') + '</div>'
        img = frame_b64(master, s["start"] + s["dur"] * 0.55)
        cards.append(
            f'<div class="cut"><img src="data:image/jpeg;base64,{img}" onclick="seek({s["start"]:.2f})" alt="{s["id"]}번 장면">'
            f'<div class="c"><div class="n">{s["id"]}</div><div>{s["text"]}</div>'
            f'<div class="t">{s["start"]:.1f}초 ~ {s["start"] + s["dur"]:.1f}초</div>{mdl}</div></div>')
    nt = NOTES[n]
    notes = "".join(f'<div class="note"><b class="h">{h}</b><p>{b}</p></div>' for h, b in nt["made"])
    ana = "".join(f'<div class="note ana"><b class="h">{h}</b><p>{b}</p></div>' for h, b in ANALYSIS.get(n, []))
    ana_sec = f'<section><h2>6화 분석 (10/4)</h2><div class="notes">{ana}</div></section>' if ana else ""
    checks = "".join(f'<div class="chk">{c}</div>' for c in CHECKS)
    when = e["when"].split(" — ")[0]
    path = str(master).replace("/", "\\")
    html = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 {int(n)}화 마스터 컷별 점검</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<section>
<p class="eye">곰곰한 마음 · {int(n)}화 · 시즌1 마스터 컷별 점검</p>
<h1>{e["title"]}</h1>
<p class="soft">{nt["sub"]}</p>
<div class="meta"><span class="pill">공개 {when}</span><span class="pill">{real:.1f}초</span><span class="pill">{len(cuts)}컷</span>
<span class="pill">1.15배 · 간격 K · 제목 카드 3초 · 루프 · 효과음 없음</span></div>
<p class="soft" style="margin-top:10px;font-size:12px">원본: {path}</p>
</section>
<section class="stage"><video id="v" src="data:video/mp4;base64,{vid}" controls loop playsinline preload="metadata"></video></section>
<section>
<h2>컷별 장면</h2>
<p class="soft" style="margin-bottom:12px">사진을 누르면 영상이 그 장면으로 이동해요. 시간은 마스터 영상 기준이에요. 고치고 싶은 컷은 <b>번호</b>로 알려 주세요.</p>
<div class="cuts">{"".join(cards)}</div>
</section>
{ana_sec}
<section>
<h2>만들면서 고친 것</h2>
<div class="notes">{notes}</div>
</section>
<section>
<h2>보면서 확인할 것</h2>
<div class="checks">{checks}</div>
</section>
<section class="ask"><div class="q"><b>점검 결과를 알려 주세요</b>
괜찮으면 "{int(n)}화 OK", 고칠 게 있으면 "{int(n)}화 07번 콩이가 이상해"처럼 <b>컷 번호 + 이유</b>로 보내 주세요.</div></section>
</div>
<script>function seek(t){{const v=document.getElementById('v');v.currentTime=t;v.play();v.scrollIntoView({{behavior:'smooth',block:'center'}})}}</script>
</body></html>'''
    p = OUT / f"gomgom_ep{n}_master_cuts.html"
    p.write_text(html, encoding="utf-8")
    print(p, f"계산 {total:.2f}초 / 실제 {real:.2f}초", round(p.stat().st_size / 1048576, 1), "MB")


if __name__ == "__main__":
    for n, i in (("04", 3), ("06", 5)):
        build(n, i)
