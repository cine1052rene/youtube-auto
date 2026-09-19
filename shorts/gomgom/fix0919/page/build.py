# -*- coding: utf-8 -*-
# 1·2화 보정 전후 비교 페이지 빌더 → index.html
import base64, pathlib
H = pathlib.Path(__file__).parent
V = H / "v"

def b64(name):
    return base64.b64encode((V / name).read_bytes()).decode()

CUTS = [
    # key, 화, 컷, 제목, 문제, 바꾼 것, 모델 변화
    ("e1_04", "1화", "04", "소파에서 하품",
     "하품하며 입을 크게 벌림",
     "시작 그림부터 새로 그려, 졸린 듯 머리를 긁적이며 윙크하는 입 다문 표정으로",
     None),
    ("e1_10", "1화", "10", "머리 위에 내려앉는 콩이",
     "4초부터 입을 벌리며 얼굴 비율이 달라져 다른 곰처럼 보임",
     "다른 영상과 섞지 않고 이전 컷 하나만 사용. 입이 벌어지기 직전인 3.8초에서 잘라, 비행 앵글은 그대로 두고 입 다문 얼굴로 끝남",
     "이전 컷을 3.8초에서 자름"),
    ("e1_13", "1화", "13", "창턱에서 보는 노을 마을 · 마무리",
     "1~3초 구간에서 입 벌린 웃음 + 얼굴 초근접. 첫 보정본은 캐릭터는 좋았지만 카메라가 뒤로 물러나기만 해 밋밋함",
     "앞부분은 Seedance 컷(뒷모습, 콩이가 기댐)을 쓰고, 이전 컷에서 머리 뒤를 스쳐 창밖 마을 위로 날아가는 무빙(3.9초~)만 이어 붙임",
     "기댐은 Seedance · 날아가는 무빙은 Wan"),
    ("e2_12", "2화", "12", "수평이 된 저울",
     "박수 치며 입을 벌려 웃음. 게다가 시작 그림의 저울부터 한쪽으로 기울어 있어, 2화 결말인 \"마음의 저울이 수평을 되찾는다\"가 전달되지 않음",
     "시작 그림을 새로 그려 가로대를 완전히 수평으로, 두 접시를 같은 높이로 고정. 박수는 빼고 입 다문 채 몸을 살랑 흔들기, 콩이는 옆에서 춤",
     None),
]

cards = []
for key, ep, cut, title, prob, fix, model in CUTS:
    tag = f'<span class="model">{model}</span>' if model else ""
    cards.append(f'''
<article class="cut" id="{key}">
  <header class="cut-head">
    <p class="where">{ep} <b>{cut}</b></p>
    <h2>{title}</h2>
    {tag}
  </header>
  <div class="pair">
    <figure class="clip before">
      <video src="data:video/mp4;base64,{b64(key + "_old.mp4")}" muted loop playsinline autoplay preload="auto"></video>
      <figcaption>이전</figcaption>
    </figure>
    <figure class="clip after">
      <video src="data:video/mp4;base64,{b64(key + "_new.mp4")}" muted loop playsinline autoplay preload="auto"></video>
      <figcaption>바뀐 컷</figcaption>
    </figure>
  </div>
  <dl class="notes">
    <div><dt>문제</dt><dd>{prob}</dd></div>
    <div><dt>바꾼 것</dt><dd>{fix}</dd></div>
  </dl>
  <button type="button" class="sync" id="sync-{key}">처음부터 같이 보기</button>
</article>''')

html = f'''<title>곰곰이 보정 비교</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--ok:#5E8A4E;--old:#A89C90;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--old:#7D7064}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--old:#7D7064}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.7;padding:0 16px;padding-block:36px 72px}}
.wrap{{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:8px}}
h1{{font-family:var(--round);font-weight:400;font-size:clamp(28px,7vw,38px);line-height:1.3;margin:0 0 10px;text-wrap:balance}}
.lead{{color:var(--soft);font-size:15px;max-width:60ch}}
.rules{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}
.rules span{{font-size:13px;border:1px solid var(--edge);background:var(--card);border-radius:999px;padding:4px 12px}}
.cut{{background:var(--card);border:1px solid var(--edge);border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:14px}}
.cut-head{{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}}
.where{{font-size:13px;color:var(--soft)}}
.where b{{color:var(--honey);font-size:15px}}
h2{{font-family:var(--round);font-weight:400;font-size:20px;margin:0;text-wrap:balance}}
.model{{font-size:12px;font-weight:700;color:var(--honey);border:1px solid var(--honey);border-radius:999px;padding:1px 10px;margin-left:auto}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.clip{{margin:0;display:flex;flex-direction:column;gap:6px}}
.clip video{{width:100%;max-width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:12px;background:#000;display:block;border:3px solid var(--old)}}
.after video{{border-color:var(--honey)}}
.clip figcaption{{font-size:13px;text-align:center;color:var(--soft)}}
.after figcaption{{color:var(--honey);font-weight:700}}
.notes{{margin:0;display:grid;gap:6px;font-size:14.5px}}
.notes div{{display:grid;grid-template-columns:4.5em 1fr;gap:8px}}
.notes dt{{color:var(--soft);font-size:13px;padding-top:1px}}
.notes dd{{margin:0}}
.notes div:last-child dd{{color:var(--ok);font-weight:500}}
.sync{{align-self:flex-start;font:inherit;font-size:14px;color:var(--ink);background:transparent;border:1px solid var(--edge);border-radius:999px;padding:6px 16px;cursor:pointer}}
.sync:hover{{border-color:var(--honey);color:var(--honey)}}
.sync:focus-visible{{outline:2px solid var(--honey);outline-offset:2px}}
.foot{{border-top:2px dashed var(--edge);padding-top:22px;display:flex;flex-direction:column;gap:10px;font-size:15px}}
.foot b{{font-family:var(--round);font-weight:400;font-size:18px}}
.foot .soft{{color:var(--soft);font-size:14px}}
@media (prefers-reduced-motion:reduce){{.clip video{{animation:none}}}}
</style>
<div class="wrap">
<section>
  <p class="eye">곰곰한 마음 · 1·2화 보정</p>
  <h1>1·2화에서 달라진 4컷</h1>
  <p class="lead">3화 때 정한 "곰곰이는 항상 입 다문 미소" 규칙을 1·2화에도 맞췄습니다. 왼쪽이 이전 컷, 오른쪽이 바뀐 컷입니다. 두 영상은 자동으로 반복되고, 버튼을 누르면 둘 다 처음부터 같이 시작합니다. 1화 05와 2화 09는 이전 컷이 더 좋아서 그대로 두었습니다.</p>
  <div class="rules"><span>입 다문 미소</span><span>곰곰이는 날지 않음</span><span>얼굴 초근접 없음</span><span>얼굴 큰 컷은 Seedance</span></div>
</section>
{"".join(cards)}
<section class="foot">
  <b>이 4컷을 넣어 1·2화를 다시 조립했습니다</b>
  <p>전체 영상은 보정본 미리보기 페이지(https://claude.ai/artifact/7RhMMhP83q1aoDjsGrewyL)에서 보실 수 있습니다.</p>
  <p class="soft">1화 13만 모델 두 개를 이어 붙인 컷입니다. 전체 흐름에서 어색하면 한쪽으로 통일하겠습니다.</p>
</section>
</div>
<script>
document.querySelectorAll(".sync").forEach(function(btn){{
  btn.addEventListener("click",function(){{
    var vids=btn.closest(".cut").querySelectorAll("video");
    vids.forEach(function(v){{try{{v.pause();v.currentTime=0;}}catch(e){{}}}});
    vids.forEach(function(v){{var p=v.play();if(p&&p.catch)p.catch(function(){{}});}});
  }});
}});
</script>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html) / 1024 / 1024, 2), "MB")
