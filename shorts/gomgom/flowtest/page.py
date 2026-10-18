# -*- coding: utf-8 -*-
import shutil, subprocess, pathlib, html
H = pathlib.Path(__file__).parent; OUT = H.parent / "review_site/public/flow1017"
def card(v, lab, note, cls=""):
    shutil.copy(H / f"{v}.mp4", OUT / f"{v}.mp4")
    subprocess.run(["ffmpeg","-v","error","-y","-ss","1","-i",str(H/f"{v}.mp4"),"-frames:v","1","-vf","scale=240:-2","-q:v","4",str(OUT/f"{v}.jpg")])
    return f'<div class="c {cls}"><video src="{v}.mp4" poster="{v}.jpg" controls playsinline preload="metadata"></video><div class="t"><b>{lab}</b></div><div class="l">{note}</div></div>'
ROWS = [
 ("7화 01 — 해 지는 작업대", [card("h_07-01","힉스필드 (Seedance 1.5 · 4초)","소리 없음 · 끝에서 콩이가 조금 커짐"), card("f_07-01_omni","Flow (Omni 1.1 Flash · 4초)","소리 있음(작게, 작업실 분위기음) · 카메라가 창 쪽으로 돌고 곰곰이가 창을 봄 · 콩이 크기 유지","now")]),
 ("7화 10 — 시계바늘 돌리기", [card("h_07-10","힉스필드 (Seedance 1.5 · 4초)","소리 없음 · 곰곰이가 정면으로 바늘을 돌림"), card("f_07-10_omni","Flow (Omni 1.1 Flash · 4초)","소리 있음 · 곰곰이가 몸을 돌려 바늘을 돌리고 다시 정면으로 · 콩이 시계 위 그대로","now")]),
 ("8화 02 — 과일 가게 시장", [card("h_08-02","힉스필드 (Seedance 1.5 · 4초)","소리 없음 · 카메라가 다가가며 콩이가 크게 보임"), card("f_08-02_omni","Flow (Omni 1.1 Flash · 4초)","소리 있음 · 시장 소음에 사람 말소리 같은 웅성거림이 섞임(받아쓰기에 일본어처럼 잡힘) · 곰곰이 뒷모습으로 돌아섬","now"), card("f_08-02_veo","Flow (Veo 3.1 Lite · 8초)","소리 가장 큼·또렷함 · 8초 고정 · 뒤돌았다가 다시 정면, 손 흔듦","now")]),
]
CSS = ("*{box-sizing:border-box}body{overflow-wrap:anywhere;font-family:system-ui,sans-serif;background:#FBF6EE;color:#3A2F25;margin:0;padding:18px 12px 60px;line-height:1.5}.w{max-width:1100px;margin:0 auto}"
       "h1{font-size:22px;margin:10px 0 4px}h2{font-size:17px;margin:0 0 6px}section{background:#FFFDF9;border:1px solid #EADFCF;border-radius:12px;padding:10px 12px;margin:8px 0}"
       ".soft{color:#85766A;font-size:13px}.rule{border-color:#D98E2B}.row{display:flex;gap:8px;flex-wrap:wrap}.c{width:min(180px,44vw)}"
       ".c video{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:8px;display:block;border:3px solid #ddd;background:#000}.c.now video{border-color:#4C8BF5}.t{font-size:12px;color:#85766A;margin-top:3px}.l{font-size:13px;margin-top:2px}")
secs = "".join(f'<section><h2>{t}</h2><div class="row">{"".join(c)}</div></section>' for t, c in ROWS)
page = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>곰곰한 마음 · 힉스필드 vs 구글 Flow</title><style>{CSS}</style></head><body><div class="w"><p class="soft"><a href="../index.html">← 목차</a></p>
<h1>🎬 힉스필드 vs 구글 Flow — 같은 그림·같은 프롬프트</h1>
<p class="soft">시작 그림과 영상 프롬프트를 힉스필드 때와 글자 하나 다르지 않게 넣었어요. 파란 테두리 = Flow. <b>소리를 켜고</b> 들어보세요(힉스필드 영상은 원래 소리 없이 만들었어요).</p>
<section class="rule"><h2>골라 주실 것</h2><p>① Flow 효과음이 쓸 만한지 (시장 컷의 웅성거림처럼 말소리가 섞이는 건 괜찮은지)<br>② 화면은 어느 쪽이 나은지<br>③ 앞으로 Flow를 쓸지 — 쓴다면 Omni(4초, 7크레딧) / Veo Lite(8초, 10크레딧) 중 어느 쪽</p></section>
{secs}
<p class="soft">Flow 크레딧 31 사용(1050 → 1019, PRO 요금제 포함분) · 힉스필드 크레딧 0 · 파일 C:\project\youtube\shorts\gomgom\flowtest\</p>
</div><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{{if(o!==v)o.pause()}})));</script></body></html>"""
(OUT / "index.html").write_text(page, encoding="utf-8"); print(OUT)
