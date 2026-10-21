# 새 화 그림 확인 페이지: python review456/build_imgs.py 09  → review_site/public/epNNimg/
import json, sys, re, html, pathlib, shutil
from PIL import Image
G = pathlib.Path(__file__).resolve().parent.parent
ep = sys.argv[1]; d = json.load(open(G / f"ep{ep}/lines.json", encoding="utf-8"))
css = re.search(r"<style>(.*?)</style>", (G / "review_site/public/ep07fix1019/index.html").read_text(encoding="utf-8"), re.S).group(1)
out = G / f"review_site/public/ep{ep}img"; out.mkdir(parents=True, exist_ok=True)
flags = json.load(open(G / f"ep{ep}/prod/img_qc.json", encoding="utf-8")) if (G / f"ep{ep}/prod/img_qc.json").exists() else {}
cards = ""
for s in d["shots"]:
    p = G / f"ep{ep}/prod/img/{s['id']}.png"
    if p.exists():
        im = Image.open(p).convert("RGB"); im.thumbnail((360, 640)); im.save(out / f"{s['id']}.jpg", quality=85)
        pic = f'<img src="{s["id"]}.jpg" style="width:100%;border-radius:8px;display:block">'
    else:
        pic = '<div style="aspect-ratio:9/16;background:#eee;border-radius:8px;display:flex;align-items:center;justify-content:center">없음</div>'
    f = flags.get(s["id"], "")
    cls = "c bad" if f.startswith("!") else "c"
    cards += f'<div class="{cls}">{pic}<div class="t"><b>{s["id"]}</b> · {html.escape(s["narrator"])}</div><div class="l">{html.escape(s["plan_img"])}</div>' + (f'<div class="l" style="color:#C0392B">{html.escape(f.lstrip("!"))}</div>' if f else "") + "</div>"
(out / "index.html").write_text(rf"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>곰곰한 마음 · {ep}화 그림 확인</title><style>{css}.c img{{border:3px solid #ddd}}.c.bad img{{border-color:#E57373}}</style></head><body><div class="w"><p class="soft"><a href="../index.html">← 목차</a></p>
<h1>🖼 {ep}화 — {html.escape(d['episode'][3:])} · 그림 확인</h1>
<p class="soft">영상 만들기 전 그림 단계예요. 그림이 영상의 첫 장면이 되고, 여기서 움직임만 더해져요.</p>
<section class="rule"><h2>골라 주실 것</h2><p><b>다시 그릴 컷 번호</b>를 말씀해 주세요. 괜찮으면 "통과"라고만 하셔도 돼요.<br>그다음 영상 단계(약 {(len(d['shots'])-1)*4.8+9.6:.0f}크레딧)로 넘어가기 전에 한 번 더 여쭤요.</p></section>
<section><h2>컷별 그림</h2><div class="row">{cards}</div></section>
<p class="soft">파일: C:\project\youtube\shorts\gomgom\ep{ep}\prod\img\</p></div></body></html>""", encoding="utf-8")
print(out)
