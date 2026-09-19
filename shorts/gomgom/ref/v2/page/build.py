# -*- coding: utf-8 -*-
# 곰곰이·콩이 시그니처 시안 + 시즌 기획 페이지 → index.html
import base64, io, pathlib
from PIL import Image
H = pathlib.Path(__file__).parent
R = H.parent
def img64(name, w=560):
    im = Image.open(R / name).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=86)
    return base64.b64encode(b.getvalue()).decode()
OPTS = [
 ("S1", "v2_honey.png", "꿀방울 배지", "시즌 1 제안. 곰이라서 꿀. 다만 배지가 작아 먼 장면에선 잘 안 보여서, 확정하면 조금 크게 키우겠습니다.", "시즌 1"),
 ("S2", "v2_star.png", "별 배지", "시즌 2 제안. 모양이 단순해서 가장 또렷하게 보이고, 2화의 별 병과도 이어집니다.", "시즌 2"),
 ("S3", "opt_b.png", "단풍잎 배지", "시즌 3 제안. 동양의 지혜 시즌의 가을 정취와 어울립니다.", "시즌 3"),
 ("S4", "v2_daisy.png", "데이지 배지", "시즌 4 제안. 다정함·관계 시즌에 어울리는 꽃.", "시즌 4"),
 ("H1", "v2_rain.png", "노란 비 모자", "콩이와 색이 맞아 둘이 한 세트처럼 보입니다. 비 오는 날 에피소드에.", "추천"),
 ("H2", "v2_straw.png", "밀짚모자", "귀가 챙 아래로 나와 곰 실루엣이 유지됩니다. 여름·소풍 에피소드에.", "추천"),
 ("H3", "v2_bucket.png", "세이지 버킷햇", "산책·외출 장면에. 귀가 옆으로 살짝 가려집니다.", ""),
 ("H4", "v2_bobble.png", "털방울 니트 모자", "모자 구멍 두 개가 눈처럼 보여 얼굴이 두 개인 듯합니다. 빼는 걸 권합니다.", "주의"),
]
cards = "".join(f'''<figure class="opt{" rec" if tag in ("추천",) else ""}">
  <img src="data:image/jpeg;base64,{img64(f)}" alt="시안 {k}: {name}">
  <figcaption><span class="k">{k}</span><b>{name}</b>{f'<em class="tag {"warn" if tag=="주의" else ""}">{tag}</em>' if tag else ""}<p>{desc}</p></figcaption>
</figure>''' for k, f, name, desc, tag in OPTS)
SEASONS = [
 ("시즌 1", "곰곰이의 마음 사전", "진행 중", ["쉬어도 피곤한 이유", "칭찬·지적의 무게", "에피쿠로스의 작은 행복", "남과 비교할 때", "걱정 내려놓기", "괜히 서운할 때"]),
 ("시즌 2", "나는 왜 이럴까", "일상 심리", ["계획 오류", "스포트라이트 효과", "자이가르닉 효과", "선택의 역설", "쾌락 적응", "피크엔드 법칙"]),
 ("시즌 3", "천천히 가도 괜찮아", "동양의 지혜", ["장자 · 무용지용", "노자 · 상선약수", "공자 · 모른다는 용기", "두 번째 화살", "와비사비·킨츠기", "휘게"]),
 ("시즌 4", "나한테도 친절하게", "관계와 나", ["자기 자비", "가면 현상", "아리스토텔레스의 우정", "친사회적 소비", "경외감", "감사 세 줄"]),
]
seasons = "".join(f'''<section class="season">
  <p class="sn">{n} <span>{sub}</span></p><h3>{t}</h3>
  <ol>{"".join(f"<li>{e}</li>" for e in eps)}</ol>
</section>''' for n, t, sub, eps in SEASONS)
html = f'''<title>곰곰이 새 옷 시안</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--sage:#6F8F68;--warn:#B4553A;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--sage:#9DBB93;--warn:#E28A6E}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--sage:#9DBB93;--warn:#E28A6E}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.7;padding:0 16px;padding-block:36px 72px}}
.wrap{{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:34px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:8px}}
h1{{font-family:var(--round);font-weight:400;font-size:clamp(28px,7vw,40px);line-height:1.3;margin:0 0 10px;text-wrap:balance}}
h2{{font-family:var(--round);font-weight:400;font-size:24px;margin:0 0 12px}}
.lead{{color:var(--soft);font-size:15px;max-width:62ch}}
.kong{{display:flex;gap:10px;align-items:baseline;background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:12px 16px;font-size:14.5px}}
.kong b{{color:var(--sage);white-space:nowrap}}
.opts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}}
.opt{{margin:0;background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.opt.rec{{border:2px solid var(--sage)}}
.opt img{{width:100%;max-width:100%;aspect-ratio:3/4;object-fit:cover;display:block}}
.opt figcaption{{padding:12px 14px 16px;font-size:13.5px;display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center}}
.opt .k{{font-family:var(--round);font-size:22px;color:var(--honey);line-height:1}}
.opt b{{font-size:15px}}
.opt p{{flex-basis:100%;color:var(--soft);margin-top:4px}}
.tag{{font-style:normal;font-size:11.5px;font-weight:700;border-radius:999px;padding:1px 9px;border:1px solid var(--sage);color:var(--sage)}}
.tag.warn{{border-color:var(--warn);color:var(--warn)}}
.rules{{display:grid;gap:8px;margin:0;padding:0;list-style:none;font-size:14.5px}}
.rules li{{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:10px 14px}}
.rules b{{color:var(--honey)}}
.seasons{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}}
.season{{background:var(--card);border:1px solid var(--edge);border-radius:16px;padding:14px 16px}}
.sn{{font-size:12px;font-weight:700;color:var(--honey);letter-spacing:.08em}}
.sn span{{color:var(--soft);font-weight:500;margin-left:6px}}
h3{{font-family:var(--round);font-weight:400;font-size:19px;margin:2px 0 8px}}
.season ol{{margin:0;padding-left:1.3em;font-size:13.5px;display:grid;gap:2px}}
.ask{{border-top:2px dashed var(--edge);padding-top:22px;font-size:15px;display:flex;flex-direction:column;gap:8px}}
.ask .soft{{color:var(--soft);font-size:14px}}
</style>
<div class="wrap">
<section>
  <p class="eye">곰곰한 마음 · 캐릭터 정리</p>
  <h1>가방은 늘, 배지는 시즌마다</h1>
  <p class="lead">말씀하신 대로 배지와 가방으로 갑니다. <b>작은 갈색 가방은 곰곰이의 고정 시그니처</b>로 늘 메고, <b>배지는 시즌마다 바꿔</b> 어느 시즌 영상인지 한눈에 알아보게 했습니다. 모자는 늘 쓰는 대신 비 오는 날·소풍처럼 <b>에피소드 상황에 맞춰</b> 씁니다. 베레모는 뺐습니다.</p>
</section>
<div class="kong"><b>콩이 · 공통</b><span>머리에 콩나물 새싹 두 잎. 이름이 '콩'이라서 붙였습니다. 네 시안 모두 같습니다.</span></div>
<section>
  <h2>시즌 배지(위 넷) · 상황 모자(아래 넷)</h2>
  <div class="opts">{cards}</div>
</section>
<section>
  <h2>새로 정한 연출 규칙</h2>
  <ul class="rules">
    <li><b>입</b> — 벌려도 괜찮지만 이빨은 절대 보이지 않게</li>
    <li><b>캐릭터</b> — 만화 곰으로 바뀌지 않게, 끝까지 펠트 인형 질감</li>
    <li><b>생동감</b> — 카메라나 캐릭터 중 하나는 움직이기. 제자리 줌인·줌아웃만 하는 컷은 쓰지 않기</li>
    <li><b>비행</b> — 곰곰이도 필요하면 날아도 됨</li>
  </ul>
</section>
<section>
  <h2>시즌 기획</h2>
  <p class="lead" style="margin-bottom:12px">6편씩 네 시즌, 모두 24편입니다. 편마다 실제 연구나 원전을 하나씩 근거로 둡니다. 편별 훅·근거·장면은 기획서 파일에 있습니다.</p>
  <div class="seasons">{seasons}</div>
</section>
<section class="ask">
  <p><b>이 조합으로 확정할까요?</b> 배지 순서를 바꾸거나 빼고 싶은 게 있으면 번호(S1~S4, H1~H4)로 알려주세요. 확정하면 시즌 1 기준 이미지(꿀방울 배지 + 가방)를 새로 만들고 4화부터 적용합니다.</p>
  <p class="soft">1~3화는 소품 없이 완성돼 있으니, 4화 첫 장면에서 콩이가 가방과 꿀방울 배지를 선물하는 식으로 이야기에 넣으면 자연스럽습니다. "꼴배지"는 꿀배지로 이해했습니다 — 꽃배지를 말씀하신 거라면 S4 데이지가 그 안입니다.</p>
  <p class="soft">기획서: shorts/gomgom/seasons_plan.md · 시안 원본: shorts/gomgom/ref/v2/v2_*.png</p>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024/1024, 2), "MB")
