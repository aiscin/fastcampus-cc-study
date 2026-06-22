# 클로드코드 뽀개기 — 학습 워크스페이스

> 패스트캠퍼스 Claude Code 온라인 강의 전용 워크스페이스입니다.

---

## 시작하기

### 1. Claude Code 설치

강의 영상(Part 02 클립 01/02)을 보면서 본인 OS에 맞춰 Claude Code 설치를 끝내세요.
- Mac 사용자 → 클립 01
- Windows 사용자 → 클립 02

### 2. 워크스페이스 받기

```bash
git clone https://github.com/fivetaku/fastcampus-cc.git
cd fastcampus-cc
```

### 3. Claude Code 실행

```bash
cc      # alias 설정 후
# 또는
claude
```

### 4. Part 02 시작

Claude Code 안에서:

```
/part02
```

→ Clip 3 (첫 실행) 또는 Clip 4 (모드+Alias) 선택해서 진행합니다.

---

## 폴더 구조

10단위 넘버링으로 정돈됐어요.

```
fastcampus-cc/
├── CLAUDE.md          ← AI에게 나를 알려주는 파일 (Part 05에서 본격 작성)
├── README.md          ← 이 파일
├── progress.json      ← 진행률 자동 추적
│
├── .claude/
│   ├── commands/      ← 커스텀 슬래시 커맨드
│   └── skills/        ← 강의 가이드 스킬 (/part02 등)
│
├── 00-system/         ← 시스템 규칙 (한국어 답변 등)
├── 10-curriculum/     ← 강의 자료 (커리큘럼 PDF 등)
├── 20-references/     ← 참고 예시 (CLAUDE.md / 스킬 / 커맨드 / Hook / MCP / 에이전트)
├── 30-templates/      ← 결과물 템플릿
├── 40-mock-data/      ← 실습용 샘플 데이터 (CSV / XLSX)
├── 50-my-work/        ← ★ 내가 만든 결과물 (Part별 → 실습별 자동 정리)
└── 90-archive/        ← 옛 버전 / 백업
```

**핵심**: 모든 실습 결과는 `50-my-work/Part{NN}-제목/실습{NN}-제목/`에 자동 저장됩니다. 학생이 직접 폴더 만들 필요 없어요 — 강의 가이드 스킬이 알아서 처리합니다.

---

## AI Native 4단계 여정

| Lv | 이름 | 달성 시점 |
|----|------|----------|
| 1 | AI Starter | 시작 (지금) |
| 2 | AI Intermediate | Part 03 완료 — 대화로 결과물 만들기 |
| 3 | AI Advanced | Part 06 완료 — 직접 스킬 만들기 |
| 4 | AI Native | Part 07 완료 — 실전 활용 |

---

## 강의 흐름 (9 Part)

| Part | 제목 | 범위 |
|---|---|---|
| 01 | 인트로 | 강사·강의 소개 (영상만) |
| 02 | 시작하기 ★ | 설치 + 첫 실행 + 모드 (실습 1-4) |
| 03 | 체험하기 | 데이터→보고서→대시보드 + 콘텐츠 + 바이브코딩 (실습 5-13) |
| 04 | 강화하기 | GPTaku 플러그인 + AI 팀 + UI/UX (실습 14-17) |
| 05 | 뜯어보기 | CLAUDE.md / 커맨드 / MCP / Hook / GitHub (실습 18-22) |
| 06 | 스킬 만들기 ★ | 직접 스킬 제작 (실습 23-31) |
| 07 | 실전 활용 | 워크스페이스 / 자동화 / 트렌드 분석 (실습 32-40) |
| 08 | [Bonus] 성장 로드맵 | 회고 + 다음 단계 |
| 09 | 월간 세미나 | 매달 업데이트 |

자세한 커리큘럼은 `10-curriculum/패스트캠퍼스-교육과정소개서-클로드코드뽀개기.pdf` 참고.

---

## 도움이 필요할 때

**강의 가이드**:
- `/part02` ~ `/part08` — Part별 가이드 스킬 호출

**진도/레벨 확인**:
- `/my-progress` — 지금까지 완료한 실습 목록
- `/check-level` — 현재 레벨 (AI Starter ~ AI Native) + 다음 단계
- `/막혔어요` — 에러/문제 해결 가이드 (어디서 막혔는지 진단)

**클로드코드 자체 명령**:
- `/help` — 슬래시 명령 전체 목록
- `/usage` — 토큰 사용량·비용·한도 확인
- `/powerup` — 클로드코드 자체 학습 (인터랙티브)

**막히면**: 클로드코드에 그냥 물어보세요 — `~하려는데 어떻게 해?`
