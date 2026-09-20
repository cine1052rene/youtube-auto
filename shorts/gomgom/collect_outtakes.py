# -*- coding: utf-8 -*-
"""
안 쓴 컷 모으기 — outtakes/ng(사고 난 컷) · outtakes/alt(멀쩡한데 안 쓴 컷)
원본은 각 화 폴더에 그대로 두고 복사본을 모은다. MANIFEST.md와 확인용 프레임 격자도 만든다.

사용: python collect_outtakes.py
"""
import pathlib, shutil, subprocess, json
from PIL import Image, ImageDraw, ImageFont

H = pathlib.Path(__file__).parent
OUT = H / "outtakes"
FONT = H / "fonts" / "GowunDodum-Regular.ttf"

# (분류, 원본경로, 저장이름, 화, 컷, 무슨 일이 있었는지)
ITEMS = [
    # ── NG: 캐릭터가 무너진 컷 ──────────────────────────────
    ("ng", "ep02/prod/clips/13_wan0915.mp4", "ep02_13_만화곰으로변신.mp4", "2화", "13",
     "곰곰이가 고개를 돌리는 순간 눈썹 달린 하얀 만화 곰으로 바뀜. Wan 모델이 얼굴이 보이면 캐릭터를 갈아치우는 대표 사례"),
    ("ng", "ep04/prod/clips/13_size_old.mp4", "ep04_13_곰곰이가날아감.mp4", "4화", "13",
     "콩이만 날아야 하는데 곰곰이가 입을 벌린 채 하늘로 날아오름. 크기만 고치려던 재생성에서 캐릭터가 통째로 뒤바뀐 사고"),
    ("ng", "ep01/v3/clips/05_old.mp4", "ep01_05_공중에서형태붕괴.mp4", "1화", "05",
     "곰곰이가 떠오르다 뒤집히면서 몸 형태가 무너짐"),
    ("ng", "ep01/v3/clips/13_flyB.mp4", "ep01_13_하늘로사라짐.mp4", "1화", "13",
     "마무리 컷에서 곰곰이가 그대로 하늘로 날아가 버림"),
    ("ng", "ep01/v3/clips/13_old.mp4", "ep01_13_얼굴초근접웃음.mp4", "1화", "13",
     "얼굴이 화면 가득 다가오며 입을 크게 벌림. 아이들이 무서워할 정도"),
    ("ng", "ep01/v3/clips/10_old.mp4", "ep01_10_입벌리면딴곰.mp4", "1화", "10",
     "4초부터 입을 벌리는데 얼굴 비율이 달라져 다른 곰처럼 보임"),
    ("ng", "ep01/v3/clips/04_old.mp4", "ep01_04_하품입벌림.mp4", "1화", "04",
     "하품하며 입을 크게 벌림"),
    ("ng", "ep02/prod/clips/12_old.mp4", "ep02_12_박수치며입벌림.mp4", "2화", "12",
     "박수 동작이 입 벌림을 유발"),
    ("ng", "ep02/prod/clips/12_try1.mp4", "ep02_12_저울이안맞음.mp4", "2화", "12",
     "마음의 저울이 수평을 되찾는 결말인데 저울이 한쪽으로 기울어 있음. 시작 그림부터 접시 높이가 달랐던 것"),
    ("ng", "ep04/prod/clips/01_old.mp4", "ep04_01_형광플라스틱하트.mp4", "4화", "01",
     "펠트 하트 배지가 형광 핑크 플라스틱처럼 빛나고, 콩이가 가방을 든 채 끝나 곰곰이가 가방을 메지 않음"),
    ("ng", "ep04/prod/clips/03_old.mp4", "ep04_03_액자에사람사진.mp4", "4화", "03",
     "펠트 세계 액자 안에 실제 사람 사진이 들어감. 게다가 카메라가 올라가며 곰곰이가 화면 밖으로 사라짐"),
    ("ng", "ep01/v3/clips/10_dynamicB.mp4", "ep01_10_끝에입벌림.mp4", "1화", "10",
     "추적 카메라는 좋았지만 마지막에 입이 벌어짐"),

    # ── ALT: 멀쩡한데 다른 이유로 안 쓴 컷 ────────────────────
    ("alt", "ep04/prod/clips/01.mp4", "ep04_01_소품선물_미사용.mp4", "4화", "01",
     "콩이가 가방과 하트 배지를 선물하는 컷. 완성도는 괜찮지만 4화 주제(비교)와 연결이 안 되고 첫 2초 훅을 잡아먹어 뺌. "
     "시즌 오프닝이나 예고편에 쓸 만함"),
    ("alt", "ep01/v3/clips/05_seedance_try.mp4", "ep01_05_대안_콩이만비행.mp4", "1화", "05",
     "곰곰이는 러그에 앉고 콩이만 빛구슬 사이를 나는 안전한 버전. 원본 분위기가 더 좋아서 안 씀"),
    ("alt", "ep01/v3/clips/10_seedance_try.mp4", "ep01_10_대안_착지.mp4", "1화", "10",
     "입은 다물었지만 움직임이 적어 심심해서 탈락"),
    ("alt", "ep01/v3/clips/13_seedance_try.mp4", "ep01_13_대안_뒷모습.mp4", "1화", "13",
     "뒷모습 유지 버전. 카메라가 물러나기만 해 밋밋"),
    ("alt", "ep02/prod/clips/09_seedance_try.mp4", "ep02_09_대안_용기포즈.mp4", "2화", "09",
     "입은 다물었지만 원본의 카메라 무빙이 더 좋아 되돌림"),
    ("alt", "ep02/prod/clips/13_seed8.mp4", "ep02_13_대안_별상승.mp4", "2화", "13",
     "엔딩 대안본"),
    ("alt", "ep04/prod/clips/04_size_old.mp4", "ep04_04_부엉이가2배.mp4", "4화", "04",
     "부엉이 할아버지가 곰곰이의 2배 크기. 크기 규칙 정하기 전 버전"),
    ("alt", "ep04/prod/clips/05_size_old.mp4", "ep04_05_부엉이가작음.mp4", "4화", "05",
     "같은 부엉이가 이번엔 곰곰이보다 작음. 04와 정반대라 크기 규칙을 만든 계기"),
    ("alt", "ep04/prod/clips/09_size_old.mp4", "ep04_09_보리가큼.mp4", "4화", "09",
     "보리가 곰곰이보다 1.5배 큼"),
    ("alt", "ep04/prod/clips/10_size_old.mp4", "ep04_10_보리가큼.mp4", "4화", "10",
     "보리가 곰곰이보다 큼"),
]

# 반려 그림
IMGS = [
    ("ep03/prod/img_reject/03_grey_owl.png", "ep03_03_부엉이색틀림.png", "3화", "03", "부엉이 색을 지정 안 해 컷마다 갈색·회색으로 바뀜"),
    ("ep03/prod/img_reject/04_grey_owl.png", "ep03_04_부엉이색틀림.png", "3화", "04", "같은 문제"),
    ("ep03/prod/img_reject/05_bear_ears.png", "ep03_05_부엉이에곰귀.png", "3화", "05", "부엉이한테 곰 귀가 달림"),
    ("ep03/prod/img_reject/10_bread_in_mouth.png", "ep03_10_빵물고있음.png", "3화", "10", "빵을 입에 물어 입이 벌어짐"),
    ("ep04/prod/img_reject/01_old.png", "ep04_01_형광하트_그림.png", "4화", "01", "형광 플라스틱 하트"),
    ("ep04/prod/img_reject/03_old.png", "ep04_03_사람사진_그림.png", "4화", "03", "액자 속 사람 사진"),
    ("ep02/prod/img_reject/12_old.png", "ep02_12_기울어진저울.png", "2화", "12", "시작 그림부터 접시 높이가 다름"),
    ("ep01/v3/img_reject/04_old.png", "ep01_04_하품_그림.png", "1화", "04", "하품 입 벌림"),
]


# 사고가 보이는 구간 (NG 영상 만들 때 이 지점을 쓰면 됨)
WHEN = {
    "ep02_13_만화곰으로변신.mp4": "2.0초 — 뒤돌아보는 순간 매끈한 만화 곰으로 바뀜",
    "ep04_13_곰곰이가날아감.mp4": "1.6~3.2초 — 곰곰이가 입 벌린 채 날아오름",
    "ep01_05_공중에서형태붕괴.mp4": "2.4초 — 공중에서 뒤집히며 형태가 무너짐",
    "ep01_13_하늘로사라짐.mp4": "2.4초~ — 점처럼 작아지며 하늘로",
    "ep01_13_얼굴초근접웃음.mp4": "1~3초 — 얼굴이 화면 가득",
    "ep01_10_입벌리면딴곰.mp4": "3.9초~ — 입이 벌어지며 얼굴 비율이 달라짐",
    "ep01_10_끝에입벌림.mp4": "마지막 1초",
    "ep01_04_하품입벌림.mp4": "중반",
    "ep02_12_박수치며입벌림.mp4": "중반",
    "ep02_12_저울이안맞음.mp4": "처음부터 끝까지 기울어 있음",
    "ep04_01_형광플라스틱하트.mp4": "2.4초~ — 하트가 형광으로 빛남",
    "ep04_03_액자에사람사진.mp4": "처음부터. 2.4초에 액자가 크게 보임",
}


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def main():
    for sub in ["ng", "alt", "img", "sheets"]:
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    rows = []
    for kind, src, name, ep, cut, why in ITEMS:
        s = H / src
        if not s.exists():
            print("없음:", src)
            continue
        d = OUT / kind / name
        if not d.exists():
            shutil.copy2(s, d)
        rows.append((kind, name, ep, cut, why, round(dur(d), 2), src))
        print(f"{kind} ← {src}")

    img_rows = []
    for src, name, ep, cut, why in IMGS:
        s = H / src
        if not s.exists():
            print("없음:", src)
            continue
        d = OUT / "img" / name
        if not d.exists():
            shutil.copy2(s, d)
        img_rows.append((name, ep, cut, why, src))
        print(f"img ← {src}")

    # 확인용 프레임 격자 (영상마다 중간 프레임 1장)
    font = ImageFont.truetype(str(FONT), 22)
    for kind in ["ng", "alt"]:
        picks = [r for r in rows if r[0] == kind]
        thumbs = []
        for _, name, ep, cut, _, d, _ in picks:
            f = OUT / kind / name
            t = max(d * 0.6, 0.1)
            tmp = OUT / "sheets" / f"_{name}.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(f),
                            "-frames:v", "1", "-q:v", "4", "-pix_fmt", "yuvj420p", str(tmp)], check=False)
            if tmp.exists():
                thumbs.append((f"{ep} {cut}", tmp))
        if not thumbs:
            continue
        cols = 4
        TW = 300
        TH = int(TW * 16 / 9)
        rows_n = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (TW * cols, (TH + 32) * rows_n), (18, 18, 18))
        dr = ImageDraw.Draw(sheet)
        for i, (label, p) in enumerate(thumbs):
            x = (i % cols) * TW
            y = (i // cols) * (TH + 32)
            dr.text((x + 8, y + 4), label, fill=(255, 220, 90), font=font)
            sheet.paste(Image.open(p).resize((TW, TH)), (x, y + 32))
        sheet.save(OUT / "sheets" / f"{kind}.jpg", quality=88)
        for _, p in thumbs:
            p.unlink(missing_ok=True)

    # MANIFEST
    lines = ["# 안 쓴 컷 모음 (outtakes)", "",
             "원본은 각 화 폴더에 그대로 있고 여기 있는 건 복사본입니다.",
             "`ng/`는 캐릭터가 무너지거나 사고가 난 컷, `alt/`는 멀쩡한데 다른 이유로 안 쓴 컷입니다.", "",
             "## ng — 사고 난 컷 (NG 영상용)", "",
             "| 파일 | 화 | 컷 | 길이 | 볼 구간 | 무슨 일이 있었나 |", "|---|---|---|---|---|---|"]
    for kind, name, ep, cut, why, d, src in rows:
        if kind == "ng":
            lines.append(f"| `{name}` | {ep} | {cut} | {d}초 | {WHEN.get(name, '-')} | {why} |")
    lines += ["", "## alt — 멀쩡한데 안 쓴 컷 (재사용 후보)", "",
              "| 파일 | 화 | 컷 | 길이 | 왜 안 썼나 |", "|---|---|---|---|---|"]
    for kind, name, ep, cut, why, d, src in rows:
        if kind == "alt":
            lines.append(f"| `{name}` | {ep} | {cut} | {d}초 | {why} |")
    lines += ["", "## img — 반려된 시작 그림", "",
              "| 파일 | 화 | 컷 | 문제 |", "|---|---|---|---|"]
    for name, ep, cut, why, src in img_rows:
        lines.append(f"| `{name}` | {ep} | {cut} | {why} |")
    lines += ["", "## 한눈에 보기", "", "- `sheets/ng.jpg` · `sheets/alt.jpg`", "",
              "## 모으지 않은 것", "",
              "- `fix0919/page/v/*` — 비교 페이지에 넣으려고 만든 저해상도 사본(중복)",
              "- `ep01/v2/*`, `ep01/clips/v*.mp4` — 폐기된 초기 그림체 테스트",
              "- `ref/veo_gate_test.mp4` — 모델 사용 가능 여부 확인용", ""]
    (OUT / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")

    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"\n영상 {len(rows)}개 · 그림 {len(img_rows)}장 · {total/1024/1024:.0f}MB → {OUT}")


if __name__ == "__main__":
    main()
