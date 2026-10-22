# 새 화 컷별 점검 페이지(사이트 호스팅): python review456/build_epcuts.py 09  → review_site/public/epNNcuts/
import json, sys, re, html, pathlib, subprocess, shutil
from PIL import Image
G = pathlib.Path(__file__).resolve().parent.parent
ep = sys.argv[1]; d = json.load(open(G / f"ep{ep}/lines.json", encoding="utf-8"))
css = re.search(r"<style>(.*?)</style>", (G / "review_site/public/ep07fix1019/index.html").read_text(encoding="utf-8"), re.S).group(1)
out = G / f"review_site/public/ep{ep}cuts"; out.mkdir(parents=True, exist_ok=True)
master = G / f"ep{ep}/prod/out/ep{ep}_master.mp4"
sh = lambda c: subprocess.run(c, capture_output=True, text=True)
dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(master)]).stdout)
sh(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "25", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", str(out / "master.mp4")])
sh(["ffmpeg", "-v", "error", "-y", "-ss", "5", "-i", str(master), "-frames:v", "1", "-vf", "scale=360:640", str(out / "master.jpg")])
notes = json.load(open(G / f"ep{ep}/prod/cut_notes.json", encoding="utf-8")) if (G / f"ep{ep}/prod/cut_notes.json").exists() else {}
cards = ""
for s in d["shots"]:
    cl = G / f"ep{ep}/prod/clips/{s['id']}.mp4"
    if not cl.exists(): continue
    mp = out / f"{s['id']}.mp4"
    sh(["ffmpeg", "-v", "error", "-y", "-i", str(cl), "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "27", "-preset", "fast", "-an", str(mp)])
    sh(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(cl), "-frames:v", "1", "-vf", "scale=360:640", str(out / f"{s['id']}.jpg")])
    n = notes.get(s["id"], "")
    cards += f'<div class="c{" bad" if n.startswith("!") else ""}"><video src="{s["id"]}.mp4" poster="{s["id"]}.jpg" controls playsinline preload="metadata" loop></video><div class="t"><b>{s["id"]}</b> · {html.escape(s["narrator"])}</div>' + (f'<div class="l">{html.escape(n.lstrip("!"))}</div>' if n else "") + "</div>"
(out / "index.html").write_text(rf"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>곰곰한 마음 · {ep}화 컷별 점검</title><style>{css}</style></head><body><div class="w"><p class="soft"><a href="../index.html">← 목차</a></p>
<h1>🎬 {ep}화 — {html.escape(d['episode'][3:])} · 컷별 점검</h1>
<p class="soft">완성본 {dur:.1f}초 · {len(d['shots'])}컷 · 1.15배 · 제목 카드 3초 · 루프 · 효과음 없음 (공개 제안: {"금 10/30 20:00" if ep=="09" else "화 11/3 20:00"})</p>
<section class="rule"><h2>골라 주실 것</h2><p>고칠 컷이 있으면 <b>화·컷 번호와 이유</b>로 말씀해 주세요. 괜찮으면 "{ep}화 OK"라고만 하셔도 돼요. OK를 주시면 유튜브 예약 업로드를 진행해요.</p></section>
<section><h2>완성본</h2><div class="row"><div class="c now"><video src="master.mp4" poster="master.jpg" controls playsinline preload="metadata" loop></video><div class="t"><b>{ep}화 완성본</b> · {dur:.1f}초</div></div></div></section>
<section><h2>컷별 영상</h2><div class="row">{cards}</div></section>
<p class="soft">파일: C:\project\youtube\shorts\gomgom\ep{ep}\prod\out\ep{ep}_master.mp4</p></div><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{{if(o!==v)o.pause()}})));</script></body></html>""", encoding="utf-8")
print(out, round(dur, 1))
