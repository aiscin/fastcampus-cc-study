# Clip 4 — skillers-suda — 스킬 만들기 체계화한 도구 (실습 25, 20분)

> 페르소나 메모 — A(마케터): "스킬 만드는 스킬" 추상적, 시연 빨리 / B(PO): clip-02 정석과 차이 명확 / C(영업): 본인 영업 일 자동 생성 사례

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습25-스킬러들의수다/
# skillers-suda 설치 확인 (gptaku-plugins 마켓플레이스 내)
if [ -d ~/.claude/plugins/cache/gptaku-plugins/skillers-suda ]; then
  echo "✓ skillers-suda 플러그인 확인됨"
else
  if [ -d ~/.claude/plugins/marketplaces/gptaku-plugins ]; then
    echo "ℹ 마켓플레이스는 등록됨 — /plugin install skillers-suda@gptaku-plugins 만 실행하면 됨"
  else
    echo "ℹ 1) /plugin marketplace add fivetaku/gptaku_plugins  2) /plugin install skillers-suda@gptaku-plugins"
  fi
fi
echo "✓ 진도 폴더 준비 완료"
```

## 브리핑

skillers-suda는 한 마디로 **스킬 만들기 자체를 체계화해서 만들어둔 도구**. clip-02에서 손으로 한 메타 흐름(분석 → 검증 → 스킬화)을 인터뷰 흐름으로 자동화. 4명 전문가 AI(아이디어 분석가·스킬 작가·검증자·통합자)가 수다 떨면서 SKILL.md 자동 생성.

**1부 도구 설명 + 2부 활용** (사용자 명시 구성):

- **1부**: skillers-suda 도구 자체 설명 — 왜 만들었나·어떻게 동작하나·언제 쓰면 좋나
- **2부**: skillers-suda 활용해 또 다른 스킬 만들기 — **구체 주제는 사용자가 본인 일에 맞게 결정**

**clip-02 정석 vs skillers-suda**:

| 항목 | clip-02 정석 | skillers-suda |
|------|------------|------------|
| 작성 | 강사가 SKILL.md 직접 (메타 흐름 손으로) | AI 4명 자동 (메타 흐름 자동 버전) |
| 시간 | 20분 | 5~7분 |
| 구조 이해 | ✓ (학습 목적) | △ (블랙박스) |
| 본인 일 응용 | 한 번 익혀두면 평생 | 빠른 첫 동작 형태 |

→ **clip-02 = 구조 이해 목적, skillers-suda = 평생 활용 도구**. 새 아이디어 떠오를 때마다 손으로 SKILL.md 안 짜고 이 도구 한 번 부르면 됨. 둘 다 익혀두면 본인 일에 맞게 골라 쓸 수 있다.

**Part 4 자산 사슬**: Part 04 clip-03 kkirikkiri 패턴 응용 (4명 전문가 자동 구성)

**clip-03 비교·분석·디벨롭 사이클 재사용** — 자동 생성된 스킬도 본인 일에 맞게 1~2줄 추가/수정하면 영구 자산. clip-03 라이프사이클 적용 가능.

## 단계 안내

| Phase | 내용 |
|------|------|
| A (1.5분) | 도입 — clip-02 정석 vs 스킬 만들기 체계화한 도구 |
| B-1 (2분) | STEP 1 skillers-suda 도구 자체 설명 (1부) |
| B-2 (1.5분) | STEP 2 본인 아이디어 한 줄 정하기 |
| B-3 (4분) | STEP 3 skillers-suda 호출 (4명 인터뷰 시작) |
| B-4 (5분) | STEP 4 인터뷰 답변 + 자동 생성 (2부 — 다른 스킬 만들기) |
| B-5 (2분) | STEP 5 첫 호출 시연 |
| B-6 (1.5분) | STEP 6 다듬기 — 본인 일에 맞게 (clip-03 비교·분석·디벨롭 사이클 재사용) |
| C (1분) | 마무리 — 본인 두 번째 스킬 |
| D (0.5분) | WRAP |

## WRAP

1. 결과물 검증 — `~/fastcampus-cc/.claude/skills/{생성스킬명}/SKILL.md`(활성) + `실습25/skill-source/`(원본 사본) + `실습25/{첫 호출 결과}`
2. README — 자동 생성 4단계 + 본인 다듬기 1~2건
3. progress.json — `practice_completed`에 25, `skills_created`에 새 스킬명
4. 회고 — "정석 vs 자동, 어느 쪽이 더 끌렸는지 + 본인 일 응용 한 줄"
5. 다음 — "clip-05 공공 API — TourAPI로 여행 가이드 (CH02 시작 ★ 스크립트 분리)"
