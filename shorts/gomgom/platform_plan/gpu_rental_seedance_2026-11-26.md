# GPU 대여로 Seedance를 쓸 수 있나? (2026-11-26 조사, PhysiWorks 채팅에서 넘어옴)

## 사용자 질문
"gpu대여하고 씨댄스를 쓸수있어?"

## 결론
**불가능하다.** Seedance(1.5·2.0·2.5 모두)는 ByteDance의 **비공개 모델**이라 모델 파일(가중치)이 공개돼 있지 않다.
GPU를 빌려도 올릴 모델이 없다. → 지금처럼 **Higgsfield 등 API(크레딧)로만** 사용 가능 (그 밖에 BytePlus ModelArk 등 공식 API).
비유: 식당 비법 소스 — 주방(GPU)을 빌려도 소스는 그 식당에서만 사 먹을 수 있다.

## 현재 곰곰 제작 방식 (확인한 내용)
- Higgsfield 크레딧: 얼굴 컷 = Seedance (1.5 Pro 4초 4.8크레딧), 얼굴 없는 컷 = Wan(2.7, 이것도 비공개 버전)
- 한 편 약 55~60크레딧 (seasons_plan.md)

## GPU 대여로 할 수 있는 것 = 공개 모델로 교체
| 모델 | 공개 | 메모 |
|---|---|---|
| **Wan 2.2** | 공개, Apache-2.0 (상업 OK) | 자체 실행에 가장 무난. 14B는 VRAM 많이, 5B/1.3B는 가벼움 |
| LTX-2 | 공개, 연매출 $10M 초과 시 유료 라이선스 | 소리 동시 생성, VRAM 많이 씀 |
| HunyuanVideo | ⚠️ 라이선스 적용 지역에서 **한국 제외** | 사용 금지 |

**공개 모델의 장점: 곰곰이 전용 LoRA 학습 가능** → series_bible.md에서 계속 프롬프트로 막고 있는 문제(크기 흔들림·이빨·만화풍 변형)를 근본적으로 줄일 가능성.
단점: 얼굴 품질이 Seedance보다 떨어질 수 있음.

## GPU 대여 요금 참고 (2026-11, 1달러≈1,450원)
- RunPod: RTX 4090(24GB) 약 $0.34/시간 · L40S(48GB) $0.79~0.99/시간
- Modal(초 단위 과금): L40S $1.95/시간, 매달 $30 무료 크레딧

## 추천
1. 얼굴 컷은 당분간 Seedance(크레딧) 유지 — GPU 대여로 비용을 줄일 수 없음
2. 작은 비교 실험: GPU 몇 시간 대여(수천 원) → Wan 2.2에 곰곰이 LoRA 학습 → 같은 장면을 Seedance와 나란히 비교 → 충분하면 풍경 컷부터 이전해 크레딧 절약

## 출처
- https://clipdance.ai/blog/is-seedance-2-open-source
- https://kenerateai.com/blogs/can-you-run-seedance-2-0-locally
- https://www.seeddance.io/blog/seedance-2-5-open-source-weights-api
- https://magichour.ai/blog/ltx-2-3-vs-wan-2-2
- https://insiderllm.com/guides/local-ai-video-generation/
- https://www.promptquorum.com/power-local-llm/local-ai-video-generation-vs-cloud
- https://www.runpod.io/product/cloud-gpus · https://modal.com/pricing
