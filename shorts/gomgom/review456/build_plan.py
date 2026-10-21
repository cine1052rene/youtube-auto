# 새 화 대본·장면 계획 확인 페이지 생성기: python review456/build_plan.py 09
import json, sys, re, html, pathlib
G = pathlib.Path(__file__).resolve().parent.parent
ep = sys.argv[1]; d = json.load(open(G / f"ep{ep}/lines.json", encoding="utf-8"))
css = re.search(r"<style>(.*?)</style>", (G / "review_site/public/ep07fix1019/index.html").read_text(encoding="utf-8"), re.S).group(1)
n = lambda s: len(re.sub(r"\s", "", s))
tot = sum(n(s["narrator"]) for s in d["shots"]); sec = 0.2 * tot + 3.7 - 0.6 * (12 - len(d["shots"]))  # 4~8화 실측 맞춤(161자 35.9초 · 222자 47.9초)
rows = "".join(f"<tr><td><b>{s['id']}</b></td><td>{html.escape(s['narrator'])}</td><td>{html.escape(s['plan_img'])}</td><td>{html.escape(s['plan_mov'])}</td><td class='soft'>{html.escape(s.get('plan_note',''))}</td></tr>" for s in d["shots"])
nimg = len(d["shots"]); vid = (nimg - 1) * 4.8 + 9.6
out = G / f"review_site/public/ep{ep}plan"; out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(rf"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>곰곰한 마음 · {ep}화 대본·장면 계획</title><style>{css}
.tb{{overflow-x:auto}}table{{border-collapse:collapse;font-size:13px;min-width:760px;width:100%}}td,th{{border-top:1px solid #EADFCF;padding:5px;vertical-align:top;text-align:left}}th{{font-size:12px;color:#85766A}}td:nth-child(1){{width:28px}}td:nth-child(2){{width:22%}}td:nth-child(5){{width:13%}}</style></head><body><div class="w"><p class="soft"><a href="../index.html">← 목차</a></p>
<h1>📝 {ep}화 — {html.escape(d['episode'][3:])} · 대본·장면 계획</h1>
<p class="soft">아직 아무것도 만들지 않았어요(크레딧 0). 대본 {tot}자 · {nimg}컷 · 예상 약 {sec:.0f}초 (실측: 4화 161자 35.9초 · 6화 169자 37.5초 / 7·8화 222자 47.9초는 늘어졌음)</p>
<section class="rule"><h2>골라 주실 것</h2>
<p><b>1. 대본·장면 이대로 괜찮을까요?</b> 고칠 줄이 있으면 번호로 말씀해 주세요.</p>
<p><b>2. 다음 단계(그림 {nimg}장 + 내레이션 {nimg}줄) 진행해도 될까요?</b> 약 {nimg + 4}~{nimg + 8}크레딧(다시 뽑기 포함). 그림이 나오면 영상 전에 컷별 그림 페이지로 먼저 보여드려요.</p>
<p class="soft">참고: 영상 단계는 그림 승인 후 따로 여쭤요(약 {vid:.0f}크레딧 + 대사가 긴 컷 나눔용 2~3개).</p></section>
<section><h2>근거</h2><p class="l">{html.escape(d['note'])}</p></section>
<section><h2>컷별 계획</h2><div class="tb"><table><tr><th>#</th><th>내레이션</th><th>그림</th><th>움직임</th><th>메모</th></tr>{rows}</table></div></section>
<p class="soft">파일: C:\project\youtube\shorts\gomgom\ep{ep}\lines.json</p></div></body></html>""", encoding="utf-8")
print(out, tot, round(sec))
