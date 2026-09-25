"""런칭 준비 페이지(index.html) 생성 — package.json 문구 + out/ 이미지 + 채널 설정 체크리스트."""
import html, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(BASE, 'package.json'), encoding='utf-8'))
e = html.escape

CHECK = [
    ('유튜브 — 오늘 업로드 전 필수', [
        '🔴 <b>youtube.com/channel_switcher → "새 채널 만들기"</b>로 만들어야 브랜드 계정이 됨(첫 화면의 "채널 만들기"는 내 이름 개인 채널이 될 수 있음) → 이름 <b>곰곰한 마음</b>, 핸들 <b>@gomgom_mind</b>. 확인: 스튜디오 → 설정 → <b>권한</b> 메뉴가 있으면 브랜드 채널',
        '로그인하는 <b>본인 구글 계정</b>에 2단계 인증 켜기 — 브랜드 채널은 이 계정으로 들어가 관리하므로 채널 탈취 방지용. 채널이 개인용으로 바뀌지 않음',
        '<b>기능 사용 인증(전화번호)</b> — 설명란 링크 클릭 가능·맞춤 미리보기 등 중급 기능이 열림',
        '🔴 설정 → 채널 → 고급 설정 → 시청자층: <b>"아니요, 아동용이 아닙니다"</b>를 채널 기본값으로. 아동용이면 댓글·광고·최종 화면이 전부 꺼짐',
        '설정 → 채널 → 기본 정보: 국가 <b>대한민국</b>, 키워드 <code>곰곰한마음 심리학 철학 마음공부 위로 힐링 쇼츠</code>',
        '설정 → 업로드 기본 설정: 카테고리 <b>교육</b>, 동영상 언어 <b>한국어</b>, 설명란 기본값에 맨 아래 제작 방식·109 두 줄 넣기',
        '같은 화면 고급 설정: 댓글 <b>"부적절할 수 있는 댓글은 검토를 위해 보류"</b>, 쇼츠 리믹스 <b>허용</b>',
        '맞춤설정 → 브랜딩: 프로필 사진(<code>profile_800.png</code>), 배너(<code>yt_banner_2560x1440.jpg</code>). 워터마크는 쇼츠에 안 보여서 생략',
        '맞춤설정 → 기본 정보: 채널 설명(아래 문구), 링크에 인스타·X 추가(계정 만든 뒤)',
        '콘텐츠 → 재생목록: <b>시즌 1 · 마음 사전</b> 만들기(공개)',
        '설정 → 커뮤니티 → 자동 필터: 차단 단어에 도박·홍보 문구, 링크 포함 댓글 보류',
        '휴대폰 YouTube 스튜디오 앱 설치 + <b>댓글 알림 켜기</b>(위기 댓글 즉시 확인용)',
    ]),
    ('유튜브 — 영상마다', [
        '세로 원본 파일 그대로 업로드(재인코딩 X)',
        '제목·설명·태그 붙여넣기(아래) → 재생목록 <b>시즌 1 · 마음 사전</b> 선택',
        '시청자층 <b>아동용 아님</b> 확인 · 변경/합성 콘텐츠(AI 표시) <b>아니요</b> — 애니메이션은 표시 의무 없음, 대신 설명란에 제작 방식 한 줄',
        '공개 설정 <b>예약</b> → 날짜·시간 확인(한국 시간)',
        '썸네일: 앱 업로드 화면에서 커버 이미지 업로드가 보이면 <code>cover_epNN_9x16.jpg</code>, 없으면 프레임 선택에서 곰곰이 얼굴이 잘 보이는 장면',
        '공개 직후 <b>고정 댓글</b> 달고 고정 → 첫 30분은 댓글에 직접 답하기',
    ]),
    ('인스타그램', [
        '새 계정 → 설정에서 <b>프로페셔널 계정(크리에이터)</b> 전환, 카테고리 <b>디지털 크리에이터</b>',
        '이름 <b>곰곰한 마음</b>, 사용자 이름 <b>gomgom_mind</b>(없으면 gomgom.mind), 프로필 사진 동일, 소개(아래), 링크 = 유튜브 채널',
        '릴스는 <b>원본 mp4</b>로 올리기(유튜브 다운로드본·워터마크 금지) → 커버에 <code>cover_epNN_9x16.jpg</code>, 격자 미리보기는 3:4 중앙이 보임',
        '공유 설정에서 <b>AI 라벨</b> 켜기 권장 — 숨기는 것보다 먼저 밝히는 게 유리(기획서 원칙)',
        '같은 시간(금 20:00) 예약 게시 가능 — 고급 설정 → 예약',
    ]),
    ('네이버 클립', [
        '네이버 앱 → 클립 → 내 채널 만들기(프로필 사진·소개 동일)',
        '업로드는 <b>모바일 앱에서만</b> 가능 — 원본을 폰으로 옮겨 두기',
        '1~2편 올린 뒤 2주차에 <b>클립 크리에이터 신청</b>(빈 채널로 신청하지 않기), 카테고리는 심리·교양 계열 1개',
    ]),
    ('X', [
        '프로필 사진 <code>profile_400.png</code>, 헤더 <code>x_header_1500x500.jpg</code>, 소개(아래), 링크 = 유튜브',
        '본편은 <b>영상 파일로 직접</b> 올리고 유튜브 링크는 <b>첫 답글</b>에, 해시태그는 1~2개',
        '🔴 <code>C:\\project\\X_twitter</code> 브라우저 자동화는 이 계정에 절대 쓰지 않기(영구정지 사유)',
    ]),
    ('네이버 블로그', [
        '카테고리 <b>곰곰한 마음</b> 만들기, 타이틀 이미지 <code>blog_title_966x300.jpg</code>',
        '첫 글은 일요일 오전 — 클립 영상 삽입 + 직접 쓴 한 문단(통째 AI 글 금지)',
    ]),
    ('공개 후 30분', [
        '고정 댓글 달기 → 첫 댓글들에 해설자 말투(존댓말)로 답하기. 곰곰이는 말하지 않고 괄호 지문으로만',
        '🔴 자해·자살 신호 댓글엔 AI 답글 금지 — 직접 짧게 공감 + 109 안내, 지우지 않기',
        '"AI죠?" 질문엔 정해둔 답: 영상은 AI 도구로 만들고, 이야기와 대본은 직접 쓰고 모든 장면을 한 컷씩 확인한다',
    ]),
]

IMGS = [
    ('profile_800.png', '프로필 800×800 (유튜브·인스타·클립·블로그)'),
    ('profile_400.png', '프로필 400×400 (X)'),
    ('yt_banner_2560x1440.jpg', '유튜브 배너 2560×1440 (가운데 1546×423만 모바일 노출)'),
    ('x_header_1500x500.jpg', 'X 헤더 1500×500'),
    ('blog_title_966x300.jpg', '블로그 타이틀 966×300'),
    ('cover_ep01_9x16.jpg', '1화 커버 9:16'),
    ('cover_ep02_9x16.jpg', '2화 커버 9:16'),
    ('cover_ep03_9x16.jpg', '3화 커버 9:16'),
]

def box(label, text):
    return (f'<div class="cp"><div class="cph"><span>{e(label)}</span>'
            f'<button onclick="cp(this)">복사</button></div><pre>{e(text)}</pre></div>')

parts = []
parts.append('<h2>업로드 일정 (9/25 재조정)</h2><table><tr><th>화</th><th>공개</th><th>제목</th></tr>' +
             ''.join(f'<tr><td>{x["n"]}화</td><td>{e(x["when"])}</td><td>{e(x["title"])}</td></tr>' for x in P['eps']) +
             '<tr><td>이후</td><td colspan="2">4화 금 10/9 한글날 20:00(준비 목 10/8) → 5화 화 10/13 → 6화 금 10/16. 매주 화·금 20:00, 준비는 공개 전날. 공휴일(10/3 개천절·10/5 대체공휴일)엔 작업 없음</td></tr></table>')
parts.append('<h2>채널 설정 체크리스트</h2>')
for sec, items in CHECK:
    parts.append(f'<h3>{e(sec)}</h3><ul class="ck">' +
                 ''.join(f'<li><label><input type="checkbox"><span>{it}</span></label></li>' for it in items) + '</ul>')
parts.append('<h2>이미지</h2><div class="grid">' +
             ''.join(f'<figure><img src="out/{f}" loading="lazy"><figcaption>{e(c)}<br><code>{f}</code></figcaption></figure>'
                     for f, c in IMGS if os.path.exists(os.path.join(BASE, 'out', f))) + '</div>')
parts.append('<h2>소개글</h2>' + ''.join(box(b['k'], b['t']) for b in P['bios']))
for x in P['eps']:
    parts.append(f'<h2>{x["n"]}화 — {e(x["when"])}</h2>')
    for k, lab in [('title', '유튜브 제목'), ('desc', '유튜브 설명란'), ('tags', '유튜브 태그'), ('pin', '고정 댓글'),
                   ('reels', '인스타 릴스 캡션'), ('clip', '네이버 클립 제목'), ('x', 'X 본문(영상 첨부)'), ('xr', 'X 첫 답글')]:
        parts.append(box(lab, x[k]))

CSS = """
:root{--bg:#fbf6ee;--fg:#3d2c20;--mut:#8a7462;--card:#fffdf8;--line:#eadfce;--acc:#c47860}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#1f1a16;--fg:#f1e6d8;--mut:#b9a58f;--card:#2a231d;--line:#40362c;--acc:#e59a80}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif}
main{max-width:760px;margin:0 auto;padding:24px 16px 80px}h1{font-size:26px;margin:0 0 4px}h2{margin:36px 0 10px;font-size:20px;border-bottom:2px solid var(--line);padding-bottom:6px}
h3{font-size:16px;color:var(--acc);margin:18px 0 6px}.sub{color:var(--mut);margin:0}table{width:100%;border-collapse:collapse;font-size:14px}
td,th{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}ul.ck{list-style:none;padding:0;margin:0}
ul.ck li{padding:6px 0;border-bottom:1px dashed var(--line)}ul.ck label{display:flex;gap:10px;align-items:flex-start}ul.ck input{margin-top:5px;flex:none;width:18px;height:18px}
ul.ck input:checked+span{opacity:.45;text-decoration:line-through}code{background:var(--line);padding:1px 5px;border-radius:4px;font-size:.88em;word-break:break-all}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
figure img{width:100%;display:block;max-height:360px;object-fit:contain;background:#0001}figcaption{padding:8px;font-size:13px;color:var(--mut)}
.cp{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:10px 0;overflow:hidden}.cph{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);font-weight:600;font-size:14px}
.cph button{border:0;background:var(--acc);color:#fff;border-radius:8px;padding:6px 14px;font-size:14px}pre{margin:0;padding:12px;white-space:pre-wrap;word-break:keep-all;font:15px/1.65 inherit;font-family:inherit}
"""
JS = """function cp(b){const t=b.closest('.cp').querySelector('pre').innerText;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).catch(()=>{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()});
b.textContent='복사됨';setTimeout(()=>b.textContent='복사',1200)}"""

page = (f'<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>곰곰한 마음 런칭 준비</title><style>{CSS}</style></head><body><main>'
        f'<h1>곰곰한 마음 런칭 준비</h1><p class="sub">2026. 9. 25(금) · 채널 설정 · 이미지 · 업로드 문구</p>'
        + ''.join(parts) + f'</main><script>{JS}</script></body></html>')
open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8').write(page)
print('index.html ok')
