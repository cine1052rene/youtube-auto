# -*- coding: utf-8 -*-
"""콩이 소리만(빠른 삐약·느린 삐약·콩콩) 넣은 2·3화 샘플 확인 페이지"""
import base64, pathlib, subprocess, re

H = pathlib.Path(__file__).resolve().parent
SFX = H.parent / "sound" / "sfx_n"
SRC = (H / "make_sample.py").read_text(encoding="utf-8")
KONG = eval(re.search(r"KONG = (\{.*?\n\})", SRC, re.S).group(1))
KIT = [("k_fast", "빠른 삐약 ①", "삐약삐약삐약삐약 — 신날 때"), ("k_fast2", "빠른 삐약 ②", "같은 병아리, 다른 4연속"),
       ("k_two", "짧은 삐약삐약", "2번 — 반응·놀람"), ("k_slow", "느린 삐약", "한 번, 길게 — 궁금할 때"),
       ("k_slow2", "느린 삐약 두 번", "(이번 샘플엔 안 씀)"), ("k_hop2", "콩콩", "폴짝 두 번"), ("k_hop3", "콩콩콩", "폴짝 세 번")]
NAME = {k: n for k, n, _ in KIT}
ACT = {"02": {"01": "구름 쪼기", "02": "하트 뿌리기", "03": "구름 빤히 보기", "04": "베개로 폴짝", "05": "저울 위 폴짝폴짝",
              "08": "부리에 빗방울", "11": "별 들고 폴짝", "12": "저울 옆 춤", "13": "마지막 장면"},
       "03": {"01": "케이크 체리 쪼기", "02": "신나서 앞장서기", "03": "식탁 건너 폴짝", "04": "치즈 보고 눈 반짝", "05": "식탁 위 춤",
              "06": "상자에서 튀어나옴", "09": "빵 받으러 폴짝", "10": "빵 오물오물", "11": "마지막 장면"}}


def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def small(tag, ep):
    f = H / "out" / f"ep{ep}_{tag}.mp4"; s = H / "out_s" / f.name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "31",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(s)], check=True)
    return s


kit = ""
for k, n, d in KIT:
    m = H / "out_s" / f"{k}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SFX / f"{k}.wav"), "-b:a", "128k", str(m)], check=True)
    kit += f'<div class="snd"><div class="lab"><b>{n}</b> <span class="soft">{d}</span></div><audio controls preload="none" src="{b64(m, "audio/mpeg")}"></audio></div>'

secs = []
for ep, title in (("02", "2화 · 칭찬과 지적"), ("03", "3화 · 에피쿠로스")):
    rows = "".join(f"<tr><td>{cid}번 · {ACT[ep].get(cid, '')}</td><td>{NAME[n]}</td></tr>" for cid, n, _, _ in KONG[ep])
    cards = ""
    for tag, lab, desc in (("N_kong", "콩이 소리 ⭐", "빠른 삐약·느린 삐약·콩콩만"), ("L_115_K_loop", "소리 없음", "비교용")):
        best = " best" if tag.startswith("N_") else ""
        cards += (f'<div class="card{best}"><video controls loop playsinline preload="metadata" src="{b64(small(tag, ep), "video/mp4")}"></video>'
                  f'<div class="c"><div class="nm">{lab}</div><div class="soft">{desc}</div></div></div>')
    secs.append(f'<section><h2>{title}</h2><div class="grid">{cards}</div>'
                f'<table><tr><th>컷 · 콩이 동작</th><th>소리</th></tr>{rows}</table></section>')

html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 콩이 소리 샘플</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",system-ui,sans-serif;line-height:1.65;margin:0;padding:24px 12px 60px}}
.wrap{{max-width:860px;margin:0 auto;display:flex;flex-direction:column;gap:24px}}p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:6px}}
h1{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:clamp(23px,6vw,32px);line-height:1.3;margin:0 0 6px}}
h2{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:21px;margin:0 0 10px}}
.soft{{color:var(--soft);font-size:13px}}
.kit{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:12px 14px}}
.snd .lab{{font-size:14px}}.snd .lab b{{color:var(--honey)}}audio{{width:100%;height:36px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-bottom:10px}}
.card{{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}.card.best{{border:2px solid var(--honey)}}
.card video{{width:100%;aspect-ratio:9/16;background:#000;display:block}}.card .c{{padding:9px 11px 11px}}
.nm{{font-family:"Gowun Dodum",sans-serif;font-size:16px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}th,td{{border-bottom:1px solid var(--edge);padding:6px 5px;text-align:left}}th{{color:var(--soft);font-weight:500;font-size:12px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}}
.q b.t{{font-family:"Gowun Dodum",sans-serif;font-size:18px;font-weight:400;display:block;margin-bottom:4px}}
</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · 콩이 소리 샘플</p><h1>삐약이 소리에만 집중했어요</h1>
<p class="soft">다른 효과음(뽁·바람·빗소리 등)은 전부 뺐어요. 실제 병아리 녹음(Pixabay, 크레딧 0)에서 빠른 삐약·느린 삐약, 작은 발소리로 콩콩을 만들었어요.
콩이가 움직이는 컷에만, <b>대사가 끝난 직후 빈틈</b>에 넣어서 말소리와 겹치지 않게 했어요. 하나를 틀면 다른 소리는 멈춰요.</p></section>
<section><h2>① 소리만 먼저 들어 보기</h2><div class="kit">{kit}</div></section>
{"".join(secs)}
<section class="q"><b class="t">알려 주세요</b>① 삐약 소리 자체: 좋다 / 다른 병아리로<br>② 콩콩: 좋다 / 더 작게·가볍게 / 빼기<br>③ 크기·횟수: 적당 / 더 크게·작게 / 더 자주·덜 자주<br>예) "빠른 삐약 좋고 콩콩은 더 작게" — 정하면 2~6화 전부 같은 규칙으로 다시 조립할게요(크레딧 0).</section>
</div>
<script>document.querySelectorAll('video,audio').forEach(m=>m.addEventListener('play',()=>{{document.querySelectorAll('video,audio').forEach(o=>{{if(o!==m)o.pause()}})}}));</script>
</body></html>"""
p = H / "gomgom_kong_peep_v1.html"
p.write_text(html, encoding="utf-8")
print(p, round(p.stat().st_size / 1048576, 1), "MB")
