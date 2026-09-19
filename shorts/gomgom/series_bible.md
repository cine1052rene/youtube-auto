# 곰곰한 마음 — 시리즈 기준서

> 곰곰이가 마음에 대해 곰곰이 생각하는, 따뜻한 심리·철학 숏폼

## 포맷
- 세로 9:16, 한 편 40초
- 한 편 = 움직이는 영상 5컷(4초씩, 20초) + 천천히 확대되는 그림 8장(2.5초씩, 20초)
- 영상 컷은 **먼저 그림을 뽑고 그 그림을 움직이는 방식**(Veo 3.1 Lite, 시작 이미지 지정). 그림체가 흔들리지 않게 하기 위함
- 소리는 Veo에서 끄고, 내레이션(TTS)과 배경음악은 편집에서 입힘
- 화면 안에 글자를 그리지 않음. 자막은 편집에서 얹음

## 모델과 단가
| 용도 | 모델 | 단가 |
|---|---|---|
| 그림 | seedream_v5_lite | 장당 1크레딧 |
| 영상 | veo3_1_lite, 4초, 소리 끔 | 4크레딧 |

한 편 예상: 그림 13장 + 영상 20초 = 33크레딧, 다시 뽑기 30% 포함 약 43크레딧

## 캐릭터

**곰곰이** — 주인공. 말수 적고 다정한 크림색 펠트 곰. **작은 갈색 펠트 가방**을 늘 메고, 가슴에 **시즌 배지**를 단다(시즌1 코랄 하트 / 시즌2 노란 별 / 시즌3 단풍잎 / 시즌4 데이지). 여름·나들이 편에서는 **세이지 리본 보터햇**을 쓴다.
**콩이** — 곰곰이 어깨에 자주 앉는 노란 아기 병아리. 머리에 **콩나물 새싹 두 잎**. 곰곰이 대신 표정으로 반응함

> 기준 이미지: `ref/gomgom_master_s1.png`(시즌1 기본) · `ref/gomgom_master_s1_hat.png`(보터햇). 1~3화는 소품 없이 완성돼 있으며, 4화 첫 장면에서 콩이가 가방과 하트 배지를 선물하는 것으로 이어붙인다.

### 매 프롬프트에 그대로 붙이는 캐릭터 문장 (수정 금지)
```
Gomgom, a small round cream-colored needle-felted wool bear with soft fuzzy texture, small round ears with pale pink inner ears, bright round black bead eyes, a small dark brown nose, soft pink blush on the cheeks and a gentle warm smile with no teeth ever visible, wearing a small coral pink felt heart badge on its chest and a tiny brown felt satchel bag across its body; Kong, a tiny round yellow needle-felted baby chick with a small orange beak and one small green bean sprout with two round leaves on top of its head
```
- 테스트 이미지에서 곰 눈이 반쯤 감겨 졸리거나 새침해 보였음 → `bright round eyes`, `gentle warm smile`로 고정
- 콩이가 안 나오는 컷은 `Kong` 부분만 뺌
- 시즌이 바뀌면 배지 부분만 교체: 시즌2 `a small soft yellow felt star badge`, 시즌3 `a small honey-yellow felt maple-leaf badge`, 시즌4 `a small white and yellow daisy felt badge`
- 여름·나들이 컷은 뒤에 `wearing a small straw boater hat with a flat top and flat brim and a sage green ribbon, both round ears fully visible` 추가
- **이빨이 보이면 안 됨**(입은 벌려도 됨), 만화풍으로 바뀌면 안 됨

### 매 프롬프트 끝에 붙이는 그림체 문장 (수정 금지)
```
soft warm golden light, dreamy bokeh with gentle floating sparkles, cozy warm pastel palette, handmade felt and knit textures, high quality 3D render, vertical composition, no text, no letters
```

### 금지어 (글자·레이아웃이 생김)
`film still`, `poster`, `storybook`, `editorial`, `book`, `sign`, `screen showing`

## 톤
- 반말 대신 부드러운 존댓말. 가르치지 않고 곁에서 말하듯이
- 어둡거나 무거운 장면 금지. 힘든 감정도 포근한 공간 안에서 보여줌
- 모든 편은 **질문으로 시작해서, 오늘 해볼 수 있는 작은 것 하나로 끝남**
- 마지막 한 줄은 댓글을 부르는 질문

## 6편 대본 (40초, 약 230자 기준)

### 1화. 쉬어도 쉬어도 피곤한 이유
쉬는 날 하루 종일 누워 있었는데, 왜 더 피곤할까요?
곰곰이도 그랬어요. 소파에서 폰만 봤는데, 저녁엔 머리가 더 무거웠죠.
심리학자들은 진짜 회복에 네 가지가 필요하다고 해요. 일에서 마음 떼어놓기, 몸의 긴장 풀기, 작은 것에 푹 빠지기, 그리고 내가 고른 시간 보내기.
누워서 화면을 넘기는 동안, 몸은 쉬어도 머리는 계속 일하고 있었던 거예요.
오늘은 딱 십 분만, 좋아하는 걸 골라서 해보세요.
여러분은 쉴 때 뭘 하면 제일 개운해지나요?

> 근거: 직무 스트레스 회복 연구(Sonnentag & Fritz)의 회복 경험 4요소 — 심리적 분리, 이완, 숙달, 통제

### 2화. 칭찬은 금방 잊고, 한마디 지적은 오래 남는 이유
칭찬 열 번보다, 지적 한 번이 더 오래 남지 않나요?
곰곰이도 좋은 말 잔뜩 들은 날, 딱 한마디가 밤새 맴돌았어요.
우리 뇌는 나쁜 신호에 더 크게 반응하도록 만들어졌대요. 옛날엔 위험을 먼저 알아채야 살아남았으니까요.
그러니까 그 한마디가 오래 남는 건, 내가 약해서가 아니라 뇌가 나를 지키려는 거예요.
오늘 들은 좋은 말 세 개를 적어보세요. 뇌에게도 공평한 기회를 주는 거예요.
오늘 들은 좋은 말, 하나만 댓글로 나눠줄래요?

> 근거: 부정성 편향(negativity bias)

### 3화. 에피쿠로스가 말한 작은 행복
쾌락주의자라고 하면, 화려하게 즐기는 사람이 떠오르죠?
그런데 쾌락주의 철학자 에피쿠로스는 빵과 물, 그리고 친구면 충분하다고 했어요.
치즈 한 조각만 있어도 잔치를 벌일 수 있다고 편지에 쓸 정도였죠.
그가 말한 즐거움은 더 갖는 게 아니라, 마음이 흔들리지 않는 고요함이었어요.
곰곰이는 오늘 따뜻한 빵 한 조각을 천천히 먹어보기로 했어요.
여러분의 치즈 한 조각은 뭔가요?

> 근거: 에피쿠로스의 아타락시아(마음의 평정), 디오게네스 라에르티오스가 전한 편지 속 "치즈 한 단지" 일화

### 4화. 남과 비교하면 마음이 작아지는 이유
친구 소식을 보고 나면, 괜히 내가 작아 보일 때 있죠?
심리학자 페스팅어는 사람은 남과 비교하며 자신을 가늠한다고 했어요.
문제는 우리가 남의 가장 빛나는 순간과, 나의 평범한 하루를 비교한다는 거예요.
곰곰이가 부러워한 친구도, 사진 밖에서는 곰곰이처럼 하품하고 있었을지 몰라요.
오늘은 비교할 상대를 어제의 나로 바꿔보세요.
어제보다 조금 나아진 것, 하나 있나요?

> 근거: 사회비교 이론(Festinger, 1954)

### 5화. 걱정을 내려놓고 싶을 때
걱정이 꼬리에 꼬리를 물어서, 잠이 안 올 때 있죠?
옛 철학자 에픽테토스는 세상일을 두 바구니에 나눠 담으라고 했어요.
내가 어쩔 수 있는 것, 그리고 어쩔 수 없는 것.
곰곰이는 내일 비가 올지 걱정하다가, 우산을 챙기는 것만 자기 바구니에 넣었어요.
어쩔 수 없는 건 바구니째 살며시 내려놓아도 괜찮아요.
지금 내려놓고 싶은 걱정, 하나 있나요?

> 근거: 스토아 철학 통제의 이분법(에픽테토스, 엥케이리디온 1장)

### 6화. 별일 아닌데 괜히 서운할 때
별일도 아닌데, 괜히 서운할 때가 있죠?
곰곰이는 콩이가 인사를 안 하고 날아가서, 하루 종일 마음이 쓰였어요.
서운함은 사실, 말하지 않은 기대가 어긋났다는 신호래요.
콩이는 곰곰이가 인사를 기다리는 줄 몰랐던 거예요.
서운할 땐 상대를 탓하기 전에, 내가 뭘 기대했는지 먼저 살펴보세요. 그리고 가볍게 말해보는 거예요.
최근에 서운했던 일, 사실은 뭘 기대했었나요?

> 근거: 충족되지 않은 기대와 관계 갈등에 관한 관계심리학 일반 논의 (특정 이론명 없이 서술)
