# 시즌 3·4 대본 → epNN/lines.json + 인쇄용 HTML(scripts_s34.html) → PDF는 크롬 headless로
import json, os, html
from data import EPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.dirname(os.path.abspath(__file__))

for e in EPS:
    d = os.path.join(ROOT, f"ep{e['no']}")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "lines.json")
    if os.path.exists(p):
        continue  # 이미 손본 대본은 덮어쓰지 않음
    shots = []
    for i, (nar, img) in enumerate(e["shots"], 1):
        last = i == len(e["shots"])
        shots.append({"id": f"{i:02d}", "type": "V", "model": "seedance1_5:8" if last else "seedance1_5",
                      "narrator": nar, "plan_img": img, "plan_mov": "",
                      "plan_note": "훅" if i == 1 else ("질문 + 8초 여운" if last else "")})
    json.dump({"episode": f"{e['no']} {e['topic']}", "title": e["title"], "hook": e["hook"],
               "concept": e["concept"], "cast": e["cast"], "shots": shots,
               "voices": {"luna": {"engine": "higgsfield text2speech_v2 elevenlabs",
                                   "voice_id": "375a3398-e3b4-4f91-845d-42181e352899",
                                   "voice_type": "preset", "script": "narrator"}},
               "note": "근거: " + e["source"]}, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

h = html.escape
parts = []
season = None
for e in EPS:
    if e["season"] != season:
        season = e["season"]
        parts.append(f'<h1 class="season">{h(season)}</h1>')
    n = sum(len(s[0]) for s in e["shots"])
    rows = "".join(f'<tr><td class="no">{i:02d}</td><td class="nar">{h(s[0])}</td><td class="img">{h(s[1])}</td></tr>'
                   for i, s in enumerate(e["shots"], 1))
    parts.append(f'''<section class="ep">
<div class="eph"><span class="epno">{e["no"]}화</span> <span class="topic">{h(e["topic"])}</span></div>
<table class="meta">
<tr><th>유튜브 제목(안)</th><td>{h(e["title"])}</td></tr>
<tr><th>제목 카드</th><td>{h(" / ".join(e["hook"]))}</td></tr>
<tr><th>핵심 개념</th><td>{h(e["concept"])}</td></tr>
<tr><th>근거</th><td>{h(e["source"])}</td></tr>
<tr><th>조연</th><td>{h(e["cast"])}</td></tr>
<tr><th>분량</th><td>대사 {n}자(공백 포함) · 11장면 · 예상 약 40~43초</td></tr>
</table>
<table class="shots"><thead><tr><th>#</th><th>내레이션</th><th>장면</th></tr></thead><tbody>{rows}</tbody></table>
<div class="memo">메모:</div>
</section>''')

doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>곰곰한 마음 시즌 3·4 대본 (13~24화)</title>
<style>
@page {{ size: A4; margin: 14mm 13mm; }}
body {{ font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; color:#222; font-size:10.5pt; line-height:1.5; }}
.cover {{ text-align:center; padding-top:60mm; page-break-after:always; }}
.cover h1 {{ font-size:24pt; margin:0 0 6mm; }} .cover p {{ color:#555; }}
.cover ul {{ display:inline-block; text-align:left; margin-top:10mm; }}
h1.season {{ font-size:15pt; border-bottom:2px solid #c9a36b; padding-bottom:2mm; page-break-before:always; margin-top:0; }}
.ep {{ page-break-inside:avoid; page-break-after:always; }}
.eph {{ font-size:14pt; font-weight:bold; margin:2mm 0 3mm; }} .epno {{ color:#b07a2a; }}
table {{ width:100%; border-collapse:collapse; }}
.meta th {{ width:28mm; text-align:left; vertical-align:top; color:#7a5a2a; padding:1mm 2mm 1mm 0; font-weight:600; }}
.meta td {{ padding:1mm 0; }}
.shots {{ margin-top:4mm; }}
.shots th {{ background:#f3ead9; padding:1.5mm; text-align:left; border:1px solid #d8c7a5; }}
.shots td {{ border:1px solid #e2d6bd; padding:1.5mm; vertical-align:top; }}
.no {{ width:8mm; text-align:center; color:#888; }} .nar {{ width:52%; font-weight:600; }} .img {{ color:#555; font-size:9.5pt; }}
.memo {{ margin-top:5mm; border:1px dashed #bbb; height:22mm; padding:2mm; color:#999; }}
</style></head><body>
<div class="cover"><h1>곰곰한 마음<br>시즌 3·4 대본 초안</h1>
<p>13~24화 · 2026-11-06 작성 · 화마다 11장면, 40초 안팎</p>
<ul><li>시즌 3 — 천천히 가도 괜찮아 (동양의 지혜) : 13~18화</li>
<li>시즌 4 — 나한테도 친절하게 (관계와 나) : 19~24화</li>
<li>고정 댓글은 제작 단계에서 확정 (근거는 각 화 '근거' 칸)</li>
<li>장면 칸은 그림 생성 전 초안 — 그림 확인 후 고침</li></ul></div>
{"".join(parts)}
</body></html>'''
open(os.path.join(OUT, "scripts_s34.html"), "w", encoding="utf-8").write(doc)
print("ok")
