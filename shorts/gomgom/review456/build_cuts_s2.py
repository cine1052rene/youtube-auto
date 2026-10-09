# -*- coding: utf-8 -*-
"""7·8화·파생 2편 — 화별 컷 점검 페이지(4화 페이지와 같은 형식). 한 화 = 한 페이지.
사용: python build_cuts_s2.py [07 08 d01 d02]"""
import base64, json, subprocess, sys
from build import G, OUT, CSS, CHECKS, frame_b64

SPEED, LEAD, TAIL, MIN_D, END, FPS = 1.15, 0.15, 0.45, 1.5, 1.2, 30
HOOK = 0.0  # 제목 카드는 첫 컷 위에 겹침(4화 페이지와 같은 계산)

EPS = {
    "07": {"title": "왜 늘 계획보다 오래 걸릴까?", "sub": "계획 오류 (Kahneman & Tversky, 1979)", "when": "미정 (제안: 금 10/23 20:00)", "label": "시즌2 · 7화",
           "made": [("10/10 콩이 크기 통일", "콩이 크기 기준을 <b>곰곰이 머리 폭의 1/3</b>로 정해 기준 사진을 새로 만들고, <b>01·03·08·12</b>를 다시 만들었어요. 02·07·10·11은 일단 그대로예요."),
                    ("10/9 다시 만든 것", "<b>02·08·12</b> 영상을 새 기준 사진(콩이를 작게 그린 사진)으로 다시 만들었어요. 08은 카메라를 곰곰이 쪽으로만 움직여 곰곰이가 둘이 되지 않게, 12는 카메라가 뒤에서만 올라가 뒤통수에 얼굴이 생기지 않게 했어요. 내레이션 <b>04·06</b>도 다시 녹음했어요."),
                    ("시즌2 기준 이미지", "곰곰이 가슴 배지가 하트 → <b>노란 별</b>로 바뀌었어요. 뒷모습 컷엔 배지가 안 보이게 지정했어요."),
                    ("다시 만든 컷", "<b>06번</b>은 벽돌이 곰곰이 머리 위에 붙어 나와서, <b>10번</b>은 콩이가 사라지고 달력에 숫자가 생겨서 다시 만들었어요(옆에서 보는 앵글·빈 달력)."),
                    ("길이", "내레이션이 46초라 영상이 48초예요. 1~6화(34~44초)보다 조금 길어요.")]},
    "08": {"title": "다들 나만 보는 것 같을 때", "sub": "스포트라이트 효과 (Gilovich 외, 2000) — 티셔츠 실험", "when": "미정 (제안: 화 10/27 20:00)", "label": "시즌2 · 8화",
           "made": [("10/10 다시 만든 것", "<b>06</b> 티셔츠 토끼가 친구들의 2배로 커지던 것 → 같은 키, 티셔츠도 07처럼 무늬 없는 노랑. <b>10</b> 입이 두 개로 보이던 것 → 눈 감고 입 다문 미소."),
                    ("10/9 다시 만든 것", "<b>07</b>(티셔츠 토끼가 끝까지 화면에), <b>08</b>(관객석에 실사 사람 → 전부 펠트 동물), <b>10</b>(콩이를 작게) 영상을 새 기준 사진으로 다시 만들었어요. 내레이션 <b>02·05·11</b>도 다시 녹음했어요."),
                    ("근거 실험", "눈에 띄는 티셔츠를 입은 학생이 '절반은 알아챘을 것'이라 예상했지만 실제로는 4명 중 1명 정도였다는 실험이에요."),
                    
                    ("길이", "48초로 7화와 비슷해요.")]},
    "d01": {"title": "댓글 답장 — 쉴 때 스트레칭", "sub": "1화 댓글(@SollaMusic_lu) 답장 · 파생 쇼츠", "when": "미정 (제안: 토 10/10 11:00)", "label": "파생 1",
            "made": [("10/9 점검 결과", "내레이션 받아쓰기·영상 프레임 끝까지 확인 — <b>문제 없음</b>."),
                     ("새로 만든 컷 2개 + 새 내레이션", "1화 장면을 잘라 쓰지 않고 스트레칭하는 곰곰이·콩이 컷을 새로 만들었어요."),
                     ("1화로 연결", "업로드할 때 관련 동영상을 1화로 걸어요.")]},
    "d02": {"title": "콩이의 작은 반짝임", "sub": "콩이 미니 장면 · 3화(작은 행복)와 연결", "when": "미정 (제안: 토 10/17 11:00)", "label": "파생 2",
            "made": [("10/9 점검 결과 — 고칠 것", "<b>02번</b> 카메라가 다가가면서 콩이가 곰곰이 머리만큼 커져요(예전 기준 사진으로 만든 컷). 내레이션 02번 '그것만으로도'가 흐리게 들릴 수 있어요. 직접 들어보고 알려 주세요."),
                     ("새로 만든 컷 2개 + 새 내레이션", "아침 이슬방울을 발견한 콩이 이야기예요."),
                     ("3화로 연결", "업로드할 때 관련 동영상을 3화로 걸어요.")]},
}


NEW = {("07", "02"): "10/9 새로 · 콩이 작게", ("07", "08"): "10/10 새로 · 콩이 1/3 크기", ("07", "12"): "10/10 새로 · 콩이 1/3 크기·어깨 위",
       ("07", "01"): "10/10 새로 · 콩이 1/3 크기", ("07", "03"): "10/10 새로 · 콩이 1/3 크기",
       ("07", "04"): "10/9 내레이션 다시", ("07", "06"): "10/9 내레이션 다시", ("08", "07"): "10/9 새로 · 티셔츠 토끼 유지",
       ("08", "08"): "10/9 새로 · 관객 전부 펠트", ("08", "10"): "10/10 새로 · 입 하나(다문 미소)", ("08", "06"): "10/10 새로 · 토끼 크기 맞춤", ("08", "02"): "10/9 내레이션 다시",
       ("08", "05"): "10/9 내레이션 다시", ("08", "11"): "10/9 내레이션 다시"}


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def plan(n):
    shots = json.load(open(G / f"ep{n}" / "lines.json", encoding="utf-8"))["shots"]
    t, out = HOOK, []
    for i, s in enumerate(shots):
        lead = 0.0 if i == 0 else LEAD
        d = max(lead + dur(G / f"ep{n}" / "audio" / "luna" / f"{s['id']}.mp3") / SPEED + TAIL, MIN_D) + (END if i == len(shots) - 1 else 0)
        d = round(d * FPS) / FPS
        out.append({"id": s["id"], "text": s["narrator"], "start": t, "dur": d})
        t += d
    return out


def build(n):
    e = EPS[n]
    master = G / f"ep{n}" / "prod" / "out" / f"ep{n}_master.mp4"
    prev = G / "speed_test" / "out_s" / f"ep{n}_master_prev.mp4"
    real = dur(master)
    cuts = plan(n)
    if cuts[-1]["start"] + cuts[-1]["dur"] - real > 1.0:  # 제목 카드가 컷 위에 겹치는 구조면 시작을 0으로
        cuts = [dict(c, start=c["start"] - HOOK) for c in cuts]
    vid = base64.b64encode(prev.read_bytes()).decode()
    cards = []
    for s in cuts:
        img = frame_b64(master, min(s["start"] + s["dur"] * 0.55, real - 0.2))
        cards.append(
            f'<div class="cut"><img src="data:image/jpeg;base64,{img}" onclick="seek({s["start"]:.2f})" alt="{s["id"]}번 장면">'
            f'<div class="c"><div class="n">{s["id"]}</div><div>{s["text"]}</div>'
            f'<div class="t">{s["start"]:.1f}초 ~ {s["start"] + s["dur"]:.1f}초</div>'
            f'<div class="md">그림 Seedream 5 Lite<br>영상 Seedance 1.5' + (f'<br><span class="rg">{NEW[(n, s["id"])]}</span>' if (n, s["id"]) in NEW else '') + '</div></div></div>')
    notes = "".join(f'<div class="note"><b class="h">{h}</b><p>{b}</p></div>' for h, b in e["made"])
    checks = "".join(f'<div class="chk">{c}</div>' for c in CHECKS + ["자막이 화면 아래 메뉴(채널명·제목)에 가리지 않는지"])
    path = str(master).replace("/", "\\")
    html = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 {e["label"]} 컷별 점검</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<section>
<p class="eye">곰곰한 마음 · {e["label"]} · 컷별 점검</p>
<h1>{e["title"]}</h1>
<p class="soft">{e["sub"]}</p>
<div class="meta"><span class="pill">공개 {e["when"]}</span><span class="pill">{real:.1f}초</span><span class="pill">{len(cuts)}컷</span>
<span class="pill">1.15배 · 간격 K · 제목 카드 3초 · 루프 · 자막 위치 수정본</span></div>
<p class="soft" style="margin-top:10px;font-size:12px">원본: {path}</p>
</section>
<section class="stage"><video id="v" src="data:video/mp4;base64,{vid}" controls loop playsinline preload="metadata"></video></section>
<section>
<h2>컷별 장면</h2>
<p class="soft" style="margin-bottom:12px">사진을 누르면 영상이 그 장면으로 이동해요. 고치고 싶은 컷은 <b>번호</b>로 알려 주세요.</p>
<div class="cuts">{"".join(cards)}</div>
</section>
<section><h2>만들면서 고친 것</h2><div class="notes">{notes}</div></section>
<section><h2>보면서 확인할 것</h2><div class="checks">{checks}</div></section>
<section class="ask"><div class="q"><b>점검 결과를 알려 주세요</b>
괜찮으면 "{e["label"]} OK", 고칠 게 있으면 "{e["label"]} 05번 콩이가 이상해"처럼 <b>컷 번호 + 이유</b>로 보내 주세요.</div></section>
</div>
<script>function seek(t){{const v=document.getElementById('v');v.currentTime=t;v.play();v.scrollIntoView({{behavior:'smooth',block:'center'}})}}</script>
</body></html>'''
    p = OUT / f"gomgom_ep{n}_master_cuts.html"
    p.write_text(html, encoding="utf-8")
    print(p, f"{real:.1f}s", round(p.stat().st_size / 1048576, 1), "MB")


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["07", "08", "d01", "d02"]):
        build(n)
