# -*- coding: utf-8 -*-
import base64, json, pathlib
OUT = pathlib.Path(__file__).parent.parent
H = pathlib.Path(__file__).parent
vid = base64.b64encode((OUT / "ep03_preview.mp4").read_bytes()).decode()
tl = json.load(open(OUT / "timeline.json", encoding="utf-8"))

CUTS = [
 ("01","훅 · 화려한 연회장","Wan 2.7 (5초)","케이크 사이로 다가감","케이크 꼭대기에서 체리를 쪼아 먹음"),
 ("02","부엉이 할아버지","Seedance 1.5","돌길 따라 이동","앞장서서 폴짝폴짝"),
 ("03","빵과 물, 친구","Seedance 1.5 (그림 재생성)","옆으로 슬라이드","테이블 위 빵 부스러기로 콩콩"),
 ("04","작은 치즈 단지","Seedance 1.5 (그림 재생성)","가까이 다가감","단지 가장자리에 앉아 안을 들여다봄"),
 ("05","소박한 잔치","Seedance 1.5 (그림 재생성)","천천히 회전","건배하는 옆에서 춤"),
 ("06","왕관 내려놓기","Seedance 1.5","뒤로 물러남","선물 상자에서 튀어나옴"),
 ("07","고요한 호수","Seedance 1.5","아주 천천히 다가감","곰곰이 옆에 폭 기대 앉음"),
 ("08","아침 커튼","Seedance 1.5","가까이 다가감","창틀로 폴짝 올라옴"),
 ("09","따뜻한 빵","Seedance 1.5","천천히 다가감","날갯짓하며 부스러기를 받음"),
 ("10","한 입씩 음미","Seedance 1.5 (그림 재생성)","천천히 돎","빵 조각 물고 고개 끄덕"),
 ("11","마무리 · 노을 소풍","Wan 2.7 (5초)","위로 오르며 멀어짐","담요 위에서 폴짝"),
]
rows = "".join(f'<tr><td>{cid}</td><td>{name}</td><td class="m">{model}</td><td>{cam}</td><td>{kong}</td></tr>'
              for cid, name, model, cam, kong in CUTS)

html = f'''<title>곰곰한 마음 3화</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--ok:#5E8A4E;--fix:#B7862A;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--fix:#E0B45A}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--fix:#E0B45A}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72;padding:0 16px;padding-block:38px 70px}}
.wrap{{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:36px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(28px,7vw,40px);line-height:1.28;margin:0 0 10px;text-wrap:balance}}
h2{{font-family:var(--round);font-size:22px;margin:0 0 8px;font-weight:400}}
.soft{{color:var(--soft);font-size:15px}}
.stage{{display:flex;justify-content:center}}
video{{width:100%;max-width:420px;aspect-ratio:9/16;border-radius:22px;background:#000;display:block;box-shadow:0 8px 30px rgba(0,0,0,.15)}}
.checks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px}}
.chk{{background:var(--card);border:1px solid var(--ok);border-radius:14px;padding:12px 14px;font-size:14px;display:flex;gap:8px;align-items:flex-start}}
.chk::before{{content:"✓";color:var(--ok);font-weight:700;flex-shrink:0}}
.fixes{{display:flex;flex-direction:column;gap:10px}}
.fixnote{{background:var(--card);border:1px solid var(--fix);border-radius:16px;padding:14px 16px;font-size:14.5px;display:flex;flex-direction:column;gap:6px}}
.fixnote b.t{{font-family:var(--round);font-size:17px;font-weight:400;color:var(--fix)}}
.tw{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;min-width:640px}}
th,td{{padding:9px 8px;border-bottom:1px solid var(--edge);text-align:left;vertical-align:top}}
th{{font-size:12px;color:var(--soft);font-weight:500}}
td.m{{color:var(--honey);font-weight:700;white-space:nowrap}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}}
.stat{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px}}
.stat .v{{font-family:var(--round);font-size:22px;font-variant-numeric:tabular-nums}}
.stat .l{{font-size:12px;color:var(--soft)}}
.ask{{border-top:2px dashed var(--edge);padding-top:24px;display:flex;flex-direction:column;gap:10px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px;font-size:15px}}
.q b{{font-family:var(--round);font-size:17px;font-weight:400;display:block;margin-bottom:2px}}
</style>
<div class="wrap">
<section>
<p class="eye">곰곰한 마음 · 3화 완성</p>
<h1>에피쿠로스가 말한 작은 행복</h1>
<p class="soft">11컷 전부 영상, Luna 내레이션, 자막, 배경음악까지 들어간 완성본입니다. 총 {tl['total']:.0f}초. 화질을 낮춘 미리보기이고, 원본 1080p 파일은 따로 보내드렸습니다.</p>
</section>

<section class="stage"><video src="data:video/mp4;base64,{vid}" controls playsinline preload="metadata"></video></section>

<section>
<h2>요청하신 것</h2>
<div class="fixes">
<div class="fixnote"><b class="t">곰곰이는 입을 벌리지 않습니다</b>
<p>11컷 모두 곰곰이가 <b>입 다문 미소</b>를 짓게 했고, 영상마다 프레임을 뽑아 확인했습니다. 마무리 장면에서는 곰곰이가 날아오르지 않고 소풍 담요에 앉아 있고, 카메라만 멀어집니다.</p></div>
<div class="fixnote"><b class="t">2화 마무리 장면도 고쳤습니다</b>
<p>2화 끝에서 입을 벌리고 날아가던 갈색 곰은 <b>콩이가 다른 모습으로 바뀐 것</b>이었습니다. 이 컷만 다시 뽑아서, 이제는 둘 다 언덕에 앉아 있고 별만 하늘로 올라갑니다. 2화 수정본은 앞서 보내드렸습니다.</p></div>
</div>
</section>

<section>
<h2>만들면서 고친 것</h2>
<div class="fixes">
<div class="fixnote"><b class="t">부엉이 할아버지가 컷마다 다르게 나옴 → 통일</b>
<p>처음에는 부엉이 할아버지가 컷마다 갈색, 곰 귀 달린 회색, 안경 없는 아기 부엉이로 다르게 나왔습니다. 영상으로 만들기 전에 발견해서, 모습을 자세히 적어 03·04·05번 그림을 다시 그렸습니다(그림값 3크레딧, 영상 크레딧은 쓰지 않음).</p></div>
<div class="fixnote"><b class="t">10번에서 곰곰이가 식빵을 입에 물고 있음 → 손에 들게</b>
<p>빵을 씹는 동작이 들어가면 입이 벌어질 수 있어서, <b>빵은 두 손에 들고 입은 다문 모습</b>으로 다시 그렸습니다.</p></div>
</div>
</section>

<section>
<h2>그 외 점검한 것</h2>
<div class="checks">
<div class="chk">부엉이 할아버지 02~05 같은 모습</div>
<div class="chk">콩이가 다른 캐릭터로 변하지 않음</div>
<div class="chk">콩이가 매 컷 실제로 움직임</div>
<div class="chk">화면에 깨진 글자 없음</div>
<div class="chk">자막 11컷 모두 또렷하게 읽힘</div>
<div class="chk">검은 화면·소리 끊김 없음</div>
</div>
</section>

<section>
<h2>컷별 구성</h2>
<div class="tw"><table>
<tr><th>#</th><th>장면</th><th>모델</th><th>카메라</th><th>콩이</th></tr>
{rows}
</table></div>
</section>

<section>
<h2>크레딧</h2>
<div class="stats">
<div class="stat"><div class="v">99.05</div><div class="l">시작 잔액</div></div>
<div class="stat"><div class="v">7.5</div><div class="l">2화 마무리 수정</div></div>
<div class="stat"><div class="v">53.25</div><div class="l">3화 제작 (재생성 포함)</div></div>
<div class="stat"><div class="v">38.3</div><div class="l">남은 잔액</div></div>
</div>
<p class="soft" style="margin-top:10px">한 편을 만드는 데 약 55~60크레딧이 드는데 38이 남아서, <b>지금 크레딧으로는 4화를 만들 수 없습니다.</b></p>
</section>

<section class="ask">
<div class="q"><b>다음은 어떻게 할까요?</b>1) 3편으로 마무리하고 업로드 준비(제목·설명·해시태그·썸네일 문구) — 크레딧이 들지 않습니다<br>2) 크레딧을 충전하고 4~6화 이어서 제작<br>고치고 싶은 컷이 있으면 번호를 알려주세요.</div>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024/1024, 2), "MB")
