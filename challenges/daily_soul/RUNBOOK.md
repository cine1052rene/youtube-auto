# Daily Soul Challenge — 매일 아침 실행 순서

Higgsfield 디스코드 #daily-soul 채널의 일일 챌린지. 매일 5명 선정, 1인당 1000크레딧.
새 주제는 매일 약 01:00 KST에 고정 메시지로 올라오고, 다음 주제가 올라오기 전까지 게시해야 한다.
월간 Academy Spotlight(첫 참가자 대상: 작품 수·꾸준함·반응) 크레딧도 함께 노린다 → **매일 빠짐없이 참가**가 중요.

## 규칙 (고정 메시지 기준)
- Soul 계열 모델(Soul, Soul 2.0, Soul Cinema)로 생성 → **Soul 2.0(`text2image_soul_v2`)만 사용** (Soul Cinematic은 규정명과 일치 불확실)
- 이미지 + Higgsfield **웹 생성물 공유 링크**를 함께 게시해야 유효
- 게시는 사용자가 직접 한다 (개인 계정 자동 게시는 디스코드 약관 위반)

## 1. 오늘 주제 읽기 (디스코드 데스크톱 앱 화면 캡처)
- 클릭·캡처 스크립트: `challenges/daily_soul/tools/dc.ps1` — PowerShell에서 `& C:/project/youtube/challenges/daily_soul/tools/dc.ps1 -x X -y Y [-scroll -720] -out 캡처경로.png -wait 1500` (좌표 없이 -out만 주면 창만 앞으로 가져와 캡처). 캡처 파일은 세션 scratchpad에 저장
- 키 입력은 SendKeys 대신 user32 keybd_event 사용(Ctrl+K=0x11+0x4B, Ctrl+V=0x11+0x56, Enter=0x0D, Esc=0x1B)
- Discord 창이 트레이에 있으면 `%LOCALAPPDATA%\Discord\Update.exe --processStart Discord.exe`로 띄운다
- Ctrl+K → `daily-soul` 붙여넣기 → Enter (다른 서버 채널이 먼저 잡히면 창 제목이 "Higgsfield AI"인지 확인)
- 채널 상단 설명 "Today's theme: …" + 오른쪽 위 핀 아이콘(고정 메시지)에서 가장 최근 "Daily Soul Challenge" 글을 캡처해 주제 설명 전체를 읽는다
- 이미 오늘 날짜 폴더가 있고 후보가 전달됐으면 중복 생성하지 않는다

## 2. 후보 생성
- 폴더: `challenges/daily_soul/YYYY-MM-DD/` (KST 날짜)
- 장면 4개 기획 → `prompts.txt`에 한 줄에 하나씩 작성 → `bash challenges/daily_soul/gen_daily.sh YYYY-MM-DD` (장당 0.12cr, 4장 약 0.5cr)
- 프롬프트 요령 (9/15 결과에서 얻은 교훈):
  - 주제 예시 문구의 핵심을 그대로 살리고, 한눈에 읽히는 상황 하나에 집중
  - 인물 사진 주제면 "realistic candid photograph, on-camera flash, wide 24mm, dynamic tilted angle, every face distinct, natural anatomy with correct hands and legs"
  - 앉은 사람은 "clearly visible bench/chair"를 명시 (안 쓰면 허공에 앉은 모습이 나옴)
  - 동물·주인공 얼굴이 소품에 가려지지 않게 "face clearly visible"
  - 칠판·간판·표지판 등 글자가 들어갈 소품 금지, "no text, no watermark"
- 잔액 20cr 미만이면 생성하지 말고 사용자에게 알린다 (곰곰한 마음 제작 예산 보호)

## 3. 점검
- 4장 전부 열어서 확인: 깨진 글자, 손·다리·얼굴 이상, 주제와 맞는지, 한눈에 웃긴지
- 방향·가림이 애매하면 부분 확대 이미지로 확인
- 좋은 것이 1장도 없으면 1회만 추가로 4장 재생성

## 4. 전달
- 추천 1~2장을 SendUserFile로 전송 (status: proactive)
- 한국어로 짧게: 오늘 주제 한 줄 요약, 추천 순위와 이유, 올리는 방법
  1. higgsfield.ai → Assets에서 해당 이미지(생성 시각 안내) 열기
  2. 공유 아이콘 → Copy Link
  3. 디스코드 #daily-soul에 이미지 + 링크 게시 (다음 날 01시 전)
- 메모리 `higgsfield_discord.md`에 날짜·주제·추천 id·잔액 한 줄 기록, `gen_daily.sh`/`prompts.txt` 커밋
