# -*- coding: utf-8 -*-
"""2·3화 비교 페이지 (한 파일): 화 선택 → 왼쪽/오른쪽 버전 선택 → 나란히 동시 재생, 소리는 한쪽씩"""
import base64, json, pathlib, subprocess

H = pathlib.Path(__file__).resolve().parent
SRC = H / "out_s"
VER = [
    ("A_orig", "A", "지금 버전", "1배 · 훅 없음 · 엔딩 급하게 끝남"),
    ("C_125", "C", "1.25배 (지난번)", "훅 · 엔딩 급하게 끝남"),
    ("C2_end", "C2", "1.25배 + 엔딩 여운 ⭐", "마지막 컷 2초 더 + 음악 살짝 커졌다가 천천히 페이드"),
    ("E_125_sfx", "E", "1.25배 + 예전 효과음", "반짝·폴짝·풍경 등 (지난번)"),
    ("H_peep_end", "H", "1.25배 + 삐약 + 엔딩 여운 ⭐", "콩이 움직일 때 삐약·삐약삐약·궁금한 삐약 등"),
]


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return round(float(r.stdout.strip()), 1)


data = {}
for ep in ("02", "03"):
    data[ep] = {}
    for tag, k, name, desc in VER:
        f = SRC / f"ep{ep}_{tag}.mp4"
        data[ep][k] = {"src": "data:video/mp4;base64," + base64.b64encode(f.read_bytes()).decode(),
                       "name": name, "desc": desc, "len": dur(f)}
meta = {k: {"name": n, "desc": d} for _, k, n, d in VER}

html = """<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 말 속도 비교</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B;--sage:#5E8A4E}
@media (prefers-color-scheme:dark){:root{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E;--sage:#9BC487}}
*{box-sizing:border-box}body{background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",system-ui,sans-serif;line-height:1.65;margin:0;padding:24px 12px 60px}
.wrap{max-width:860px;margin:0 auto;display:flex;flex-direction:column;gap:20px}p{margin:0}
.eye{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:6px}
h1{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:clamp(23px,6vw,32px);line-height:1.3;margin:0 0 6px}
h2{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:19px;margin:0 0 8px}
.soft{color:var(--soft);font-size:13.5px}
.seg{display:flex;gap:6px;flex-wrap:wrap}
.seg button,.pick button{font:inherit;border:1px solid var(--edge);background:var(--card);color:var(--ink);border-radius:999px;padding:6px 14px;cursor:pointer;font-size:14px}
.seg button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.side{background:var(--card);border:1px solid var(--edge);border-radius:16px;padding:10px;display:flex;flex-direction:column;gap:8px}
.side.loud{border:2px solid var(--honey)}
.pick{display:flex;gap:4px;flex-wrap:wrap}
.pick button{padding:4px 10px;font-size:13px;min-width:34px}
.pick button.on{background:var(--honey);color:#fff;border-color:var(--honey)}
video{width:100%;aspect-ratio:9/16;background:#000;border-radius:12px;display:block}
.nm{font-family:"Gowun Dodum",sans-serif;font-size:16px}.len{color:var(--honey);font-weight:700;font-variant-numeric:tabular-nums}
.ctl{display:flex;gap:8px;flex-wrap:wrap}
.ctl button{font:inherit;border:0;border-radius:12px;padding:10px 14px;background:var(--ink);color:var(--bg);cursor:pointer;font-size:14px;flex:1;min-width:120px}
.ctl button.alt{background:var(--card);color:var(--ink);border:1px solid var(--edge)}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{border-bottom:1px solid var(--edge);padding:6px 5px;text-align:left;vertical-align:top}
th{color:var(--soft);font-weight:500;font-size:12px}td b{color:var(--honey)}
.q{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}
.q b{font-family:"Gowun Dodum",sans-serif;font-size:18px;font-weight:400;display:block;margin-bottom:4px}
</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · 말 속도 비교</p><h1>삐약 효과음 · 엔딩 여운 비교</h1>
<p class="soft">위에서 화를 고르고, 왼쪽·오른쪽 버전을 고른 뒤 <b>같이 재생</b>을 누르세요. 소리는 한쪽만 나와요 — <b>소리 바꾸기</b>로 왼쪽/오른쪽을 오가며 들어 보세요.</p></section>
<section class="seg" id="eps"><button data-ep="02" class="on">2화 · 칭찬과 지적</button><button data-ep="03">3화 · 에피쿠로스</button></section>
<section class="duo">
 <div class="side loud" id="sL"><div class="pick" id="pL"></div><video id="vL" playsinline preload="metadata"></video><div><div class="nm" id="nL"></div><div class="len" id="lL"></div><div class="soft" id="dL"></div></div></div>
 <div class="side" id="sR"><div class="pick" id="pR"></div><video id="vR" playsinline preload="metadata" muted></video><div><div class="nm" id="nR"></div><div class="len" id="lR"></div><div class="soft" id="dR"></div></div></div>
</section>
<section class="ctl"><button id="play">▶ 같이 재생</button><button id="swap" class="alt">🔊 소리 바꾸기 (지금: 왼쪽)</button><button id="re" class="alt">⏮ 처음부터</button></section>
<section><h2>버전 설명</h2><table><tr><th></th><th>내용</th></tr>__ROWS__</table>
<p class="soft" style="margin-top:8px">C 이후 공통: 1.25배(고정) · 컷 사이 빈 시간 줄임 · 첫 목소리 0초 시작 · 0~1.8초 화면 위쪽 큰 제목 카드(훅) · 배경음악은 지금 것</p></section>
<section class="q"><b>골라 주세요</b>① 엔딩: 여운 넣은 C2가 나은지 &nbsp; ② 삐약 효과음(H): 좋다 / 빼자 / 더 크게·작게 / 더 자주·덜<br>예) "H로 가자" 또는 "삐약은 좋은데 좀 더 작게" — 정하면 2~6화에 똑같이 적용할게요(크레딧 0).</section>
</div>
<script>
const D=__DATA__, K=__KEYS__;
let ep="02", L="C2", R="H", loud="L";
const $=id=>document.getElementById(id);
function picks(side){const p=$("p"+side);p.innerHTML="";K.forEach(k=>{const b=document.createElement("button");b.textContent=k;
 if((side=="L"?L:R)==k)b.className="on";b.onclick=()=>{if(side=="L")L=k;else R=k;load(side)};p.appendChild(b)})}
function load(side){const k=side=="L"?L:R,v=D[ep][k];$("v"+side).src=v.src;$("n"+side).textContent=k+" · "+v.name;
 $("l"+side).textContent=v.len+"초";$("d"+side).textContent=v.desc;picks(side)}
function mute(){$("vL").muted=loud!="L";$("vR").muted=loud!="R";$("sL").classList.toggle("loud",loud=="L");$("sR").classList.toggle("loud",loud=="R");
 $("swap").textContent="🔊 소리 바꾸기 (지금: "+(loud=="L"?"왼쪽":"오른쪽")+")"}
document.querySelectorAll("#eps button").forEach(b=>b.onclick=()=>{ep=b.dataset.ep;document.querySelectorAll("#eps button").forEach(x=>x.classList.toggle("on",x==b));load("L");load("R")});
$("play").onclick=()=>{const a=$("vL"),b=$("vR");if(a.paused){a.play();b.play();$("play").textContent="⏸ 같이 멈춤"}else{a.pause();b.pause();$("play").textContent="▶ 같이 재생"}};
$("re").onclick=()=>{["vL","vR"].forEach(i=>{$(i).currentTime=0});};
$("swap").onclick=()=>{loud=loud=="L"?"R":"L";mute()};
load("L");load("R");mute();
</script></body></html>"""
rows = "".join(f'<tr><td><b>{k}</b></td><td>{m["name"]} — {m["desc"]}</td></tr>' for k, m in meta.items())
html = html.replace("__ROWS__", rows).replace("__KEYS__", json.dumps([v[1] for v in VER])).replace("__DATA__", json.dumps(data, ensure_ascii=False))
p = H / "gomgom_speed_compare.html"
p.write_text(html, encoding="utf-8")
print(p.name, round(p.stat().st_size / 1048576, 1), "MB")
