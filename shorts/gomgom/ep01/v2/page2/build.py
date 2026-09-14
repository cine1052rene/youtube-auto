# -*- coding: utf-8 -*-
import base64, pathlib
H = pathlib.Path(__file__).parent
b = lambda n: base64.b64encode((H / n).read_bytes()).decode()
def card(f, name, price, verdict, cls, note):
    return f'''<figure class="c {cls}"><video src="data:video/mp4;base64,{b(f)}" autoplay loop muted playsinline controls></video>
<figcaption><div class="top"><b>{name}</b><span class="tag">{verdict}</span></div><span class="price">{price}</span><p>{note}</p></figcaption></figure>'''
html = f'''<title>곰곰이 영상 모델 비교</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--ok:#5E8A4E;--no:#B5543C;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--no:#E08A70}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--no:#E08A70}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72;padding:0 16px;padding-block:38px 70px}}
.wrap{{max-width:960px;margin:0 auto;display:flex;flex-direction:column;gap:34px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(28px,7vw,40px);line-height:1.28;margin:0 0 10px;text-wrap:balance}}
h2{{font-family:var(--round);font-size:23px;margin:0 0 8px;font-weight:400}}
.soft{{color:var(--soft);font-size:15px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
@media (max-width:700px){{.grid{{grid-template-columns:1fr}}}}
.c{{margin:0;background:var(--card);border:1px solid var(--edge);border-radius:18px;overflow:hidden}}
.c.ok{{border:2px solid var(--ok)}}
.c video{{width:100%;max-width:100%;aspect-ratio:9/16;display:block;background:#000}}
.c figcaption{{padding:12px 14px 15px;display:flex;flex-direction:column;gap:4px}}
.top{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
.top b{{font-family:var(--round);font-size:19px;font-weight:400}}
.tag{{font-size:12px;font-weight:700;padding:2px 9px;border-radius:9px;color:#fff;white-space:nowrap}}
.ok .tag{{background:var(--ok)}} .no .tag{{background:var(--no)}}
.price{{font-size:13px;color:var(--honey);font-weight:700;font-variant-numeric:tabular-nums}}
.c p{{font-size:14px;color:var(--soft)}}
.note{{background:var(--card);border:1px dashed var(--edge);border-radius:16px;padding:14px 16px;font-size:14.5px}}
.note ul{{margin:6px 0 0;padding-left:18px;display:flex;flex-direction:column;gap:5px;color:var(--soft)}}
.tw{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums;min-width:560px}}
th,td{{padding:10px 8px;border-bottom:1px solid var(--edge);text-align:left;vertical-align:top}}
th{{font-size:12.5px;color:var(--soft);font-weight:500}}
td.n{{text-align:right;white-space:nowrap}}
tr.rec td{{background:color-mix(in srgb,var(--honey) 10%,transparent)}}
.ask{{border-top:2px dashed var(--edge);padding-top:22px;display:flex;flex-direction:column;gap:10px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px;font-size:15px}}
.q b{{font-family:var(--round);font-size:17px;font-weight:400;display:block;margin-bottom:2px}}
</style>
<div class="wrap">
<section>
<p class="eye">곰곰한 마음 · 영상 모델 비교</p>
<h1>카메라가 움직이는 모델을 찾았습니다</h1>
<p class="soft">같은 소파 장면, 같은 시작 그림, 같은 지시로 세 모델을 비교했습니다. 이번 비교에 12.3크레딧을 썼고 남은 크레딧은 215입니다.</p>
</section>

<section class="grid">
{card("t01.mp4", "Veo 3.1 Lite", "4초 · 4크레딧", "카메라 고정", "no", "지금까지 쓰던 모델. 곰곰이 표정만 바뀌고 구도는 그대로입니다.")}
{card("t01_seedance15.mp4", "Seedance 1.5 Pro", "4초 · 4.8크레딧", "움직임", "ok", "위에서 부드럽게 내려오며 곰곰이 쪽으로 다가갑니다. 은은하고 안정적입니다.")}
{card("t01_wan27.mp4", "Wan 2.7", "5초 · 7.5크레딧", "크게 움직임", "ok", "곰곰이 얼굴 가까이까지 과감하게 다가갑니다. 영화 같은 느낌이 가장 강합니다.")}
</section>

<section class="note"><b>확인한 것</b>
<ul>
<li>Seedance 1.5와 Wan 2.7 모두 곰곰이 모습이 흐트러지지 않았고, 화면에 이상한 물체도 없었습니다.</li>
<li>Kling 3.0, Kling 3.0 Turbo, Seedance 2.0 Mini는 무료 플랜에서 막혀 있었습니다. 막힌 시도에는 크레딧이 빠지지 않았습니다.</li>
<li>Seedance 1.5는 영상 길이를 4·8·12초 중에서만 고를 수 있습니다. 대사가 4초보다 긴 컷은 조금 느리게 틀거나 8초로 만듭니다.</li>
</ul></section>

<section>
<h2>모델별로 몇 편이 나오나</h2>
<p class="soft" style="margin-bottom:10px">남은 크레딧 215 기준, 한 편 13컷 전부 영상, 다시 뽑기 30% 포함. 이미 만든 시점 테스트 그림 3장은 1화에 재사용합니다.</p>
<div class="tw"><table>
<tr><th>구성</th><th>카메라 느낌</th><th class="n">한 편 비용</th><th>편수</th></tr>
<tr class="rec"><td><b>Seedance 1.5 전부</b></td><td>은은하게 움직임</td><td class="n">약 98</td><td>2편</td></tr>
<tr><td><b>Seedance 1.5 + 중요한 3컷만 Wan 2.7</b></td><td>평소엔 은은, 첫 장면·전환·마지막만 과감</td><td class="n">약 108</td><td>2편</td></tr>
<tr><td><b>Wan 2.7 전부</b></td><td>매 컷 과감하게 움직임</td><td class="n">약 144</td><td>1편</td></tr>
</table></div>
</section>

<section class="ask">
<div class="q"><b>1. 어느 구성으로 갈까요?</b>“Seedance”, “섞기”, “Wan” 중 하나. 섞기는 첫 장면처럼 시선을 잡아야 하는 컷에만 Wan을 씁니다.</div>
<div class="q"><b>2. 목소리는 Luna로 확정했습니다</b>정해주시면 1화 13컷을 새 시점·새 배경으로 다시 만들고, Luna 내레이션을 입혀 보여드립니다.</div>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024), "KB")
