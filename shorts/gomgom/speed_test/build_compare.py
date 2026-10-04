# -*- coding: utf-8 -*-
"""2·3화 비교 페이지 (한 파일): 화 선택 → 버전별 영상이 따로 재생됨(하나 틀면 나머지는 자동 멈춤) + 삐약 소리 미리듣기"""
import base64, json, pathlib, subprocess

H = pathlib.Path(__file__).resolve().parent
SRC = H / "out_s"
PEEPS = H.parent / "sound" / "chick_demo.m4a"
VER = [
    ("A_orig", "A", "지금 버전", "1배 · 훅 없음 · 엔딩 급하게 끝남"),
    ("H2_peep_loud", "H2", "지난번 (1.25배)", "간격 짧음 · 삐약(새소리 같았던 것) · 제목 1.8초"),
    ("J_115_gap_mid", "J", "1.15배 · 간격 보통 ⭐", "대사 앞 0.10초 + 뒤 0.30초 · 제목 3초 · 병아리 소리 · 엔딩 여운"),
    ("K_115_gap_wide", "K", "1.15배 · 간격 넉넉", "대사 앞 0.15초 + 뒤 0.45초 · 제목 3초 · 병아리 소리 · 엔딩 여운"),
]


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return round(float(r.stdout.strip()), 1)


def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


secs = []
for ep, title in (("02", "2화 · 칭찬과 지적"), ("03", "3화 · 에피쿠로스")):
    cards = []
    for tag, k, name, desc in VER:
        f = SRC / f"ep{ep}_{tag}.mp4"
        if not f.exists():
            continue
        best = " best" if k == "J" else ""
        cards.append(f'<div class="card{best}"><video controls playsinline preload="metadata" src="{b64(f, "video/mp4")}"></video>'
                     f'<div class="c"><div class="nm"><b>{k}</b> · {name}</div><div class="len">{dur(f)}초</div><div class="soft">{desc}</div></div></div>')
    secs.append(f'<section class="ep" data-ep="{ep}"{"" if ep == "02" else " hidden"}><div class="grid">{"".join(cards)}</div></section>')

html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 병아리·간격 비교</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",system-ui,sans-serif;line-height:1.65;margin:0;padding:24px 12px 60px}}
.wrap{{max-width:860px;margin:0 auto;display:flex;flex-direction:column;gap:20px}}p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:6px}}
h1{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:clamp(23px,6vw,32px);line-height:1.3;margin:0 0 6px}}
h2{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:19px;margin:0 0 8px}}
.soft{{color:var(--soft);font-size:13.5px}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:2}}
.tabs button{{font:inherit;border:1px solid var(--edge);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 16px;cursor:pointer;font-size:14px}}
.tabs button.on{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}
.card.best{{border:2px solid var(--honey)}}
.card video{{width:100%;aspect-ratio:9/16;background:#000;display:block}}
.card .c{{padding:9px 11px 11px;font-size:13px}}.nm{{font-family:"Gowun Dodum",sans-serif;font-size:16px}}
.len{{color:var(--honey);font-weight:700;font-variant-numeric:tabular-nums}}
.peep{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;gap:8px}}
audio{{width:100%}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}}
.q b{{font-family:"Gowun Dodum",sans-serif;font-size:18px;font-weight:400;display:block;margin-bottom:4px}}
</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · 병아리·간격 비교</p><h1>하나씩 틀어서 비교해 보세요</h1>
<p class="soft">영상마다 재생 버튼이 따로 있어요. <b>하나를 틀면 다른 영상은 자동으로 멈춰서</b> 소리가 섞이지 않아요. 소리를 켜고 들어 주세요.</p></section>
<section class="peep"><h2>먼저 병아리 소리만 들어 보기</h2><p class="soft">새로 만든 4가지: 삐약 한 번 → 삐약삐약 → 신나서 삐약삐약삐약 → 병아리 여러 마리(마지막 장면)</p>
<audio controls preload="metadata" src="{b64(PEEPS, 'audio/mp4')}"></audio></section>
<nav class="tabs"><button class="on" data-ep="02">2화 · 칭찬과 지적</button><button data-ep="03">3화 · 에피쿠로스</button></nav>
{"".join(secs)}
<section class="soft">J·K 공통: 말 속도 1.15배 · 첫 목소리 0초 시작 · 0~3초 화면 위쪽 제목 카드 · 병아리 소리 · 마지막 컷 2초 여운 · 지금 배경음악</section>
<section class="q"><b>알려 주세요</b>① 말 사이 간격: J(보통) / K(넉넉) &nbsp; ② 병아리 소리: 좋다 / 빼자 / 더 크게·작게 / 더 자주·덜 자주 &nbsp; ③ 제목 3초: 적당 / 더 길게 / 짧게<br>예) "J로 가자" — 정하면 2~6화에 똑같이 적용할게요(크레딧 0).</section>
</div>
<script>
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x==b));
  document.querySelectorAll('.ep').forEach(s=>s.hidden=s.dataset.ep!=b.dataset.ep);
  document.querySelectorAll('video,audio').forEach(m=>m.pause());
}});
document.querySelectorAll('video,audio').forEach(m=>m.addEventListener('play',()=>{{
  document.querySelectorAll('video,audio').forEach(o=>{{if(o!==m)o.pause()}});
}}));
</script></body></html>"""
p = H / "gomgom_peep_compare.html"
p.write_text(html, encoding="utf-8")
print(p.name, round(p.stat().st_size / 1048576, 1), "MB")
