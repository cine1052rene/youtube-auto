# -*- coding: utf-8 -*-
"""4·5·6화 점검 페이지 생성기 — 화별 index html (영상 + 컷별 장면 + 제작 메모 + 점검 질문)"""
import base64, json, pathlib, subprocess

G = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(__file__).resolve().parent
PKG = json.load(open(G / "launch" / "package.json", encoding="utf-8"))["eps"]

NOTES = {
    "04": {
        "sub": "사회비교 이론 (Festinger, 1954)",
        "made": [
            ("시즌 1 소품 첫 등장", "곰곰이가 갈색 펠트 가방 + 코랄 하트 배지를 처음 달고 나와요. 친구 캐릭터 <b>보리</b>(흰 토끼, 민트 목도리)도 이 화에서 처음 나와요."),
            ("첫 컷 삭제 → 훅으로 시작", "원래 01번은 콩이가 가방·배지를 선물하는 장면이었는데, 주제(비교)와 상관없고 첫 2초를 잡아먹어서 뺐어요. 지금은 <b>\"친구 소식을 보고 나면,\"</b>으로 바로 시작해요. 그래서 컷 번호가 02부터예요."),
            ("크기 맞춤 5컷 재생성", "부엉이 할아버지가 컷마다 2배로 커지거나, 보리가 1.5배로 나오던 컷(04·05·09·10)을 곰곰이와 같은 키로 다시 만들었어요. 13번은 다시 만들었더니 곰곰이가 입 벌리고 날아가 버려서 원래 컷을 그대로 썼어요."),
            ("영어 음성 사고 수정", "내레이션 2줄이 엉뚱한 영어로 나왔던 걸 받아쓰기 검사로 잡아서 다시 녹음했어요(그중 하나는 지금 09번)."),
            ("소품 2컷 다시 그림", "하트 배지가 형광 플라스틱처럼 보이던 것 → 매트한 펠트로, 액자 속에 실제 사람 사진이 들어가던 것 → 펠트 동물 사진으로 바꿨어요."),
        ],
    },
    "05": {
        "sub": "에픽테토스 『엥케이리디온』 1장 — 통제의 이분법",
        "made": [
            ("12컷 전부 한 번에 통과", "크기 규칙·훅 규칙을 처음부터 넣고 만들어서 <b>다시 만든 컷이 하나도 없어요.</b> 6편 중 가장 깔끔하게 나온 화예요."),
            ("부엉이 할아버지 재등장", "곰곰이와 같은 키로 고정했어요."),
            ("마무리 8초", "마지막 질문 컷은 8초로 길게 만들어 여운을 줬어요."),
        ],
    },
    "06": {
        "sub": "관계 심리학 — 서운함은 말하지 않은 기대의 신호",
        "made": [
            ("12컷 전부 통과", "콩이 시점으로 관점을 바꾸는 장면과 씨앗 심기 마무리로 구성했어요. 다시 만든 컷이 없어요."),
            ("콩이 비중 확대", "이 화는 콩이가 서운해하는 쪽이라 콩이 표정·동작이 많아요. 콩이가 다른 캐릭터로 변하지 않았는지 특히 봐 주세요."),
        ],
    },
}

REGEN = {"04": {"03": "그림 다시", "04": "크기 재생성", "05": "크기 재생성", "09": "크기 재생성", "10": "크기 재생성", "13": "원본 유지"}}

ANALYSIS = {
    "06": [
        ("영상 모델은 5화와 똑같아요", "4·5·6화 모두 <b>그림 Seedream 5 Lite → 영상 Seedance 1.5</b>로 만들었어요. 같은 기준 이미지, 같은 캐릭터 문장, 같은 크기 규칙을 썼어요. 그래서 따로 노는 느낌은 <b>모델 탓이 아니라 장면 연출 차이</b>예요."),
        ("부엉이가 작아진 이유", "부엉이 설명 문장은 5화와 글자 하나까지 같아요. 차이는 <b>장면 문장</b>이에요. 5화는 \"곰곰이 옆에 <b>같은 높이로 서서</b>\"라고 썼고, 6화 06번은 \"<b>옆에서 지켜보는</b> 부엉이\"라고만 써서 그림 모델이 부엉이를 뒤쪽·구석에 작게 앉혔어요. 05번도 둘 다 <b>앉은 자세</b>라 부엉이가 둥글게 웅크려 작아 보여요."),
        ("따로 노는 느낌의 원인 (제 판단)", "① 6화는 곰곰이 <b>얼굴 클로즈업이 많아서</b> 다른 화보다 곰곰이가 화면에 꽉 차요. ② 05·06·10·11번이 <b>배경 없는 크림색 벽</b>이라 미니어처 세계 느낌이 약해요. ③ 콩이가 주인공인 화라 <b>콩이가 규칙보다 크게</b> 나온 컷(07·08·10)이 있어요. ④ 5화는 밤·새벽·노을로 빛이 변하는데 6화는 대부분 <b>밝은 낮</b>이라 단조로워요."),
        ("고치는 방법 (작업 전 확인용)", "부엉이 컷(05·06)은 \"같은 높이로 서서, 곰곰이와 나란히\"로 장면 문장을 고쳐 다시 만들고, 크림 벽 컷(10·11)은 배경을 마을 골목·정원으로 바꾸면 돼요. 한 컷에 약 5크레딧이에요."),
    ],
}

CHECKS = [
    "곰곰이가 만화 곰으로 변하지 않았는지",
    "이빨이 보이는 장면이 없는지",
    "콩이 크기가 곰곰이 머리만 한지",
    "조연(부엉이·보리)이 곰곰이와 같은 키인지",
    "자막 글자가 깨지거나 잘리지 않는지",
    "내레이션이 또렷하고 이상한 소리가 없는지",
    "제자리 줌만 하는 심심한 컷이 없는지",
    "첫 2초가 궁금하게 만드는지",
]


def frame_b64(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1",
                        "-vf", "scale=240:-2", "-q:v", "5", "-f", "image2", "-c:v", "mjpeg", "pipe:1"],
                       capture_output=True, check=True)
    return base64.b64encode(r.stdout).decode()


CSS = """
:root{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--ok:#5E8A4E;--fix:#B7862A;
--round:"Gowun Dodum","Noto Sans KR",sans-serif;--sans:"Noto Sans KR",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--ok:#9BC487;--fix:#E0B45A}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72;padding:0 16px;padding-block:34px 70px;margin:0}
.wrap{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:34px}
p{margin:0}
.eye{font-size:12px;letter-spacing:.18em;color:var(--honey);font-weight:700;margin:0 0 10px}
h1{font-family:var(--round);font-size:clamp(26px,6.5vw,38px);line-height:1.3;margin:0 0 10px;font-weight:400;text-wrap:balance}
h2{font-family:var(--round);font-size:21px;margin:0 0 10px;font-weight:400}
.soft{color:var(--soft);font-size:14.5px}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.pill{background:var(--card);border:1px solid var(--edge);border-radius:999px;padding:4px 12px;font-size:13px}
.stage{display:flex;justify-content:center}
video{width:100%;max-width:400px;aspect-ratio:9/16;border-radius:22px;background:#000;display:block;box-shadow:0 8px 30px rgba(0,0,0,.15)}
.cuts{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.cut{background:var(--card);border:1px solid var(--edge);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.cut img{width:100%;aspect-ratio:9/16;object-fit:cover;display:block;cursor:pointer}
.cut .c{padding:8px 10px 10px;font-size:13px;line-height:1.5}
.cut .n{font-family:var(--round);color:var(--honey);font-size:16px}
.cut .t{color:var(--soft);font-size:11.5px;font-variant-numeric:tabular-nums}
.md{font-size:11.5px;color:var(--soft);margin-top:4px;padding-top:4px;border-top:1px dashed var(--edge);line-height:1.45}
.md .rg{color:var(--fix);font-weight:700}
.ana{border:1px solid var(--honey)}
.notes{display:flex;flex-direction:column;gap:10px}
.note{background:var(--card);border:1px solid var(--fix);border-radius:16px;padding:13px 16px;font-size:14.5px}
.note b.h{font-family:var(--round);font-size:17px;font-weight:400;color:var(--fix);display:block;margin-bottom:2px}
.checks{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}
.chk{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:10px 12px;font-size:14px;display:flex;gap:8px;align-items:flex-start}
.chk::before{content:"□";color:var(--honey);font-weight:700;flex-shrink:0}
.ask{border-top:2px dashed var(--edge);padding-top:22px}
.q{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:15px}
.q b{font-family:var(--round);font-size:18px;font-weight:400;display:block;margin-bottom:4px}
.nav{display:flex;gap:8px;flex-wrap:wrap}
"""


def build(n, idx):
    e = PKG[idx]
    out = G / f"ep{n}" / "prod" / "out"
    tl = json.load(open(out / "timeline.json", encoding="utf-8"))
    vid = base64.b64encode((out / f"ep{n}_preview.mp4").read_bytes()).decode()
    lines = {x["id"]: x["model"] for x in json.load(open(G / f"ep{n}" / "lines.json", encoding="utf-8"))["shots"]}
    cards = []
    for s in tl["shots"]:
        m = lines.get(s["id"], "seedance1_5")
        sec = m.split(":")[1] if ":" in m else "4"
        rg = REGEN.get(n, {}).get(s["id"])
        mdl = f'<div class="md">그림 Seedream 5 Lite<br>영상 Seedance 1.5 · {sec}초' + (f'<br><span class="rg">{rg}</span>' if rg else '') + '</div>'
        mid = s["start"] + s["dur"] * 0.55
        img = frame_b64(out / f"ep{n}.mp4", mid)
        cards.append(
            f'<div class="cut"><img src="data:image/jpeg;base64,{img}" onclick="seek({s["start"]:.2f})" alt="{s["id"]}번 장면">'
            f'<div class="c"><div class="n">{s["id"]}</div><div>{s["text"]}</div>'
            f'<div class="t">{s["start"]:.1f}초 ~ {s["start"] + s["dur"]:.1f}초</div>{mdl}</div></div>')
    nt = NOTES[n]
    notes = "".join(f'<div class="note"><b class="h">{h}</b><p>{b}</p></div>' for h, b in nt["made"])
    ana = "".join(f'<div class="note ana"><b class="h">{h}</b><p>{b}</p></div>' for h, b in ANALYSIS.get(n, []))
    ana_sec = f'<section><h2>왜 따로 노는 느낌일까 — 분석</h2><div class="notes">{ana}</div></section>' if ana else ""
    checks = "".join(f'<div class="chk">{c}</div>' for c in CHECKS)
    when = e["when"].split(" — ")[0]
    html = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 {int(n)}화 점검</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<section>
<p class="eye">곰곰한 마음 · {int(n)}화 점검</p>
<h1>{e["title"]}</h1>
<p class="soft">{nt["sub"]}</p>
<div class="meta"><span class="pill">공개 {when}</span><span class="pill">{tl["total"]:.1f}초</span><span class="pill">{len(tl["shots"])}컷</span></div>
</section>
<section class="stage"><video id="v" src="data:video/mp4;base64,{vid}" controls playsinline preload="metadata"></video></section>
<section>
<h2>컷별 장면</h2>
<p class="soft" style="margin-bottom:12px">사진을 누르면 영상이 그 장면으로 이동해요. 고치고 싶은 컷은 <b>번호</b>로 알려 주세요.</p>
<div class="cuts">{"".join(cards)}</div>
</section>
{ana_sec}
<section>
<h2>만들면서 고친 것</h2>
<div class="notes">{notes}</div>
</section>
<section>
<h2>보면서 확인할 것</h2>
<div class="checks">{checks}</div>
</section>
<section class="ask"><div class="q"><b>점검 결과를 알려 주세요</b>
괜찮으면 "{int(n)}화 OK", 고칠 게 있으면 "{int(n)}화 07번 콩이가 이상해"처럼 <b>컷 번호 + 이유</b>로 보내 주세요. 다시 만들 컷만 골라서 고칠게요.</div></section>
</div>
<script>function seek(t){{const v=document.getElementById('v');v.currentTime=t;v.play();v.scrollIntoView({{behavior:'smooth',block:'center'}})}}</script>
</body></html>'''
    p = OUT / f"gomgom_ep{n}_review.html"
    p.write_text(html, encoding="utf-8")
    print(p.name, round(p.stat().st_size / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    for n, i in (("04", 3), ("05", 4), ("06", 5)):
        build(n, i)
