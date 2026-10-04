# -*- coding: utf-8 -*-
"""2·3화 말 속도·훅·효과음·음악 비교 페이지 (화별 1개 html, 영상 내장)"""
import base64, json, pathlib, subprocess

H = pathlib.Path(__file__).resolve().parent
OUT = H / "out"
EP = {"02": "칭찬 열 번보다 지적 한 번이 더 오래 남는 이유", "03": "에피쿠로스가 말한 작은 행복"}
VER = [
    ("A_orig", "A · 지금 버전", "원래 속도 · 훅 없음 · 지금 배경음악"),
    ("B_115", "B · 1.15배", "훅 + 컷 사이 빈 시간 줄임 · 지금 배경음악"),
    ("C_125", "C · 1.25배 ⭐", "훅 + 빈 시간 줄임 · 지금 배경음악"),
    ("D_135", "D · 1.35배", "훅 + 빈 시간 줄임 · 지금 배경음악"),
    ("E_125_sfx", "E · 1.25배 + 효과음", "C에 작은 효과음 추가 · 지금 배경음악"),
    ("F_125_sfx_bgmA", "F · 1.25배 + 효과음 + 새 음악 A", "우쿨렐레·글로켄슈필, 조금 경쾌"),
    ("G_125_sfx_bgmB", "G · 1.25배 + 효과음 + 새 음악 B", "오르골·피아노, 차분하지만 흐름 있음"),
]
CSS = """:root{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B}
@media (prefers-color-scheme:dark){:root{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}
*{box-sizing:border-box}body{background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",system-ui,sans-serif;line-height:1.7;margin:0;padding:30px 14px 60px}
.wrap{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:26px}p{margin:0}
.eye{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:8px}
h1{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:clamp(24px,6vw,34px);line-height:1.3;margin:0 0 8px}
h2{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:20px;margin:0 0 8px}
.soft{color:var(--soft);font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}
.v{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}
.v.best{border:2px solid var(--honey)}
.v video{width:100%;aspect-ratio:9/16;background:#000;display:block}
.v .c{padding:9px 11px 11px;font-size:13px}.v .t{font-family:"Gowun Dodum",sans-serif;font-size:16px}
.v .len{color:var(--honey);font-weight:700;font-variant-numeric:tabular-nums}
table{width:100%;border-collapse:collapse;font-size:13.5px}th,td{border-bottom:1px solid var(--edge);padding:7px 6px;text-align:left}
th{color:var(--soft);font-weight:500;font-size:12px}
.q{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:15px}
.q b{font-family:"Gowun Dodum",sans-serif;font-size:18px;font-weight:400;display:block;margin-bottom:4px}"""


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


for ep, title in EP.items():
    cards = []
    for tag, name, desc in VER:
        f = OUT / f"ep{ep}_{tag}.mp4"
        if not f.exists():
            continue
        b = base64.b64encode(f.read_bytes()).decode()
        cards.append(f'<div class="v{" best" if tag == "C_125" else ""}"><video src="data:video/mp4;base64,{b}" controls playsinline preload="metadata"></video>'
                     f'<div class="c"><div class="t">{name}</div><div class="len">{dur(f):.1f}초</div><div class="soft">{desc}</div></div></div>')
    html = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{int(ep)}화 말 속도 비교</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · {int(ep)}화 비교 샘플</p><h1>{title}</h1>
<p class="soft">같은 영상·같은 목소리로 <b>말 속도, 첫 장면 훅, 효과음, 배경음악</b>만 바꿨어요. 소리를 켜고 A부터 차례로 들어 보세요. 미리보기 화질이에요.</p></section>
<section><h2>바뀐 것</h2><table>
<tr><th>항목</th><th>지금(A)</th><th>샘플(B~G)</th></tr>
<tr><td>말 속도</td><td>1배 (1초에 약 5글자)</td><td>1.15 / 1.25 / 1.35배, 목소리 높낮이는 그대로</td></tr>
<tr><td>컷 사이 빈 시간</td><td>대사 앞 0.15초 + 뒤 0.3초</td><td>앞 0.05초 + 뒤 0.15초, 첫 목소리는 0초부터</td></tr>
<tr><td>첫 장면 훅</td><td>없음</td><td>0~1.8초 화면 위쪽에 큰 제목 카드</td></tr>
<tr><td>효과음 (E~G)</td><td>없음</td><td>반짝·폴짝·날갯짓·딸랑 등 작은 소리를 장면에 맞춰 살짝</td></tr>
</table></section>
<section><div class="grid">{"".join(cards)}</div></section>
<section class="q"><b>골라 주세요</b>① 말 속도: B / C / D 중 어느 쪽이 좋은지<br>② 효과음: 넣기(E) / 빼기(C)<br>③ 배경음악: 지금 것(E) / 새 음악 A(F) / 새 음악 B(G)<br>예) "C, 효과음 넣고, 음악 A" — 고른 조합으로 2~6화를 다시 조립할게요(크레딧 0).</section>
</div></body></html>'''
    p = H / f"gomgom_ep{ep}_speed_compare.html"
    p.write_text(html, encoding="utf-8")
    print(p.name, round(p.stat().st_size / 1048576, 1), "MB")
