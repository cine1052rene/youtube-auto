# -*- coding: utf-8 -*-
"""7·8화 — 지금까지 만든 컷 전부 한 화면 비교 + 통과 지시 표시 + 7화 06 없는 비교본. 출력: review_site/public/all1012/"""
import json, os, shutil, subprocess, pathlib, datetime, html, hashlib
G = pathlib.Path(__file__).resolve().parent.parent
OUT = G / "review_site/public/all1012"; shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir(parents=True, exist_ok=True)

PASS = {"07": {"02", "07", "10", "11"}}  # 10/9 21:31 "7화 1,3,8,12 컷만 새로 만들고 나머지는 일단 보자"
NOTE = {
 "07": {
  "01": "10/9 새로 만들기 지시 → 10/10 · 10/11 콩이 자세 → 10/12 · <b>10/12 '새 컷' 선택</b>",
  "02": "<b class=p>통과 지시</b>(10/9 '나머지는 일단 보자') · 10/12 제가 지시 없이 뒤에 02b를 덧붙임 — <b class=r>02b도 벽돌이 혼자 솟아오름</b>",
  "03": "10/9 새로 만들기 지시 → 10/10",
  "06": "10/7 벽돌이 머리에 붙어 1회 버림 · 10/11 '늘어진다' → 10/12 제가 '벽돌이 혼자 날아와 쌓임'으로 만듦(반려)",
  "07": "<b class=p>통과 지시</b>(10/9 '나머지는 일단 보자') — 손대지 않음",
  "08": "10/9 곰곰이 복제 → 10/10 · 10/12 두 번 다시 만듦 · <b>10/12 '이전 컷' 선택</b>(=10/10판) · 08b는 10/12 덧붙임",
  "10": "<b class=p>통과 지시</b>(10/9 '나머지는 일단 보자') · 10/7 시도 2개 버림 · <b class=r>10/12 제가 통과 컷을 새로 만들어 바꿈</b>",
  "11": "<b class=p>통과 지시</b>(10/9 '나머지는 일단 보자') — 손대지 않음",
  "12": "10/9 · 10/10 · 10/12 다시 만듦 · <b>10/12 '새 컷' 선택</b>",
 },
 "08": {
  "02": "10/11 콩이 자세 → 10/12 · <b>10/12 '새 컷' 선택</b> · 02b는 10/12 덧붙임",
  "06": "10/9 토끼 크기 → 10/10 두 번(친구 2배·둥둥 날아다님) · 10/12 제자리 줌인 교체 2번(첫 판 토끼 2마리)",
  "07": "10/9 토끼가 끝까지 화면에 → 다시 만듦",
  "08": "10/9 관객석 실사 사람 → 다시 · 10/12 제자리 줌인 교체",
  "10": "10/9 콩이 크게 → 10/10 입이 이중 → 다시",
  "11": "11b는 10/12 덧붙임",
 }}

def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
def md5(p): return hashlib.md5(open(p, "rb").read()).hexdigest()
def poster(src, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur(src)/2:.2f}", "-i", str(src), "-frames:v", "1", "-vf", "scale=240:-2", "-q:v", "4", str(dst)])

def vid(src, name, cap, cls=""):
    shutil.copy(src, OUT / f"{name}.mp4"); poster(src, OUT / f"{name}.jpg")
    return f'<div class="c {cls}"><video src="{name}.mp4" poster="{name}.jpg" controls playsinline preload="metadata"></video><div class="t">{cap}</div></div>'

body = []
for ep in ["07", "08"]:
    E = G / f"ep{ep}"; C = E / "prod/clips"
    lines = {s["id"]: s["narrator"] for s in json.load(open(E / "lines.json", encoding="utf-8"))["shots"]}
    rows = []
    for k in sorted(lines):
        fs = [p for p in C.glob(f"{k}*.mp4") if p.stem == k or p.stem.startswith(k + "_") or p.stem.startswith(k + "b")]
        cur = {md5(q) for q in (C / f"{k}.mp4", C / f"{k}b.mp4") if q.exists()}
        seen, cells = {}, []
        for p in sorted(fs, key=lambda p: (p.stem.startswith(k + "b"), os.path.getmtime(p))):
            h = md5(p)
            if h in seen: continue
            seen[h] = 1
            t = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m/%d %H:%M")
            now = h in cur
            lab = ("b컷 · " if p.stem.startswith(k + "b") else "") + t + (" · <b>지금 사용</b>" if now else " · 안 씀")
            cells.append(vid(p, f"{ep}_{p.stem}", lab, "now" if now else ""))
        if len(cells) < 2 and k not in NOTE[ep] and k not in PASS.get(ep, set()): continue
        tag = ' <span class="v p">통과 지시</span>' if k in PASS.get(ep, set()) else ""
        rows.append(f'<section><h2>{int(ep)}화 {k}{tag} <span class="soft">{len(cells)}개</span></h2><p class="line">"{html.escape(lines[k])}"</p>'
                    f'<p class="soft">{NOTE[ep].get(k, "")}</p><div class="row">{"".join(cells)}</div></section>')
    body.append(f"<h1 style='margin-top:26px'>{int(ep)}화</h1>" + "".join(rows))

o = G / "speed_test/out"
no06 = "".join([
    vid(G / "ep07/prod/out/ep07_master_old1012b.mp4", "m_morning", "10/12 아침본 (06 = 풍선, 1.15배 느림)"),
    vid(G / "ep07/prod/out/ep07_master.mp4", "m_now", "지금 (06 = 벽돌 혼자 쌓임)", "bad"),
    vid(o / "ep07_NO06A.mp4", "m_A", "<b>A. 06 대사·화면 둘 다 빼기</b> · 43.3초", "now"),
    vid(o / "ep07_NO06B.mp4", "m_B", "<b>B. 06 대사는 두고 화면만 11(완성된 집)</b> · 47.9초 · 그 컷만 1.15배 느림", "now"),
])

CSS = ("body{font-family:system-ui,sans-serif;background:#FBF6EE;color:#3A2F25;margin:0;padding:18px 12px 60px;line-height:1.5}.w{max-width:1100px;margin:0 auto}"
       "h1{font-size:22px;margin:10px 0 4px}h2{font-size:16px;margin:0 0 2px}section{background:#FFFDF9;border:1px solid #EADFCF;border-radius:12px;padding:8px 10px;margin:6px 0}"
       ".soft{color:#85766A;font-size:13px;margin:2px 0}.line{font-size:14px;margin:2px 0}.rule{border-color:#D98E2B}"
       ".row{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px}.c{width:min(180px,44vw)}.c video{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:8px;display:block;border:3px solid #ddd;background:#000}"
       ".c.now video{border-color:#4CAF50}.c.bad video{border-color:#E57373}#pv{position:fixed;inset:0;background:#000c;display:none;align-items:center;justify-content:center;z-index:9}#pv video{max-height:88vh;max-width:94vw;border-radius:10px}.t{font-size:13px;color:#85766A;line-height:1.3;margin-top:2px}"
       ".v{display:inline-block;padding:1px 8px;border-radius:8px;font-size:12px;font-weight:700}.p{background:#E3F1FF;color:#1F5FA8}b.p{color:#1F5FA8}b.r{color:#C0392B}")
page = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>곰곰한 마음 · 7·8화 만든 컷 전부 비교</title><style>{CSS}</style></head><body><div class="w"><p class="soft"><a href="../index.html">← 목차</a></p>
<h1>🗂 7·8화 — 지금까지 만든 컷 전부</h1>
<p class="soft">초록 테두리 = 지금 완성본에 들어간 것 · 같은 컷의 모든 버전을 한 줄에 · 영상마다 바로 재생 · 하나를 틀면 다른 건 멈춰요</p>
<section class="rule"><h2>통과 지시 찾은 것</h2>
<p class="line">10/9 21:31 — <b>"7화 1,3,8,12 컷만 새로 만들고 나머지는 일단 보자"</b> → 7화 <b>02·07·10·11은 통과</b></p>
<p class="line">10/10 00:00 — <b>"너무 작거나 너무 크지만 않으면 어색하지 않은 장면에서는 그냥 넘어갈 수 있는데"</b> → 자세가 어색하지 않은 콩이 컷은 통과</p>
<p class="soft">제가 어긴 것: <b class=r>7화 10(통과 컷)을 10/12에 새로 만들어 바꿈</b> · <b class=r>7화 02(통과 컷)에 02b를 덧붙임</b> — 둘 다 아래 줄에서 이전 것과 비교할 수 있어요. 통과 컷으로 되돌리면 크레딧은 안 들어요.</p></section>
<section class="rule"><h2>7화 06 없이 — 완성본 비교</h2><p class="soft">A·B는 새로 만든 것 없이 조립만 다시 했어요(크레딧 0).</p><div class="row">{no06}</div></section>
{''.join(body)}
</div><div id="pv" onclick="if(event.target===this){{this.style.display='none';this.firstChild.pause()}}"><video controls playsinline></video></div>
<script>document.querySelectorAll('.c video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('.c video').forEach(o=>{{if(o!==v)o.pause()}})));</script></body></html>"""
(OUT / "index.html").write_text(page, encoding="utf-8")
print(OUT, len(list(OUT.glob("*.mp4"))), "videos")
