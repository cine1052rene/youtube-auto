# 블렌더 시험 — 복구 방법 (10/21 준비)

블렌더 시험은 이 폴더(`shorts/gomgom/blendertest/`) 안에서만 한다.
기존 화(ep01~08)·기준 이미지(ref/)·생성기(s2_make_gen.py)·편집기(make_sample.py)는 건드리지 않는다.

## 기준점
- git 태그 `before-blender-1021` (커밋 67c6e2c) — 시험 시작 직전 상태
- 블렌더 설정 백업: `blender_config_backup_1021.tgz` (%APPDATA%\Blender Foundation 전체)
- Claude MCP 설정 백업: `claude_json_backup_1021.json` (~/.claude.json)

## 마음에 안 들 때 되돌리기
1. 시험 결과물 지우기: 이 폴더의 `*.blend`, `render/` 삭제 (RESTORE.md·백업 파일은 남겨도 됨)
2. 코드가 바뀌었다면: `git diff before-blender-1021 --stat` 로 확인 → `git checkout before-blender-1021 -- <파일>`
3. 블렌더 설정 복구: 블렌더 끄고 `%APPDATA%\Blender Foundation` 지운 뒤 tgz 풀기
   `tar -xzf blender_config_backup_1021.tgz -C "$APPDATA"`
4. 블렌더 자체를 아예 없애려면: `C:\Users\cine1\blender_app\` 폴더 삭제 + `claude mcp remove blender --scope user`
   (휴대용 설치라 시스템에 다른 흔적 없음)
5. 확인 사이트에 시험 페이지를 올렸다면: review_site/public/<페이지 폴더> 삭제 → 목차 줄 삭제 → 재배포

## 크레딧
- 블렌더 작업 자체는 무료.
- 블렌더 그림을 펠트 질감으로 바꾸는 AI 단계(힉스필드)·generate_3d는 크레딧이 들 수 있음 → 금액 알리고 허락받은 뒤에만.
