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
 ("B1", "v3_boat_sage.png", "보터햇 · 세이지 리본", "새싹 색과 맞아 콩이와 한 세트처럼 보입니다. 귀가 양옆에 그대로 드러납니다.", "추천"),
 ("B2", "v3_boat_honey.png", "보터햇 · 꿀색 리본", "가장 따뜻한 느낌. 크림색 곰과 톤이 비슷해 리본이 덜 도드라집니다.", ""),
 ("B3", "v3_boat_navy.png", "보터햇 · 네이비 줄무늬", "가장 클래식한 여름 보터. 색 대비가 강해 멀리서도 잘 보입니다.", ""),
 ("S1a", "v3_s1_heart.png", "하트 배지", "시즌 1 '마음 사전'과 뜻이 바로 이어집니다. 작지만 또렷합니다.", "추천"),
 ("S1b", "v3_s1_pot.png", "꿀단지 배지 (크게)", "곰다운 소품. 크게 키워 잘 보이지만, 가슴을 많이 가려 다른 배지들과 크기가 달라집니다.", ""),
 ("S1c", "v3_s1_clover.png", "네잎클로버 배지", "행운의 의미. 초록이라 콩이 새싹·시즌 2 별과 겹치지 않게 조율이 필요합니다.", ""),
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
  <h1>보터햇과 시즌 1 배지</h1>
  <p class="lead"><b>확정</b> — 갈색 가방은 늘 메고, 배지는 시즌 2 별 · 시즌 3 단풍잎 · 시즌 4 데이지. 모자는 앞의 네 가지를 모두 빼고 말씀하신 <b>보터햇</b>(윗면이 평평하고 챙이 빳빳한 밀짚모자)을 리본 색만 바꿔 뽑았습니다. 시즌 1 배지는 아직 정하지 않으셔서 후보 셋을 함께 올립니다.</p>
</section>
<div class="kong"><b>콩이 · 공통</b><span>머리에 콩나물 새싹 두 잎. 이름이 '콩'이라서 붙였습니다. 네 시안 모두 같습니다.</span></div>
<section>
  <h2>보터햇(위 셋) · 시즌 1 배지 후보(아래 셋)</h2>
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
  <p><b>보터햇 리본(B1~B3)과 시즌 1 배지(S1a~S1c)를 골라주세요.</b> 고르시면 시즌 1용 기준 이미지를 확정본으로 만들고 4화부터 적용합니다. 보터햇은 여름·나들이 에피소드에서 씁니다.</p>
  <p class="soft">1~3화는 소품 없이 완성돼 있으니, 4화 첫 장면에서 콩이가 가방과 꿀방울 배지를 선물하는 식으로 이야기에 넣으면 자연스럽습니다. "꼴배지"는 꿀배지로 이해했습니다 — 꽃배지를 말씀하신 거라면 S4 데이지가 그 안입니다.</p>
  <p class="soft">기획서: shorts/gomgom/seasons_plan.md · 시안 원본: shorts/gomgom/ref/v2/v3_*.png</p>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024/1024, 2), "MB")
