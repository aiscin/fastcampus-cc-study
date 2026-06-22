---
name: part02-start
description: "Part 02: 클로드코드 시작하기 (신 커리큘럼 v3). 설치 클립(1, 2)은 강의 영상으로 진행하고, 이 스킬은 Clip 3 첫 실행과 Clip 4 모드+Alias 두 클립을 단계별로 안내한다. '/part02', 'Part 02', '시작하기' 요청에 사용."
---

# Part 02: 클로드코드 시작하기

이 스킬이 호출되면 아래 규칙을 반드시 따른다.

**먼저 `_common/stop-protocol-v6.md`를 읽고 Phase별 STOP PROTOCOL을 숙지한다.**

---

## 신 커리큘럼 v3 — Part 02 구성

| 클립 | 실습 # | 제목 | 스킬 적용 |
|------|------|------|---------|
| 01 | 1 | Mac 환경 설치하기 | ❌ 강의 영상 (CC 미설치) |
| 02 | 2 | Windows 환경 설치하기 | ❌ 강의 영상 (CC 미설치) |
| **03** | **3** | **첫 실행 — 화면/슬래시/모델/powerup + 폴더 정리** | ✅ **Clip 3 가이드** |
| **04** | **4** | **주요 모드 + cc Alias** | ✅ **Clip 4 가이드** |

설치(clip 01/02)는 안티그래비티 IDE의 챗 에이전트가 안내한다 — 이 스킬은 CC 설치 후부터만 작동한다.

---

## References 파일 맵

| 클립 | 파일 | 강의 클립 |
|------|------|----|
| Clip 3 | `references/clip3-first-run.md` | clip-03 (실습 3) |
| Clip 4 | `references/clip4-modes-alias.md` | clip-04 (실습 4) |

---

## Scripts

| 스크립트 | 용도 |
|---------|------|
| `scripts/make-mockup-downloads.sh` | 다운로드 폴더 정리 실습용 50개 mock 파일 자동 생성 (OS 자동 감지: macOS / WSL / Linux) |

---

## 핵심 원칙 (반드시 준수)

1. **"~해줘" 패턴 금지 / "~하려는데 어떻게 해?" 패턴 강제**
   - 모든 사용자 입력 가이드는 "~하려는데 어떻게 해?" / "방법 알려줘" 형식
   - "~해줘" 형식은 절대 첫 멘트로 사용하지 말 것
   - Part 02 clip-03가 수강생의 첫 Claude Code 실습이므로 이 습관을 첫날부터 박는다 (memory: feedback_ask_how_pattern.md)

2. **Phase 단위 STOP PROTOCOL**
   - 각 Phase는 한 턴에 끝나지 않음 — 설명 → 안내 → STOP → 사용자 "완료" → 다음 Phase
   - 한 턴에 여러 Phase 묶지 말 것

3. **자율 에이전트 4단계 강조** (Clip 3 마지막 Phase)
   - 분석 → 판단 → 확인 → 실행
   - "AI가 실행 전 '할까요?' 묻는 게 안전장치" 메시지 필수

4. **목업 데이터 자동 제공** (Clip 3 마지막 Phase)
   - 사용자 다운로드 폴더가 비어있거나 시연용으로 명확한 결과 보고 싶을 때
   - `scripts/make-mockup-downloads.sh` 자동 실행으로 50개 mock 파일 생성
   - OS 자동 감지: macOS/WSL/Linux 모두 `~/Downloads/cc-demo` 하위 폴더 사용

5. **Clip 3에서 모드 설명 금지** — Clip 4 메인 주제이므로 Status Line 설명 시 "현재 모드는 다음 클립에서 자세히" hook만

6. **Auto 모드를 강의 기본으로** (Clip 4)
   - 4가지 모드 (일반/Auto/Plan/Bypass) 자동차 기어 비유
   - Auto 모드를 강의 기본 모드로 강조 + 직접 Shift+Tab으로 전환 체험

7. **cc Alias 설정** (Clip 4)
   - Mac: `~/.zshrc` / WSL: `~/.bashrc`
   - 외부 작업 — 쉘 설정 수정은 사용자 직접

8. **결과물 저장 규칙 ★**
   - 모든 실습 결과물은 `50-my-work/Part02-시작하기/실습{NN}-{제목}/`에 저장
   - 실습 시작 시 폴더 자동 생성 (`mkdir -p`)
   - 결과물 파일 + `README.md` (메타: 날짜·모드·모델·완료 시각) 함께 저장
   - 실습 폴더 매핑:
     - Clip 3 → `50-my-work/Part02-시작하기/실습03-첫실행-폴더정리/`
     - Clip 4 → `50-my-work/Part02-시작하기/실습04-모드소개-Alias/`

---

## 시작

**1단계: progress.json 확인**

워크스페이스 루트의 `progress.json`에서 `current_clip` 필드를 확인한다.

- 값이 있으면 → 재진입 로직 실행 (stop-protocol-v6.md 참조)
- 값이 null이면 → 아래 시작 질문 표시

**2단계: 시작 클립 선택**

```json
{
  "questions": [{
    "question": "어떤 클립을 진행할까요?",
    "header": "Part 02: 클로드코드 시작하기 (CC 설치 후)",
    "options": [
      {"label": "Clip 3: 첫 실행 — 화면/슬래시/모델/powerup + 폴더 정리", "description": "실습 3 / 첫 실행자가 알아야 할 모든 기본 + 자율 에이전트 4단계 첫 체험 (~10분)"},
      {"label": "Clip 4: 모드 + cc Alias", "description": "실습 4 / 4가지 모드 + 단축 실행 설정 (~10분)"}
    ],
    "multiSelect": false
  }]
}
```

선택한 클립의 첫 Phase부터 진행한다.

---

## Clip별 진행 흐름 요약

### Clip 3: 첫 실행 (5 Phase)

1. **Phase 1 — 화면 둘러보기**: 프롬프트 입력 영역 / Status Line / 응답 영역 / 도구 호출 / Permission Prompt
2. **Phase 2 — 슬래시 커맨드**: `/help` · `/clear` · `/compact` 직접 입력 체험
3. **Phase 3 — `/model` + 디폴트 설정**: Sonnet/Opus/Haiku 즉시 전환 + `settings.json`의 `"model"` 필드로 디폴트 영구화
4. **Phase 4 — `/powerup` 같이 해보기**: Claude Code의 인터랙티브 학습 도구 1~2개 같이 진행
5. **Phase 5 — 다운로드 폴더 정리**: mock 50개 자동 생성 → 자율 에이전트 4단계 + 5단계 흐름 체험

### Clip 4: 모드 + Alias (2 Phase)

1. **Phase 1 — 4가지 모드 + Shift+Tab 전환**: 자동차 기어 비유 + Auto 모드에 세팅
2. **Phase 2 — cc Alias 설정**: Mac `~/.zshrc` / WSL `~/.bashrc` + 작동 확인 + Part 02 완료 처리

---

## Part 02 완료 시 (Clip 4 Phase 2 끝나면)

1. progress.json 업데이트:
   - `completed_parts`에 "Part 02" 추가
   - `practice_completed`에 "실습 1-4" 기록 (실습 1, 2는 강의 영상으로 완료 가정)
   - `environment.os`: 확인된 OS 기록
   - `environment.claude_version`: `claude --version` 결과 기록
   - `environment.alias_set`: cc Alias 설정 여부
   - `environment.default_mode`: "Auto"
   - `current_clip`: null로 초기화
   - `last_activity`: 현재 시각
2. 안내:
   ```
   Part 02 완료!
   - Claude Code 설치, 첫 실행, 슬래시 커맨드, 모델 전환, powerup, 폴더 정리, 모드 세팅, cc Alias 모두 끝났습니다.
   - 다음은 Part 03 — 본격적으로 대화로 결과물을 만들어봅니다.
   - /part03 입력하세요.
   ```
