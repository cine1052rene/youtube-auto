# -*- coding: utf-8 -*-
# 1·2화 보정 완성본 검토 페이지 → index.html
import base64, json, pathlib
H = pathlib.Path(__file__).parent
G = H.parent.parent
def b64(p): return base64.b64encode((G / p).read_bytes()).decode()
t1 = json.load(open(G / "ep01/v3/out/timeline.json", encoding="utf-8"))["total"]
t2 = json.load(open(G / "ep02/prod/out/timeline.json", encoding="utf-8"))["total"]
EPS = [
  ("1화", "쉬어도 쉬어도 피곤한 이유", "ep01/v3/out/ep01_v3_preview.mp4", t1, [
    ("04", "하품 → 윙크하며 머리 긁적이는 입 다문 표정 (새로 뽑음)"),
    ("05", "그대로 — 빛구슬 사이로 곰곰이가 떠오르는 원래 컷"),
    ("10", "원래 컷 하나만 사용. 입이 벌어지기 직전(3.8초)에서 잘라 비행 앵글은 살리고 입 다문 얼굴로 끝남"),
    ("13", "뒷모습으로 콩이가 기댄 뒤, 원래 컷의 '마을 위로 날아가는' 무빙으로 마무리 (이어 붙임 — 검토 부탁)"),
  ]),
  ("2화", "칭찬은 금방 잊고, 한마디 지적은 오래 남는 이유", "ep02/prod/out/ep02_preview.mp4", t2, [
    ("09", "그대로 — 원래 컷의 용기 포즈 카메라 무빙"),
    ("12", "저울 가로대가 끝까지 수평, 곰곰이는 입 다문 채 살랑 (새로 뽑음)"),
    ("13", "마무리: 고개 돌릴 때 만화 곰으로 바뀌던 Wan 컷을 Seedance로 교체. 끝까지 펠트 곰 뒷모습, 별만 하늘로 (새로 뽑음)"),
  ]),
]
blocks = []
for ep, title, vid, total, changes in EPS:
    items = "".join(f'<li><b>{c}</b><span>{t}</span></li>' for c, t in changes)
    blocks.append(f'''<article class="ep">
  <div class="stage"><video src="data:video/mp4;base64,{b64(vid)}" controls playsinline preload="metadata"></video></div>
  <div class="info">
    <p class="eye">{ep} · {total:.0f}초</p>
    <h2>{title}</h2>
    <ul class="changes">{items}</ul>
  </div>
</article>''')
html = f'''<title>곰곰한 마음 1·2화 보정본</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.7;padding:0 16px;padding-block:36px 72px}}
.wrap{{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:32px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:6px}}
h1{{font-family:var(--round);font-weight:400;font-size:clamp(28px,7vw,38px);line-height:1.3;margin:0 0 10px;text-wrap:balance}}
h2{{font-family:var(--round);font-weight:400;font-size:21px;margin:0 0 12px;text-wrap:balance}}
.lead{{color:var(--soft);font-size:15px;max-width:60ch}}
.ep{{display:grid;grid-template-columns:minmax(0,300px) 1fr;gap:24px;align-items:start;background:var(--card);border:1px solid var(--edge);border-radius:20px;padding:20px}}
@media (max-width:640px){{.ep{{grid-template-columns:1fr}}}}
.stage video{{width:100%;max-width:100%;aspect-ratio:9/16;border-radius:14px;background:#000;display:block}}
.changes{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px;font-size:14.5px}}
.changes li{{display:grid;grid-template-columns:2.4em 1fr;gap:8px}}
.changes b{{color:var(--honey);font-variant-numeric:tabular-nums}}
.foot{{border-top:2px dashed var(--edge);padding-top:22px;display:flex;flex-direction:column;gap:8px;font-size:15px}}
.foot .soft{{color:var(--soft);font-size:14px}}
</style>
<div class="wrap">
<section>
  <p class="eye">곰곰한 마음 · 보정본</p>
  <h1>1·2화, 다시 이어 붙였습니다</h1>
  <p class="lead">말씀하신 대로 반영해서 두 편을 다시 조립했습니다. 화질을 낮춘 미리보기입니다. 오른쪽 목록은 이번에 달라진 컷입니다.</p>
</section>
{"".join(blocks)}
<section class="foot">
  <p><b>1화 13</b>(마지막 장면)을 이어서 보시고 괜찮은지 알려주세요. 어색하면 원래 컷이나 뒷모습 컷 중 하나로 통일하겠습니다.</p>
  <p class="soft">원본 1080p는 PC에 있습니다 — ep01/v3/out/ep01_v3.mp4 · ep02/prod/out/ep02.mp4 (업로드용 경량본 *_send.mp4)</p>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024/1024, 2), "MB")
