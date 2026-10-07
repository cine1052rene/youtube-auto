# -*- coding: utf-8 -*-
"""시즌1 마스터 6편 확인 페이지 (하나 틀면 나머지 멈춤, 루프 재생)"""
import base64, pathlib, subprocess, json

H = pathlib.Path(__file__).resolve().parent
G = H.parent
EPS_S1 = [("01", "쉬어도 피곤한 이유", "ep01/v3/out"), ("02", "칭찬과 지적", "ep02/prod/out"), ("03", "에피쿠로스의 작은 행복", "ep03/prod/out"),
       ("04", "비교", "ep04/prod/out"), ("05", "걱정 내려놓기", "ep05/prod/out"), ("06", "서운함", "ep06/prod/out")]
import sys
EPS = EPS_S1 if len(sys.argv) < 2 else [("07", "계획은 늘 오래 걸려요 (시즌2-1)", "ep07/prod/out"), ("08", "남들은 나를 안 봐요 (시즌2-2)", "ep08/prod/out"),
       ("d01", "파생: 댓글 답장 · 스트레칭", "epd01/prod/out"), ("d02", "파생: 콩이의 작은 반짝임", "epd02/prod/out")]
SUF = "_master_s1" if len(sys.argv) < 2 else "_master"
PAGE = "gomgom_season1_masters.html" if len(sys.argv) < 2 else "gomgom_ep07_08_derived.html"


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


cards = ""
for ep, name, d in EPS:
    f = G / d / f"ep{ep}{SUF}.mp4"
    s = H / "out_s" / f"ep{ep}{SUF}_prev.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "30",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(s)], check=True)
    b = base64.b64encode(s.read_bytes()).decode()
    cards += (f'<div class="card"><video controls loop playsinline preload="metadata" src="data:video/mp4;base64,{b}"></video>'
              f'<div class="c"><div class="nm">{name}</div><div class="len">{dur(f):.1f}초</div>'
              f'<div class="path">C:\\project\\youtube\\shorts\\gomgom\\{d.replace("/", chr(92))}\\ep{ep}{SUF}.mp4</div></div></div>')

html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 시즌1 마스터 확인</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",system-ui,sans-serif;line-height:1.6;margin:0;padding:24px 12px 60px}}
.wrap{{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:20px}}p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:6px}}
h1{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:clamp(23px,5vw,32px);margin:0 0 6px}}
.soft{{color:var(--soft);font-size:13.5px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}
.card video{{width:100%;aspect-ratio:9/16;background:#000;display:block}}.c{{padding:9px 11px 11px}}
.nm{{font-family:"Gowun Dodum",sans-serif;font-size:16px}}.len{{color:var(--honey);font-weight:700}}
.path{{font-size:10.5px;color:var(--soft);word-break:break-all;margin-top:4px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}}
</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · 시즌1 마스터</p><h1>1~6화 마스터 파일</h1>
<p class="soft">모든 화 공통: 말 속도 1.15배 · 말 사이 간격(앞 0.15초/뒤 0.45초) · 처음 3초 제목 카드 · 끝나면 자연스럽게 처음으로 이어지는 루프 처리 · 효과음 없음 · 1080×1920.
여기 영상은 미리보기 화질이고, 업로드용 원본은 카드 아래 경로에 있어요. 하나를 틀면 나머지는 멈춰요.</p></section>
<div class="grid">{cards}</div>
<section class="q"><b>확인해 주세요</b> — 제목 카드 문구(특히 1·4·5·6화는 커버 제목을 썼어요), 말 속도, 끝→처음 이어짐. 고칠 화와 내용을 알려 주시면 그 화만 다시 만들게요.</section>
</div>
<script>document.querySelectorAll('video').forEach(m=>m.addEventListener('play',()=>{{document.querySelectorAll('video').forEach(o=>{{if(o!==m)o.pause()}})}}));</script>
</body></html>"""
p = H / PAGE
p.write_text(html, encoding="utf-8")
print(p, round(p.stat().st_size / 1048576, 1), "MB")
