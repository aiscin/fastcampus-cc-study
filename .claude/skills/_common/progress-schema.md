# progress.json 스키마

> v6.0 커리큘럼 기반 경량 스키마 (2026-03-28)
> 위치: `workspaces/fastcampus-cc/my-work/progress.json`

---

## 스키마

```json
{
  "started_at": null,
  "completed_at": null,
  "level": "AI Starter",
  "current_part": null,
  "current_block": null,
  "completed_parts": [],
  "practice_completed": [],
  "skills_created": [],
  "projects_completed": [],
  "plugins_installed": [],
  "environment": {
    "os": null,
    "claude_version": null
  },
  "claude_md_version": "v0",
  "diagnosis": {
    "mid": null,
    "final": null
  },
  "last_activity": null
}
```

---

## 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `started_at` | string \| null | 강의 시작 시각 (ISO 8601). Part 0 완료 시 기록. |
| `completed_at` | string \| null | 강의 완료 시각 (ISO 8601). Part 7 완료 시 기록. |
| `level` | string | 현재 레벨. 초기값: "AI Starter" |
| `current_part` | string \| null | 현재 진행 중인 Part. 예: "Part 2" |
| `current_block` | string \| null | 현재 진행 중인 Block. 예: "Block 3". 세션 재진입에 사용. |
| `completed_parts` | array | 완료된 Part 목록. 예: ["Part 0", "Part 1"] |
| `practice_completed` | array | 완료된 실습 목록. 예: ["Part 2 Block 1"] |
| `skills_created` | array | 수강생이 직접 만든 스킬 목록. 예: ["/my-report"] |
| `projects_completed` | array | 완료된 프로젝트 목록. 예: ["포트폴리오 사이트"] |
| `plugins_installed` | array | 설치된 플러그인 목록. |
| `environment.os` | string \| null | 운영체제. 예: "Mac", "Windows" |
| `environment.claude_version` | string \| null | Claude Code 버전. 예: "1.x.x" |
| `claude_md_version` | string | CLAUDE.md 버전. "v0" → "v1" → "v2" |
| `diagnosis.mid` | object \| null | 중간 자가진단 결과 (Part 4 완료 후) |
| `diagnosis.final` | object \| null | 최종 자가진단 결과 (Part 7 완료 후) |
| `last_activity` | string \| null | 마지막 활동 시각 (ISO 8601) |

---

## 레벨 전환 규칙

| 레벨 | 전환 조건 |
|------|----------|
| AI Starter | 초기 레벨 |
| AI Intermediate | Part 2 완료 |
| AI Advanced | Part 5 완료 |
| AI Native | Part 7 완료 |

레벨 전환 시 Phase C에서 레벨업 알림을 표시하고 `level` 필드를 업데이트한다.

---

## current_block 사용법

`current_block`은 세션 재진입을 위한 핵심 필드입니다.

**스킬 시작 시:**
1. `current_block` 값을 확인한다
2. 값이 있으면 AskUserQuestion으로 재진입 여부 확인:
   - "Block N에서 멈추셨네요. 이어서 진행할까요?"
3. 이어서 진행 선택 시 해당 블록의 Phase A부터 시작

**블록 진행 중:**
- Phase B 진입 시: `current_block`을 현재 블록으로 설정
- Phase C 완료 시: `current_block`을 null로 초기화

**저장 형식:**
```json
"current_block": "Block 3"
```

---

## 초기 파일 생성

progress.json이 없는 경우, 스킬 시작 시 자동으로 생성한다:

```
my-work/progress.json 파일을 위 스키마의 기본값으로 생성
started_at은 Part 0 완료 시 기록
```
