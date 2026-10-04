# -*- coding: utf-8 -*-
"""실제 녹음 효과음 후보(Pixabay 24개) 미리듣기 + K 간격 루프 샘플 비교 페이지 (파일 하나)"""
import base64, json, pathlib, subprocess

H = pathlib.Path(__file__).resolve().parent
SND = H.parent / "sound"
CAT = [("footsteps", "발걸음 (카펫·양말)", "곰곰이가 걸어갈 때"), ("door", "문 여는 소리", "집·우편함·창문"),
       ("rain", "가벼운 빗소리", "비·구름 장면"), ("teacup", "찻잔·숟가락", "차 마시는 장면"),
       ("wind", "바람·나뭇잎", "바깥 장면 배경"), ("page", "책장 넘김", "편지·책·생각 장면"),
       ("sparkle", "반짝임", "깨달음·마무리"), ("pop", "뽁 소리", "콩이가 튀어나올 때")]


def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def preview(src, dst):
    """앞 무음 자르고 최대 6초, 음량 맞춤"""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:6,afade=t=out:st=5.5:d=0.5,loudnorm=I=-18:TP=-2",
                    "-ac", "1", "-b:a", "80k", str(dst)], check=True)
    return dst


cand = json.loads(open(SND / "pixabay_candidates.json", encoding="utf-8").read())
if isinstance(cand, str):
    cand = json.loads(cand)
pv = SND / "real_preview"; pv.mkdir(exist_ok=True)
sfx_html = []
for key, name, use in CAT:
    rows = []
    for i, c in enumerate(cand[key], 1):
        f = preview(SND / "real" / f"{key}{i}.mp3", pv / f"{key}{i}.mp3")
        title = c["title"].split(" by ")[0].strip()
        rows.append(f'<div class="snd"><div class="lab"><b>{key}{i}</b> <span class="soft">{title}</span></div>'
                    f'<audio controls preload="none" src="{b64(f, "audio/mpeg")}"></audio></div>')
    sfx_html.append(f'<div class="cat"><h3>{name} <span class="soft">· {use}</span></h3>{"".join(rows)}</div>')

vids = []
for ep, t in (("02", "2화"), ("03", "3화")):
    for tag, lab, desc in (("L_115_K_loop", "새 버전 · 루프 처리 ⭐", "검은 화면 없음 · 음악이 끊기지 않고 처음 크기로 끝남 · 여운 1.2초"),
                           ("K_115_gap_wide", "지난번 K", "끝에서 화면이 어두워지고 음악이 0으로 줄어듦 · 여운 2초")):
        f = H / "out" / f"ep{ep}_{tag}.mp4"
        small = H / "out_s" / f.name
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "31",
                        "-c:a", "aac", "-b:a", "80k", "-movflags", "+faststart", str(small)], check=True)
        best = " best" if tag.startswith("L_") else ""
        vids.append(f'<div class="card{best}"><video controls loop playsinline preload="metadata" src="{b64(small, "video/mp4")}"></video>'
                    f'<div class="c"><div class="nm">{t} · {lab}</div><div class="soft">{desc}</div></div></div>')

html = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>곰곰한 마음 효과음 후보·루프 확인</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
:root{{--bg:#FBF6EE;--card:#FFFDF9;--edge:#EADFCF;--ink:#3A2F25;--soft:#85766A;--honey:#D98E2B}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1C1712;--card:#26201A;--edge:#3D342A;--ink:#F3E9DC;--soft:#B5A594;--honey:#EDAA4E}}}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",system-ui,sans-serif;line-height:1.65;margin:0;padding:24px 12px 60px}}
.wrap{{max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:22px}}p{{margin:0}}
.eye{{font-size:12px;letter-spacing:.16em;color:var(--honey);font-weight:700;margin-bottom:6px}}
h1{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:clamp(23px,6vw,32px);line-height:1.3;margin:0 0 6px}}
h2{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:21px;margin:0 0 6px}}
h3{{font-family:"Gowun Dodum",sans-serif;font-weight:400;font-size:17px;margin:0 0 8px}}
.soft{{color:var(--soft);font-size:13px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--edge);border-radius:16px;overflow:hidden}}.card.best{{border:2px solid var(--honey)}}
.card video{{width:100%;aspect-ratio:9/16;background:#000;display:block}}.card .c{{padding:9px 11px 11px;font-size:13px}}
.nm{{font-family:"Gowun Dodum",sans-serif;font-size:16px}}
.cats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px}}
.cat{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:12px 14px}}
.snd{{margin-bottom:8px}}.lab{{font-size:13px;margin-bottom:2px}}.lab b{{color:var(--honey)}}audio{{width:100%;height:36px}}
.q{{background:var(--card);border:1px solid var(--edge);border-radius:14px;padding:14px 16px;font-size:14.5px}}
.q b.t{{font-family:"Gowun Dodum",sans-serif;font-size:18px;font-weight:400;display:block;margin-bottom:4px}}
</style></head><body><div class="wrap">
<section><p class="eye">곰곰한 마음 · 효과음 후보 + 루프 확인</p><h1>실제 녹음 효과음 고르기 · 반복 재생 확인</h1>
<p class="soft">하나를 틀면 다른 소리는 자동으로 멈춰요. 소리를 켜고 들어 주세요.</p></section>

<section><h2>① 반복 재생(루프) 확인</h2>
<p class="soft">영상이 끝나면 쇼츠처럼 <b>자동으로 처음부터 다시</b> 나와요. 끝 → 처음으로 넘어가는 순간을 봐 주세요. 말 사이 간격 K · 1.15배 · 제목 카드 3초 · 효과음 없음.</p>
<div class="grid" style="margin-top:10px">{"".join(vids)}</div></section>

<section><h2>② 실제 녹음 효과음 후보 24개</h2>
<p class="soft">Pixabay의 무료 효과음이에요(상업적 사용 가능, 출처 표기 필요 없음, 크레딧 0). AI로 만든 소리가 아니라 실제로 녹음한 소리예요. 미리듣기는 앞 6초만 잘랐고 음량을 맞췄어요.</p>
<div class="cats" style="margin-top:10px">{"".join(sfx_html)}</div></section>

<section class="q"><b class="t">알려 주세요</b>① 루프: 새 버전이 자연스러운지<br>② 효과음: 마음에 드는 번호만 골라 주세요 — 예) "teacup2, sparkle2, rain3 좋아. 나머지 빼"<br>고른 소리만 장면에 맞춰 넣어서 다시 보여 드릴게요.</section>
</div>
<script>document.querySelectorAll('video,audio').forEach(m=>m.addEventListener('play',()=>{{document.querySelectorAll('video,audio').forEach(o=>{{if(o!==m)o.pause()}})}}));</script>
</body></html>"""
p = H / "gomgom_sfx_loop_review.html"
p.write_text(html, encoding="utf-8")
print(p, round(p.stat().st_size / 1048576, 1), "MB")
