# -*- coding: utf-8 -*-
import base64, pathlib
H = pathlib.Path(__file__).parent
a = lambda n: base64.b64encode((H / f"{n}.mp3").read_bytes()).decode()
LINE_N = "쉬는 날 하루 종일 누워 있었는데, 왜 더 피곤할까요? 곰곰이도 그랬어요."
LINE_B = "쉬는 날 하루 종일 누워 있었는데, 왜 더 피곤할까? 나도 그랬어."
el = [("Hana",193,"7.0초","동양 이름이라 골라봤습니다"),
      ("Luna",311,"7.0초","열 개 중 가장 높은 목소리"),
      ("Willow",190,"6.4초",""),
      ("Daisy",225,"6.2초",""),
      ("Pixie",232,"5.4초",""),
      ("Kiki",187,"6.2초",""),
      ("Mabel",232,"7.9초","천천히 읽는 편"),
      ("Emily",218,"5.2초","가장 빠르게 읽음"),
      ("Chloe",262,"5.6초","두 번째로 높은 목소리"),
      ("Nora",172,"8.2초","가장 느리고 낮은 편")]
free = [("F1","여자 1",200),("F2","여자 2",246),("F3","여자 3",189),("F4","여자 4",218),("F5","여자 5",170),("M1","남자 1 · 가벼운 톤",172)]
bear = [("bear_p4","곰곰이 · 조금 높게",242,"여자 1 목소리를 4반음 올림"),("bear_p6","곰곰이 · 더 높게",259,"여자 1 목소리를 6반음 올림")]
def row(key, title, meta, sub="", tag=None):
    return f'''<div class="v"><div class="vh"><span class="tag">{tag or key}</span><b>{title}</b><span class="hz">{meta}</span></div>
{f'<p class="sub">{sub}</p>' if sub else ''}<audio controls preload="none" src="data:audio/mpeg;base64,{a(key)}"></audio></div>'''
el_rows = "".join(row(f"el_{n}", n, f"{hz}Hz · {d}", s, tag="EL") for n,hz,d,s in el)
free_rows = "".join(row(k, t, f"{hz}Hz") for k,t,hz in free)
bear_rows = "".join(row(k, t, f"{hz}Hz", s) for k,t,hz,s in bear)
html = f'''<title>곰곰이 목소리 고르기</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--rose:#C9707A;--no:#B5543C;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--rose:#E39AA2;--no:#E08A70}}}}
:root[data-theme="dark"]{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--rose:#E39AA2;--no:#E08A70}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;padding:0 18px;padding-block:40px 70px}}
.wrap{{max-width:680px;margin:0 auto;display:flex;flex-direction:column;gap:38px}}
p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}}
h1{{font-family:var(--round);font-size:clamp(28px,7.5vw,40px);line-height:1.28;margin:0 0 12px;text-wrap:balance}}
h2{{font-family:var(--round);font-size:23px;margin:0 0 6px}}
.soft{{color:var(--soft);font-size:15px}}
.line{{background:var(--card);border-left:3px solid var(--honey);padding:11px 14px;font-family:var(--round);font-size:16.5px;margin:12px 0 16px;border-radius:0 12px 12px 0}}
.list{{display:flex;flex-direction:column;gap:10px}}
.v{{background:var(--card);border:1px solid var(--edge);border-radius:16px;padding:13px 15px;display:flex;flex-direction:column;gap:8px}}
.vh{{display:flex;align-items:center;gap:10px}}
.vh b{{font-family:var(--round);font-size:17px;font-weight:400;flex:1}}
.tag{{font-size:12px;font-weight:700;background:var(--honey);color:#2A2118;padding:2px 8px;border-radius:8px}}
.new .tag{{background:var(--rose);color:#2A1518}}
.hz{{font-size:13px;color:var(--soft);font-variant-numeric:tabular-nums;white-space:nowrap}}
.sub{{font-size:13px;color:var(--soft)}}
audio{{width:100%;height:40px}}
.new{{border:2px solid var(--rose);border-radius:20px;padding:18px 16px 20px;background:color-mix(in srgb,var(--rose) 6%,transparent)}}
.badge{{display:inline-block;font-size:12px;font-weight:700;color:var(--rose);letter-spacing:.08em;margin-bottom:6px}}
.note{{background:var(--card);border:1px dashed var(--edge);border-radius:14px;padding:12px 14px;font-size:14px;color:var(--soft);margin-bottom:14px}}
.excl{{background:var(--card);border:1px dashed var(--edge);border-radius:16px;padding:14px 16px;font-size:14.5px;color:var(--soft)}}
.excl b{{color:var(--no)}}
details{{background:var(--card);border:1px solid var(--edge);border-radius:18px;padding:14px 16px}}
summary{{cursor:pointer;font-family:var(--round);font-size:19px}}
details > .inner{{margin-top:14px;display:flex;flex-direction:column;gap:26px}}
.ask{{border-top:2px dashed var(--edge);padding-top:24px;display:flex;flex-direction:column;gap:10px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:13px 15px;font-size:15px}}
.q b{{font-family:var(--round);font-size:17px;font-weight:400;display:block;margin-bottom:2px}}
</style>
<div class="wrap">
<section>
<p class="eye">곰곰한 마음 · 목소리 정하기</p>
<h1>곰곰이에게 어울리는 목소리</h1>
<p class="soft">1화 첫 두 문장을 여러 목소리로 읽혀봤습니다. 이어폰으로 들어보시길 권합니다.</p>
</section>

<section class="new">
<span class="badge">새로 추가 · ElevenLabs</span>
<h2>ElevenLabs 목소리 10개</h2>
<p class="soft">Higgsfield 안의 ElevenLabs 엔진으로 뽑았습니다. 10개에 1.5크레딧 들었습니다.</p>
<div class="line">“{LINE_N}”</div>
<div class="note">이름만 보고 골랐는데, 음높이를 재보니 10개 모두 여자 목소리 범위입니다. 한국어 발음이 자연스러운지는 기계로 확인하지 못해서 직접 들어봐 주셔야 합니다.</div>
<div class="list">{el_rows}</div>
</section>

<details>
<summary>무료 TTS 목소리 · 곰곰이 변형 (앞서 만든 것)</summary>
<div class="inner">
<div class="excl"><b>뺀 목소리</b> — 무료 남자 목소리 2~5번은 98~131Hz로 중후해서 제외했습니다.</div>
<section>
<h2>방식 A · 해설자 (무료)</h2>
<div class="line">“{LINE_N}”</div>
<div class="list">{free_rows}</div>
</section>
<section>
<h2>방식 B · 곰곰이가 직접 말하기</h2>
<p class="soft">대본 6편을 반말 1인칭으로 고쳐야 합니다. 여자 목소리 음높이를 올려 만들어서 약간 기계적으로 들릴 수 있습니다.</p>
<div class="line">“{LINE_B}”</div>
<div class="list">{bear_rows}</div>
</section>
</div>
</details>

<section class="ask">
<div class="q"><b>마음에 드는 목소리 이름만 알려주세요</b>예: “Hana”, “Luna”, 무료 중엔 “F4”</div>
<p class="soft">두세 개로 좁혀주시면 1화 대본 전체(40초)를 읽혀서 영상에 맞춰 최종 비교해드립니다. 목소리 하나당 약 1.5크레딧입니다.</p>
</section>
</div>'''
(H / "index.html").write_text(html, encoding="utf-8")
print("ok", round(len(html)/1024), "KB")
