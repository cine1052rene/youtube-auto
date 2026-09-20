# Daily Soul Challenge — 매일 아침 실행 순서

> ⚠️ **예약 메시지에 적힌 "장면 4개 / 추천 1~2장 전송"보다 이 런북이 우선한다.** 현행: 장면 5~6개 생성 → 번호 컨택트시트 → 서로 다른 콘셉트 3장 이상 추천. **파일은 폰으로 보내지 않고(9/17 글로벌 규칙) PC 경로만 알린다** — 사용자는 higgsfield.ai Assets에서 직접 골라 올린다.

Higgsfield 디스코드 #daily-soul 채널의 일일 챌린지. 매일 5명 선정, 1인당 1000크레딧.
새 주제는 매일 약 01:00 KST에 고정 메시지로 올라오고, 다음 주제가 올라오기 전까지 게시해야 한다.
월간 Academy Spotlight(첫 참가자 대상: 작품 수·꾸준함·반응) 크레딧도 함께 노린다 → **매일 빠짐없이 참가**가 중요.

## 규칙 (고정 메시지 기준)
- Soul 계열 모델(Soul, Soul 2.0, Soul Cinema)로 생성 → **Soul 2.0(`text2image_soul_v2`)만 사용** (Soul Cinematic은 규정명과 일치 불확실)
- 이미지 + Higgsfield **웹 생성물 공유 링크**를 함께 게시해야 유효
- 게시는 사용자가 직접 한다 (개인 계정 자동 게시는 디스코드 약관 위반)

## -1. PC 잠금 확인 (9/19 추가) ⚠️ 가장 먼저
- PowerShell `[bool](Get-Process LogonUI -ErrorAction SilentlyContinue)` 가 True면 **Windows 잠금 화면(PIN)** 상태 → 디스코드 창을 띄울 수 없고 키 입력도 전부 무시된다. PIN은 절대 입력하지 않는다
- 잠금이면 생성하지 말고: 사용자에게 "PC 잠금이 풀려야 진행 가능"이라고 알리고, `date`로 현재 시각 확인 후 **1시간 뒤 같은 작업을 재예약**(tbot_project_schedule_add). 13시가 지나도 잠겨 있으면 재예약을 멈추고 보고
- 9/18 아침 예약이 결과 없이 끝난 것, 9/19 08:10 실패 모두 이 원인(전원 설정은 AC 기준 화면·절전 '안 함'이라 절전 때문은 아님)

## 0. 어제 결과 먼저 확인 (9/16 추가)
- 당선 발표는 **다음 날 새벽 3~6시 KST**에 `#🏆|hall-of-fame`에 올라온다(9/16 발표 03:13, 9/17 발표 05:39 — 시각이 일정하지 않으니 아침에 확인하면 항상 떠 있다) (Vinca | Community Team이 "Daily Soul Challenge · Hall of Fame / <주제> · <날짜>" + "Today's champions: 🏆@5명" 형식으로 게시)
- 아침 작업 시작 시 hall-of-fame을 먼저 열어 어제 주제 글의 champions 5명에 사용자(T100roxy)가 있는지 확인하고 보고한다
- Ctrl+K로 `hall-of-fame` 검색하면 **OpenAI 서버 채널이 먼저 잡힌다** → 목록에서 "Higgsfield AI" 줄을 골라야 함(↓ 한 번 + Enter)
- 당선 시 1인당 1000크레딧. 링크 없는 게시물은 실격이므로 사용자에게 안내할 때 항상 링크를 강조한다

## 공식 룰 요약 (docs-storage 스레드 전문, 9/20 확인)
- Soul / Soul 2 / Soul Cinema만. 이미지 + 생성 링크를 **한 메시지**에 올려야 채점됨. SFW·PG-13
- 하루 투고 무제한이지만 **1인 1승**. 다음 주제가 올라올 때까지 접수. 이전 당선자도 재당선 가능
- 채점: theme relevance / execution quality / originality / narrative·emotion / prompt execution, 각 1~10점(최대 50). 리액션은 투표가 아님
- 보상: 매일 5명, 1000cr 프로모 코드를 DM으로 받음 → **7일 안에 Manage Account → Promocode에 입력**(입력 시점부터 90일 유효)
- 공식 팁: 예상 밖의 해석이 눈에 띈다 / 화려함보다 깔끔한 완성도 — 올리기 전 손·얼굴·디테일 점검

## 심사 기준 (9/16부터 당선작 카드에 점수표가 공개됨) ⭐
당선작 이미지 하단에 채점표가 박혀 나온다. **5개 항목 × 10점 = 50점 만점.**

| 항목 | 의미 | 9/16 5인 평균 |
|---|---|---|
| Theme | 주제 부합 | 9.0 |
| Quality | 이미지 완성도 | 8.4 |
| Originality | 독창성 | 8.2 |
| Emotion | 감정 전달 | 8.2 |
| Prompt | **프롬프트 자체의 완성도** | 8.4 |

9/16(My Usual Route) 실측: deelsewerld 44 / mr.yousaf 43 / brilz 43 / sofiatitova 42 / ramadangonim 39

읽어낸 것:
- **당선 커트라인이 39점**이었다. 만점권이 아니라 **다섯 항목 모두 8점 이상**이면 든다 — 한 항목만 튀는 것보다 고른 점수가 유리
- Quality는 누구도 9를 넘지 못했다. 그림만 예쁘게 뽑아선 못 이긴다
- Theme이 가장 높게 나온다(최저 8). 주제에서 벗어나면 그 시점에 탈락
- **Prompt가 채점 대상** → 심사자가 생성 링크로 프롬프트 원문을 읽는다. 키워드 나열이 아니라 **의도가 읽히는 문장**으로 쓸 것. `no watermark, no signs` 같은 기술적 꼬리표는 최소화
- Originality에 7~8점이 몰린다 → **여기가 승부처**. 주제문에 예시로 나온 소재(final boss in uniform 등)를 그대로 쓰면 이 점수가 깎인다
- ramadangonim은 9/14·9/15·9/16 3일 연속 당선했고 9/16엔 최저점(39)으로 들었다 → 꾸준한 참가자가 유리하거나, 하루에 여러 장 올려 확률을 높이는 것으로 보인다

## 1. 오늘 주제 읽기 (디스코드 데스크톱 앱 화면 캡처)
- 클릭·캡처 스크립트: `challenges/daily_soul/tools/dc.ps1` — PowerShell에서 `& C:/project/youtube/challenges/daily_soul/tools/dc.ps1 -x X -y Y [-scroll -720] -out 캡처경로.png -wait 1500` (좌표 없이 -out만 주면 창만 앞으로 가져와 캡처). 캡처 파일은 세션 scratchpad에 저장
- ⚠️ **키 입력 전 디스코드 창 제목에 "Higgsfield AI"가 들어있는지 확인**한다. 다른 서버가 열려 있으면 Ctrl+K 입력이 그 서버의 메시지 입력창에 타이핑될 수 있다(9/19 사용자 개인 서버에 "hall-of-fame"이 입력됨 — 전송 전 삭제). 제목이 다르면 먼저 좌측 서버 아이콘에서 Higgsfield를 클릭
- 키 입력은 SendKeys 대신 user32 keybd_event 사용(Ctrl+K=0x11+0x4B, Ctrl+V=0x11+0x56, Enter=0x0D, Esc=0x1B)
- Discord 창이 트레이에 있으면 `%LOCALAPPDATA%\Discord\Update.exe --processStart Discord.exe`로 띄운다
- Ctrl+K → `daily-soul` 붙여넣기 → Enter (다른 서버 채널이 먼저 잡히면 창 제목이 "Higgsfield AI"인지 확인)
- 채널 상단 설명 "Today's theme: …" + 오른쪽 위 핀 아이콘(고정 메시지)에서 가장 최근 "Daily Soul Challenge" 글을 캡처해 주제 설명 전체를 읽는다
- 이미 오늘 날짜 폴더가 있고 후보가 전달됐으면 중복 생성하지 않는다

## 2. 후보 생성
- 폴더: `challenges/daily_soul/YYYY-MM-DD/` (KST 날짜)
- 장면 **5~6개** 기획 → `prompts.txt`에 한 줄에 하나씩 작성 → `bash challenges/daily_soul/gen_daily.sh YYYY-MM-DD` (장당 0.12cr)
- **투고는 3장 이상**(9/17 확정). 규정에 장수 제한이 없고 "Drop your image(s)"라 복수 투고가 허용되며, 당선자 5명은 매일 서로 다른 사람이라 **여러 장을 올려도 그중 최고점 한 장으로 평가**된다 → 티켓만 늘어남
  - 단 **서로 다른 콘셉트**여야 한다. 같은 발상의 변주 3장은 Originality가 같이 깎여 티켓 1장과 다름없다
  - 게시 전 #daily-soul을 훑어 남이 이미 올린 소재·장소와 겹치는지 확인한다(9/17 빨래방·편의점이 겹쳤음)
- 프롬프트 요령 (9/15 결과에서 얻은 교훈):
  - 주제 예시 문구의 핵심을 그대로 살리고, 한눈에 읽히는 상황 하나에 집중
  - 인물 사진 주제면 "realistic candid photograph, on-camera flash, wide 24mm, dynamic tilted angle, every face distinct, natural anatomy with correct hands and legs"
  - 앉은 사람은 "clearly visible bench/chair"를 명시 (안 쓰면 허공에 앉은 모습이 나옴)
  - 동물·주인공 얼굴이 소품에 가려지지 않게 "face clearly visible"
  - 칠판·간판·표지판 등 글자가 들어갈 소품 금지, "no text, no watermark"
- 잔액 20cr 미만이면 생성하지 말고 사용자에게 알린다 (곰곰한 마음 제작 예산 보호)
  - ⚠️ **무장한 캐릭터 + 어린아이를 한 장면에 넣으면 서버가 생성을 거부한다**(create는 되지만 결과가 실패, 크레딧 미차감). 9/17 "거대 전사가 아이 신발끈 묶어주기"가 2회 연속 실패 → 아이를 빼고 다른 장면으로 교체할 것
  - 채널에 이미 올라온 남의 작품과 소재가 겹치지 않는지 게시물을 훑고 나서 기획한다

## 3. 점검
- 4장 전부 열어서 확인: 깨진 글자, 손·다리·얼굴 이상, 주제와 맞는지, 한눈에 웃긴지
- 방향·가림이 애매하면 부분 확대 이미지로 확인
- 좋은 것이 1장도 없으면 1회만 추가로 4장 재생성

## 4. 전달
- **생성분 전체를 번호 붙인 컨택트시트 1장으로 만들어 먼저 보낸다**(PIL로 3열 격자, 좌상단에 큰 번호 + 한 줄 설명 + [추천]/(반려) 표시). 파일명 번호와 생성순 번호가 어긋나 혼선이 생기므로 **이 시트 번호로만 소통**한다
- 추천작 번호와 이유, 그리고 **각 추천작의 생성 시각**(gen.log의 done 시각)을 알린다 — 사용자는 **Higgsfield 앱 Assets에서 이미지 다운로드와 공유 링크 복사를 한 번에** 하므로 생성 시각이 찾는 기준이다. PC 경로는 참고용으로 한 줄만(SendUserFile 사용 금지)
- ⚠️ **규정 위배 아이디어는 생성 금지**(9/20 사용자 확정): 사용자가 제안한 소재라도 그날 요구사항(예: "aliens taking over a human place")에서 벗어나면 **생성하지 말고 먼저 경고**한다. 반대 구도(인간이 외계를 점령 등)는 Theme 감점 위험. 대안을 제시했더라도 사용자 확인 뒤에 생성한다
- **콘셉트 중복 제거**(9/19 사용자 확정): 추천·하트 전에 같은 발상의 변주를 묶어 가장 강한 한 장만 남기고, 뺀 것은 "○번과 콘셉트 겹침"이라고 먼저 경고한다
- **추천작에 Higgsfield 하트(Favorites) 표시**(9/19 추가): PC의 Higgsfield 앱 창(Chrome PWA, 제목 "Higgsfield - Assets")을 최대화 → Today 타일에 마우스를 올리면 좌하단에 하트가 뜬다(타일 좌상단 기준 약 +17,+242) → 클릭 후 좌측 Favorites 숫자로 확인. CLI엔 즐겨찾기 기능 없음. 사용자가 PC를 쓰는 중이면 먼저 물어볼 것
- 한국어로 짧게: 오늘 주제 한 줄 요약, 추천 순위와 이유, 올리는 방법
  1. higgsfield.ai → Assets에서 해당 이미지(생성 시각 안내) 열기
  2. 공유 아이콘 → Copy Link
  3. 디스코드 #daily-soul에 이미지 + 링크 게시 (다음 날 01시 전)
- 메모리 `higgsfield_discord.md`에 날짜·주제·추천 id·잔액 한 줄 기록, `gen_daily.sh`/`prompts.txt` 커밋
