# -*- coding: utf-8 -*-
import base64, json, pathlib
H = pathlib.Path(__file__).parent
OUT = H.parent / "out"
v64 = lambda n: base64.b64encode((OUT / f"ep01_{n}_preview.mp4").read_bytes()).decode()
tl = {v: json.load(open(OUT / f"timeline_{v}.json", encoding="utf-8")) for v in ("luna", "bear")}
def lines(v):
    return "".join(f'<li><span class="t">{s["start"]:.1f}s</span>{s["text"]}</li>' for s in tl[v]["shots"])
html = f'''<title>곰곰한 마음 1화 목소리 비교</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--rose:#C9707A;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--rose:#E39AA2}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--rose:#E39AA2}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72;padding:0 16px;padding-block:38px 70px}}
.wrap{{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:34px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(28px,7vw,40px);line-height:1.28;margin:0 0 10px;text-wrap:balance}}
.soft{{color:var(--soft);font-size:15px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media (max-width:620px){{.pair{{grid-template-columns:1fr}}}}
.col{{background:var(--card);border:1px solid var(--edge);border-radius:20px;overflow:hidden;display:flex;flex-direction:column}}
.col.b{{border-color:var(--rose)}} .col.a{{border-color:var(--honey)}}
video{{width:100%;max-width:100%;aspect-ratio:9/16;display:block;background:#000}}
.meta{{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px}}
.meta h2{{font-family:var(--round);font-size:21px;margin:0;font-weight:400}}
.chip{{display:inline-block;font-size:12px;font-weight:700;padding:2px 9px;border-radius:9px;color:#2A2118;margin-right:6px}}
.a .chip{{background:var(--honey)}} .b .chip{{background:var(--rose)}}
.meta p{{font-size:14px;color:var(--soft)}}
details{{padding:0 16px 14px}}
summary{{cursor:pointer;font-size:14px;color:var(--soft)}}
ol{{margin:8px 0 0;padding-left:0;list-style:none;display:flex;flex-direction:column;gap:3px;font-size:14px}}
.t{{display:inline-block;width:44px;color:var(--soft);font-variant-numeric:tabular-nums}}
.notes{{background:var(--card);border:1px dashed var(--edge);border-radius:16px;padding:14px 16px;font-size:14.5px;color:var(--soft)}}
.notes ul{{margin:6px 0 0;padding-left:18px;display:flex;flex-direction:column;gap:4px}}
.ask{{border-top:2px dashed var(--edge);padding-top:22px;display:flex;flex-direction:column;gap:10px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px;font-size:15px}}
.q b{{font-family:var(--round);font-size:17px;font-weight:400;display:block;margin-bottom:2px}}
</style>
<div class="wrap">
<section>
<p class="eye">곰곰한 마음 · 1화 목소리 비교</p>
<h1>같은 영상, 두 목소리</h1>
<p class="soft">고르신 두 목소리로 1화를 끝까지 입혀봤습니다. 소리를 켜고 하나씩 재생해보세요.</p>
</section>

<section class="pair">
<div class="col b">
<video src="data:video/mp4;base64,{v64('bear')}" controls playsinline preload="metadata"></video>
<div class="meta"><h2><span class="chip">bear_p4</span>곰곰이가 직접</h2>
<p>곰곰이가 반말로 말합니다. 무료 목소리의 음높이를 올렸습니다. {tl['bear']['total']:.1f}초</p></div>
<details><summary>대사 보기</summary><ol>{lines('bear')}</ol></details>
</div>
<div class="col a">
<video src="data:video/mp4;base64,{v64('luna')}" controls playsinline preload="metadata"></video>
<div class="meta"><h2><span class="chip">Luna</span>해설자가 들려주기</h2>
<p>ElevenLabs 목소리로 존댓말 해설. 1화 전체 약 2크레딧. {tl['luna']['total']:.1f}초</p></div>
<details><summary>대사 보기</summary><ol>{lines('luna')}</ol></details>
</div>
</section>

<section class="notes"><b>비교용이라 빠진 것</b>
<ul>
<li>자막과 배경음악은 아직 없습니다. 목소리가 정해지면 넣습니다.</li>
<li>화질은 페이지용으로 줄였습니다. 원본은 1080×1920입니다.</li>
<li>대사가 영상보다 긴 컷(첫 장면, 콩이가 날아오는 장면)은 영상을 조금 느리게 틀었습니다.</li>
</ul></section>

<section class="ask">
<div class="q"><b>어느 쪽으로 갈까요?</b>“곰곰이”, “Luna” 중 하나로 답해주세요.</div>
<div class="q"><b>섞는 방법도 있습니다</b>Luna 목소리로 곰곰이 반말 대본을 읽히면, 음높이를 억지로 올리지 않은 자연스러운 귀여운 목소리가 됩니다. 약 2크레딧이면 한 번 더 만들어 비교해드립니다.</div>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html) / 1024), "KB")
