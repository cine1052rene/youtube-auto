# -*- coding: utf-8 -*-
import base64, pathlib
H = pathlib.Path(__file__).parent
b = lambda n: base64.b64encode((H / n).read_bytes()).decode()
def vid(n, cap, tag, cls):
    return f'''<figure class="c {cls}"><video src="data:video/mp4;base64,{b(n + ".mp4")}" autoplay loop muted playsinline controls></video>
<figcaption><span class="tag">{tag}</span>{cap}</figcaption></figure>'''
html = f'''<title>곰곰이 카메라 무빙 테스트</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--ok:#5E8A4E;--no:#B5543C;--mid:#B7862A;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--no:#E08A70;--mid:#E0B45A}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--no:#E08A70;--mid:#E0B45A}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72;padding:0 16px;padding-block:38px 70px}}
.wrap{{max-width:960px;margin:0 auto;display:flex;flex-direction:column;gap:36px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(28px,7vw,40px);line-height:1.28;margin:0 0 10px;text-wrap:balance}}
h2{{font-family:var(--round);font-size:23px;margin:0 0 8px;font-weight:400}}
.soft{{color:var(--soft);font-size:15px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.grid.two{{grid-template-columns:repeat(2,1fr)}}
@media (max-width:700px){{.grid,.grid.two{{grid-template-columns:1fr 1fr}}}}
.c{{margin:0;background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}
.c video{{width:100%;max-width:100%;aspect-ratio:9/16;display:block;background:#000}}
.c figcaption{{padding:10px 12px 12px;font-size:13.5px;color:var(--soft);display:flex;flex-direction:column;gap:4px}}
.tag{{align-self:flex-start;font-size:12px;font-weight:700;padding:1px 8px;border-radius:8px;color:#fff}}
.ok .tag{{background:var(--ok)}} .no .tag{{background:var(--no)}} .mid .tag{{background:var(--mid)}}
.ok{{border-color:var(--ok)}}
.strip{{background:var(--card);border:1px solid var(--edge);border-radius:16px;padding:12px;display:flex;flex-direction:column;gap:8px}}
.strip img{{width:100%;max-width:100%;height:auto;border-radius:8px}}
.strip p{{font-size:14px;color:var(--soft)}}
.facts{{background:var(--card);border:1px dashed var(--edge);border-radius:16px;padding:14px 16px}}
.facts ul{{margin:6px 0 0;padding-left:18px;display:flex;flex-direction:column;gap:5px;font-size:14.5px}}
.tw{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums;min-width:560px}}
th,td{{padding:10px 8px;border-bottom:1px solid var(--edge);text-align:left;vertical-align:top}}
th{{font-size:12.5px;color:var(--soft);font-weight:500}}
td.n{{text-align:right;white-space:nowrap}}
td b{{font-family:var(--round);font-size:16px;font-weight:400}}
.opt{{display:flex;flex-direction:column;gap:10px}}
.o{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}}
.o.rec{{border:2px solid var(--honey)}}
.o b{{font-family:var(--round);font-size:18px;font-weight:400;display:block;margin-bottom:3px}}
.o span{{color:var(--soft)}}
.ask{{border-top:2px dashed var(--edge);padding-top:22px;display:flex;flex-direction:column;gap:10px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px;font-size:15px}}
.q b{{font-family:var(--round);font-size:17px;font-weight:400;display:block;margin-bottom:2px}}
</style>
<div class="wrap">
<section>
<p class="eye">곰곰한 마음 · 전부 영상 테스트</p>
<h1>배경은 풍부해졌고, 카메라는 아직 잘 안 움직입니다</h1>
<p class="soft">시점이 다른 그림 4장, 영상 5개를 만들어 봤습니다. 이번 테스트에 28크레딧을 썼고 남은 크레딧은 225입니다.</p>
</section>

<section>
<h2>카메라가 움직인 영상</h2>
<div class="grid two">
{vid("t11", "산책길 · 걷는 곰곰이를 옆에서 따라감. 앞쪽 벚꽃이 화면을 스쳐 지나감", "성공", "ok")}
{vid("t05_orbit_cut", "빛 구슬 · 정면에서 옆쪽 낮은 시점으로 돌아감. 끝 장면 그림을 따로 줘서 만든 것(8초 중 앞 4.8초만 사용)", "절반 성공", "mid")}
</div>
</section>

<section>
<h2>카메라가 거의 안 움직인 영상</h2>
<div class="grid">
{vid("t01", "소파 · 위에서 내려오며 다가가라고 했지만 구도가 그대로", "실패", "no")}
{vid("t05", "빛 구슬 · 둘레를 돌라고 했지만 구도가 그대로", "실패", "no")}
{vid("t01_push", "소파 · 카메라 지시를 강하게 쓰니 다가가긴 했지만 검은 막대가 지나감", "결함", "no")}
</div>
<div class="strip" style="margin-top:12px"><img src="data:image/jpeg;base64,{b("push_artifact.jpg")}" alt="검은 막대가 지나가는 구간 캡처">
<p>0.3초 간격 캡처. 프롬프트의 “crane(카메라 크레인)”을 촬영 장비를 그리라는 뜻으로 받아들인 것으로 보입니다.</p></div>
</section>

<section class="facts"><b>알게 된 것</b>
<ul>
<li>지금 쓰는 Veo 3.1 Lite는 시작 그림을 주면 <b>카메라를 거의 고정</b>합니다. 캐릭터가 걸어서 이동할 때만 따라갑니다.</li>
<li>끝 장면 그림을 따로 주면 시점이 바뀌지만, 8초로 고정되고 도중에 원래 시점으로 돌아올 수 있습니다.</li>
<li>그림은 성공입니다. 하이앵글, 로우앵글, 측면에서도 곰곰이 모습이 흐트러지지 않았고 배경이 풍부해졌습니다.</li>
</ul></section>

<section>
<h2>카메라를 더 잘 움직이는 모델</h2>
<p class="soft" style="margin-bottom:10px">세로 영상, 시작 그림 기준 실제 조회 가격입니다.</p>
<div class="tw"><table>
<tr><th>모델</th><th>한 컷</th><th>특징</th><th>한 편(10컷) 예상</th><th>남은 크레딧으로</th></tr>
<tr><td><b>Veo 3.1 Lite</b> (지금)</td><td class="n">4초 · 4</td><td>가장 쌈. 카메라 고정 경향</td><td class="n">약 65</td><td>3편</td></tr>
<tr><td><b>Kling 3.0 Turbo</b></td><td class="n">5초 · 7.5</td><td>빠르고 저렴한 편. 끝 장면 지정 불가</td><td class="n">약 110</td><td>2편</td></tr>
<tr><td><b>Kling 3.0</b></td><td class="n">5초 · 10</td><td>끝 장면 지정 가능</td><td class="n">약 140</td><td>1편</td></tr>
<tr><td><b>Seedance 2.0 Mini</b></td><td class="n">5초 · 12.5</td><td>곰곰이 참고 그림을 여러 장 넣을 수 있어 큰 카메라 무빙에도 모습 유지에 유리</td><td class="n">약 175</td><td>1편</td></tr>
</table></div>
<p class="soft" style="margin-top:8px">한 편 예상 = 그림 10장 + 영상 10개, 다시 뽑기 30% 포함. 이미 만든 3컷은 1화에 재사용합니다.</p>
</section>

<section>
<h2>갈 수 있는 길</h2>
<div class="opt">
<div class="o"><b>A. Veo Lite 유지, 시점은 컷마다 바꾸기</b><span>한 컷 안에서 카메라는 거의 고정이지만, 컷이 바뀔 때마다 위에서·아래에서·옆에서·가까이로 번갈아 잡습니다. 중요한 2~3컷만 끝 장면 그림으로 회전을 넣습니다. 3편 가능.</span></div>
<div class="o rec"><b>B. 더 좋은 모델로 같은 컷을 먼저 비교</b><span>소파 장면 하나를 Kling 3.0 Turbo(7.5)와 Seedance 2.0 Mini(12.5)로 만들어 Veo와 나란히 비교합니다. 약 20크레딧. 결과를 보고 편수와 모델을 정합니다.</span></div>
</div>
</section>

<section class="ask">
<div class="q"><b>1. A와 B 중 어느 쪽으로 갈까요?</b></div>
<div class="q"><b>2. 목소리는요?</b>“곰곰이(bear_p4)”, “Luna”, “Luna로 반말” 중 하나. 아직 정하지 않으셔도 화면 작업은 계속할 수 있습니다.</div>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024), "KB")
