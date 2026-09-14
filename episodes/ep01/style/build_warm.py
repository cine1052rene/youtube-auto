# -*- coding: utf-8 -*-
import base64, pathlib
H = pathlib.Path(__file__).parent
b = lambda n: base64.b64encode((H / n).read_bytes()).decode()
html = f'''<title>곰곰한 마음</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--blush:#E39A8B;--leaf:#6F8F5C;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--blush:#EBAB9E;--leaf:#9BB887}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--blush:#EBAB9E;--leaf:#9BB887}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.78;padding:0 20px;padding-block:44px 72px}}
.wrap{{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:46px}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(30px,8vw,44px);line-height:1.25;margin:0 0 14px;text-wrap:balance}}
h2{{font-family:var(--round);font-size:25px;margin:0 0 8px}}
p{{margin:0}}
.soft{{color:var(--soft);font-size:15px}}
.panel{{background:var(--card);border:1px solid var(--edge);border-radius:18px;padding:18px 20px;display:flex;flex-direction:column;gap:10px}}
.panel b{{color:var(--ink)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}}
.stat{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px}}
.stat .v{{font-family:var(--round);font-size:24px;font-variant-numeric:tabular-nums}}
.stat .l{{font-size:12.5px;color:var(--soft)}}
.pics{{display:flex;flex-direction:column;gap:26px}}
figure{{margin:0;background:var(--card);border:1px solid var(--edge);border-radius:18px;overflow:hidden}}
figure img{{width:100%;max-width:100%;height:auto;display:block}}
figcaption{{padding:16px 18px 19px;display:flex;flex-direction:column;gap:7px}}
.top{{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}}
.top strong{{font-family:var(--round);font-size:21px}}
.cost{{font-size:13px;font-weight:700;color:var(--honey)}}
figcaption p{{font-size:14.5px;color:var(--soft)}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums}}
td{{padding:9px 4px;border-bottom:1px solid var(--edge)}}
td:last-child{{text-align:right;font-weight:700}}
tr.sum td{{border-bottom:none;color:var(--honey)}}
.tw{{overflow-x:auto}}
.eps{{display:flex;flex-direction:column;gap:10px}}
.ep{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 16px;font-size:15px}}
.ep span{{display:block;font-size:12.5px;color:var(--soft)}}
.ask{{border-top:2px dashed var(--edge);padding-top:28px;display:flex;flex-direction:column;gap:12px}}
.q{{background:var(--card);border-radius:14px;border:1px solid var(--edge);padding:14px 16px;font-size:15px}}
.q b{{font-family:var(--round);font-size:17px;display:block;margin-bottom:3px}}
</style>
<div class="wrap">
<section>
<p class="eye">방향 재설정 · 따뜻하고 귀엽게</p>
<h1>계속 무너졌던 이유는 모델이었습니다</h1>
<div class="panel">
<p>지금까지 쓴 <b>Soul 2.0은 실사에 특화된 모델</b>입니다. 애니메·클레이·일러스트를 시킬 때마다 얼굴에만 스타일이 먹고 배경은 실사로 남았던 게 그래서입니다.</p>
<p>이번엔 <b>귀여운 그림체에 강한 모델</b>로 바꿨더니, 화면 전체가 한 그림체로 통일되고 깨진 글자도 사라졌습니다.</p>
</div>
</section>

<section>
<h2>크레딧 재조사</h2>
<div class="stats">
<div class="stat"><div class="v">294.48</div><div class="l">현재 잔액</div></div>
<div class="stat"><div class="v">0</div><div class="l">만료·회수 변동 (9/10 이후)</div></div>
<div class="stat"><div class="v">5.52</div><div class="l">이번 테스트 누적 사용</div></div>
</div>
<p class="soft" style="margin-top:12px">GPT Image 2.5와 Recraft는 <b>무료 플랜에서 막혀 있어</b> 생성이 거부됐고, 크레딧은 빠지지 않았습니다.</p>
</section>

<section>
<h2>같은 장면, 두 모델</h2>
<p class="soft" style="margin-bottom:18px">창가에서 담요를 두르고 코코아를 든 곰, 어깨 위의 작은 새.</p>
<div class="pics">
<figure><img src="data:image/jpeg;base64,{b('w_a.jpg')}" alt="Nano Banana Pro 결과">
<figcaption><div class="top"><strong>A · 맑고 또렷한 3D</strong><span class="cost">장당 2크레딧</span></div>
<p>눈웃음 짓는 곰, 선명한 디테일, 아늑한 방 전체가 보입니다. <b>캐릭터 상품 같은 완성도.</b> 표정이 확실해서 감정 전달이 쉽습니다.</p></figcaption></figure>
<figure><img src="data:image/jpeg;base64,{b('w_b.jpg')}" alt="Seedream 5.0 Lite 결과">
<figcaption><div class="top"><strong>B · 몽글몽글한 펠트</strong><span class="cost">장당 1크레딧</span></div>
<p>털실 질감과 반짝이는 빛망울, 더 몽환적입니다. <b>위로하는 분위기는 이쪽이 더 강합니다.</b> 다만 곰 표정이 살짝 졸리거나 새침해 보입니다.</p></figcaption></figure>
</div>
</section>

<section>
<h2>예산을 다시 짜야 합니다</h2>
<p class="soft" style="margin-bottom:14px">그림 한 장이 0.12에서 1~2크레딧으로 올랐으니, 스틸 350장 계획은 불가능합니다. 대신 <b>좋은 그림을 적게 뽑고, 핵심 장면은 그 그림을 그대로 움직여</b> 그림체를 유지합니다.</p>
<div class="tw"><table>
<tr><td>스틸 90장 (B 기준 1크레딧)</td><td>90</td></tr>
<tr><td>그림을 움직이는 영상 20컷 (Veo 3.1 Lite, 8크레딧)</td><td>160</td></tr>
<tr><td>예비 · 캐릭터 일관성 테스트</td><td>44</td></tr>
<tr class="sum"><td>합계</td><td>294</td></tr>
</table></div>
<p class="soft" style="margin-top:12px">A로 가면 스틸이 45장으로 줄어듭니다. 8~9분 롱폼을 채우기엔 B가 현실적입니다.</p>
</section>

<section>
<h2>콘텐츠 방향: 「곰곰한 마음」</h2>
<p class="soft" style="margin-bottom:14px">곰 캐릭터가 마음에 대해 <b>곰곰이</b> 생각하는 따뜻한 심리·철학 채널. 해외에선 귀여운 그림체로 심리학을 풀어내는 Psych2Go가 구독자 1,300만 명입니다. 한국어로는 검색 한 번으로 딱 맞는 채널이 안 잡혔지만, 그것만으로 빈자리라고 단정하긴 이릅니다.</p>
<div class="eps">
<div class="ep">쉬어도 쉬어도 피곤한 이유<span>심리학 · 번아웃과 회복</span></div>
<div class="ep">별일 아닌데 괜히 서운할 때<span>심리학 · 기대와 감정</span></div>
<div class="ep">에피쿠로스가 말한 작은 행복<span>철학 · 소박한 즐거움</span></div>
</div>
</section>

<section class="ask">
<div class="q"><b>1. A와 B, 어느 쪽 그림이 좋으세요?</b>A는 또렷하고 표정이 확실하고, B는 더 포근하지만 스틸 수가 두 배입니다.</div>
<div class="q"><b>2. 곰 캐릭터와 「곰곰한 마음」 방향, 괜찮으세요?</b>다른 동물이나 사람 캐릭터가 좋으시면 말씀해주세요.</div>
<p class="soft">고르시면 다음 테스트는 <b>같은 곰이 서로 다른 장면 3곳에서 똑같이 나오는지</b>입니다. 시리즈의 성패는 여기서 갈립니다.</p>
</section>
</div>'''
(H / "style_board.html").write_text(html, encoding="utf-8")
print("ok")
