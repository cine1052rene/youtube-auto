# -*- coding: utf-8 -*-
import base64, pathlib
H = pathlib.Path(__file__).parent
R = H.parent
b = lambda p: base64.b64encode(p.read_bytes()).decode()
img = lambda n: b(H / f"{n}.jpg")
vid = b(R / "ref" / "veo_gate_test.mp4")
html = f'''<title>곰곰이 첫 테스트</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--ok:#5E8A4E;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;padding:0 18px;padding-block:40px 70px}}
.wrap{{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:42px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(30px,8vw,42px);line-height:1.25;margin:0 0 12px;text-wrap:balance}}
h2{{font-family:var(--round);font-size:24px;margin:0 0 8px}}
.soft{{color:var(--soft);font-size:15px}}
.checks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.check{{background:var(--card);border:1px solid var(--edge);border-radius:16px;padding:15px 17px}}
.check .t{{font-family:var(--round);font-size:18px;display:flex;gap:8px;align-items:center}}
.check .t::before{{content:"";width:10px;height:10px;border-radius:50%;background:var(--ok);flex-shrink:0}}
.check p{{font-size:14px;color:var(--soft);margin-top:4px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.tile{{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}
.tile img,.tile video{{width:100%;max-width:100%;height:auto;display:block;aspect-ratio:9/16;object-fit:cover;background:#EFE6D8}}
.tile .cap{{padding:10px 12px 13px;font-size:13.5px}}
.tile .cap b{{display:block;font-family:var(--round);font-size:15.5px;font-weight:400}}
.tile .cap span{{color:var(--soft)}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
@media (max-width:520px){{.grid3{{grid-template-columns:1fr 1fr}}}}
.notes{{background:var(--card);border:1px solid var(--edge);border-radius:16px;padding:16px 18px;display:flex;flex-direction:column;gap:9px;font-size:14.5px}}
.notes li{{color:var(--soft)}} .notes ul{{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}}
.next{{border-top:2px dashed var(--edge);padding-top:26px;display:flex;flex-direction:column;gap:10px}}
.bal{{font-variant-numeric:tabular-nums;font-size:13.5px;color:var(--soft)}}
</style>
<div class="wrap">
<section>
<p class="eye">곰곰한 마음 · 1화 준비</p>
<h1>곰곰이, 장면이 바뀌어도 그대로입니다</h1>
<p class="soft">본 작업에 크레딧을 크게 쓰기 전에 걸릴 수 있는 두 가지를 먼저 확인했습니다. 둘 다 통과했습니다.</p>
</section>

<section class="checks">
<div class="check"><div class="t">무료 플랜에서 영상 생성됨</div><p>4초 세로 영상 1개, 정확히 4크레딧 사용. 막혀 있을 가능성이 있었는데 괜찮았습니다.</p></div>
<div class="check"><div class="t">곰이 매번 같은 곰</div><p>기준 이미지를 참조로 물려 서로 다른 장면 3곳에서 뽑았더니 얼굴·색·콩이까지 동일했습니다.</p></div>
</section>

<section>
<h2>기준 곰곰이와 첫 영상</h2>
<p class="soft" style="margin-bottom:14px">왼쪽이 모든 장면의 기준이 되는 그림, 오른쪽이 그 그림을 그대로 움직인 4초 영상입니다.</p>
<div class="pair">
<div class="tile"><img src="data:image/jpeg;base64,{img('master')}" alt="곰곰이 기준 이미지"><div class="cap"><b>기준 곰곰이</b><span>이 그림을 모든 컷의 참조로 씁니다</span></div></div>
<div class="tile"><video src="data:video/mp4;base64,{vid}" autoplay loop muted playsinline controls></video><div class="cap"><b>첫 영상 · 4초</b><span>손 흔드는 동안 얼굴이 변하지 않음</span></div></div>
</div>
</section>

<section>
<h2>1화에 들어갈 실제 컷</h2>
<p class="soft" style="margin-bottom:14px">테스트용으로 따로 뽑지 않고 1화 컷을 바로 뽑았습니다. 그대로 씁니다.</p>
<div class="grid3">
<div class="tile"><img src="data:image/jpeg;base64,{img('v01_start')}" alt="소파에서 폰 보는 곰곰이"><div class="cap"><b>0:00 소파</b><span>쉬는 날인데 피곤한 얼굴</span></div></div>
<div class="tile"><img src="data:image/jpeg;base64,{img('s08')}" alt="화분에 물 주는 곰곰이"><div class="cap"><b>0:20 화분</b><span>작은 것에 푹 빠지기</span></div></div>
<div class="tile"><img src="data:image/jpeg;base64,{img('v12_start')}" alt="창가에서 코코아 든 곰곰이"><div class="cap"><b>0:32 창가</b><span>좋아하는 걸 골라 하기</span></div></div>
</div>
</section>

<section class="notes">
<b>작은 것들</b>
<ul>
<li>영상 뒤쪽에서 반짝이가 너무 많아집니다. 다음 영상부터 반짝이를 줄이라고 지시합니다.</li>
<li>콩이가 어깨 대신 볼 옆에 떠 있는데, 세 장 모두 같은 자리라 그대로 둡니다.</li>
<li>Veo Lite 영상은 720p가 최대입니다. 편집할 때 1080p로 키웁니다.</li>
</ul>
</section>

<section class="next">
<h2>지금 진행 중</h2>
<p class="soft">1화의 나머지 그림 10장과 영상 5개를 뽑고 있습니다. 약 30크레딧, 20~30분 걸립니다. 끝나면 1화를 편집해서 보여드리고, 보신 뒤에 2~6화로 넘어갑니다.</p>
<p class="bal">사용 13.52 · 잔액 286.48</p>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("board ok", round(len(html)/1024), "KB")
