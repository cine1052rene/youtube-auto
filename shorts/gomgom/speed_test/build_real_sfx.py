# -*- coding: utf-8 -*-
"""고른 실제 녹음 효과음 8개를 넣은 2·3화 샘플 확인 페이지 (효과음 있음/없음 + 들어간 위치 표)"""
import base64, json, pathlib, subprocess, re

H = pathlib.Path(__file__).resolve().parent
SRC = (H / "make_sample.py").read_text(encoding="utf-8")
NAME = {"r_footsteps": "발걸음", "r_door": "문 여는 소리", "r_rain": "빗소리", "r_teacup": "찻잔",
        "r_wind": "바람", "r_page": "책장 넘김", "r_sparkle": "반짝임", "r_pop": "뽁"}
REAL = eval(re.search(r"REAL = (\{.*?\n\})", SRC, re.S).group(1))


def b64(p):
    return "data:video/mp4;base64," + base64.b64encode(p.read_bytes()).decode()


def small(tag, ep):
    f = H / "out" / f"ep{ep}_{tag}.mp4"; s = H / "out_s" / f.name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "31",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(s)], check=True)
    return s


secs = []
for ep, title in (("02", "2화 · 칭찬과 지적"), ("03", "3화 · 에피쿠로스")):
    starts = {}  # make_sample과 같은 규칙으로 컷 시작 시각 계산 대신, 미리 저장된 json 없이 표는 컷 번호로 표시
    rows = "".join(f"<tr><td>{cid}번 컷</td><td>{NAME[n]}</td><td>컷 시작 +{off:g}초</td></tr>" for cid, n, off, _ in REAL[ep])
    cards = ""
    for tag, lab, desc in (("M_K_loop_real", "효과음 있음 ⭐", "고른 실제 녹음 8개 중 장면에 맞는 것만"),
                           ("L_115_K_loop", "효과음 없음", "비교용 (지난번 루프 버전)")):
        best = " best" if tag.startswith("M_") else ""
        cards += (f'<div class="card{best}"><video controls loop playsinline preload="metadata" src="{b64(small(tag, ep))}"></video>'
                  f'<div class="c"><div class="nm">{lab}</div><div class="soft">{desc}</div></div></div>')
    secs.append(f'<section><h2>{title}</h2><div class="grid">{cards}</div>'
                f'<table><tr><th>어디에</th><th>무슨 소리</th><th>언제</th></tr>{rows}</table></section>')

html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 실제 효과음 넣은 샘플</title>
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
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-bottom:10px}}
.card{{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}.card.best{{border:2px solid var(--honey)}}
.card video{{width:100%;aspect-ratio:9/16;background:#000;display:block}}.card .c{{padding:9px 11px 11px}}
.nm{{font-family:"Gowun Dodum",sans-serif;font-size:16px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}th,td{{border-bottom:1px solid var(--edge);padding:6px 5px;text-align:left}}th{{color:var(--soft);font-weight:500;font-size:12px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}}
.q b.t{{font-family:"Gowun Dodum",sans-serif;font-size:18px;font-weight:400;display:block;margin-bottom:4px}}
</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · 실제 효과음 넣은 샘플</p><h1>고르신 효과음 8개를 넣어 봤어요</h1>
<p class="soft">발걸음1 · 문 여는 소리2 · 빗소리1 · 찻잔1 · 바람3 · 책장2 · 반짝임3 · 뽁1 — 장면에 맞는 자리에만 넣었어요. 공통: 1.15배 · 간격 K · 제목 카드 3초 · 루프 처리(끝나면 자동으로 처음부터). 하나를 틀면 다른 영상은 멈춰요.</p></section>
{"".join(secs)}
<section class="q"><b class="t">알려 주세요</b>① 효과음 크기: 적당 / 더 크게 / 더 작게<br>② 빼고 싶은 소리나 위치: 예) "2화 빗소리 빼", "찻잔 더 크게"<br>정해지면 같은 규칙으로 2~6화 전부 다시 조립할게요(크레딧 0).</section>
</div>
<script>document.querySelectorAll('video').forEach(m=>m.addEventListener('play',()=>{{document.querySelectorAll('video').forEach(o=>{{if(o!==m)o.pause()}})}}));</script>
</body></html>"""
p = H / "gomgom_real_sfx_v1.html"
p.write_text(html, encoding="utf-8")
print(p, round(p.stat().st_size / 1048576, 1), "MB")
