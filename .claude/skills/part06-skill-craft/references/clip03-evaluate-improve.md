# Clip 3 — deep-research v1 분석·비교·디벨롭 → v2 (실습 24, 20분)

> 페르소나 메모 — A(마케터): SKILL.md 직접 손대는 부담 / B(PO): 비교 분석 빠르게 / C(영업): 본인 일 평생 라이프사이클 응용

## 자동 셋업

```bash
DEST=~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습24-스킬분석개선
SRC23=~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습23-딥리서치스킬
mkdir -p "$DEST"/{본인-v1-결과,강사-풀스펙-결과}/
# 필수 — clip-02 deep-research v1 + 결과 확인 + 산출 자동 복사 (원본은 실습23에 보존)
if [ -f ~/fastcampus-cc/.claude/skills/deep-research/SKILL.md ]; then
  echo "✓ clip-02 deep-research v1 확인됨"
  if [ -d "$SRC23" ]; then
    cp -n "$SRC23"/*.md "$DEST/본인-v1-결과/" 2>/dev/null
    COUNT=$(ls "$DEST/본인-v1-결과/" 2>/dev/null | wc -l | tr -d ' ')
    echo "✓ 실습23 v1 산출 ${COUNT}개 → 본인-v1-결과/ 복사 (원본 보존)"
  fi
else
  echo "⚠ deep-research 없음 — clip-02 먼저 완료 필수"
fi
# 강사 deep-research 플러그인 확인 (gptaku-plugins 마켓플레이스 내)
if [ -d ~/.claude/plugins/cache/gptaku-plugins/deep-research ]; then
  echo "✓ 강사 deep-research 플러그인 확인됨 — 비교 대상"
else
  if [ -d ~/.claude/plugins/marketplaces/gptaku-plugins ]; then
    echo "ℹ 마켓플레이스는 등록됨 — /plugin install deep-research@gptaku-plugins 만 실행하면 됨"
  else
    echo "ℹ 1) /plugin marketplace add fivetaku/gptaku_plugins  2) /plugin install deep-research@gptaku-plugins"
  fi
fi
# trash-guard hook 확인 (자동 백업용)
if grep -q "trash-guard" ~/fastcampus-cc/.claude/settings.json 2>/dev/null; then
  echo "✓ trash-guard hook 확인됨"
fi
echo "✓ 진도 폴더 + 비교 폴더 패턴 (본인-v1-결과 / 강사-풀스펙-결과) 준비 완료"
```

## 브리핑

이론 아닌 실습. **clip-02 본인 v1 ↔ 강사 본인 deep-research(gptaku-plugins) 비교·분석·디벨롭 → v2**. 사용자 명시 폴더 패턴 — 두 결과를 같은 폴더에 모아놓고 시각적으로 차이 확인.

**별도 폴더 패턴** (사용자 명시):

```
실습24-스킬분석개선/
├── 본인-v1-결과/김밥맛집-v1.md       ← clip-02 산출 이동
├── 강사-풀스펙-결과/전국_김밥_맛집_{날짜}/  ← 강사 /deep-research 호출 결과
├── 구조-분석.md
├── 비교-분석.md (5관점)
├── deep-research-v2-SKILL.md
└── 김밥맛집-v2-{날짜}.md
```

**5 STEP 흐름 (v3.0)**:

1. **별도 폴더 생성 + 두 결과 모아놓기** — 본인 v1 이동 + 강사 deep-research 호출 (같은 김밥 주제)
2. **본인 SKILL.md 구조 분석** — 약점 발견
3. **5관점 비교** — 출처 수 / 멀티에이전트 / 세션 폴더 / 산출 형식 / 인터랙티브 질문
4. **SKILL.md 직접 손 디벨롭** → v2 (trash-guard 자동 백업)
5. **v2 호출 + Before/After**

**메타 메시지** — 본인 스킬은 한 번 만들고 끝이 아니라 **라이프사이클(v1 → v2 → v3...)**. clip-02 메타 흐름이 "만들기 전" 사이클이면 본 클립은 "만든 후 다듬기" 사이클.

**Part 5 자산 사슬**: 실습 21 trash-guard hook (자동 백업 안전) + GPTaku Plugin (강사 deep-research)

## 단계 안내

| Phase | 내용 |
|------|------|
| A (1.5분) | 도입 — 같은 폴더에 두 결과 모아 비교 + 디벨롭 |
| B-1 (3분) | STEP 1 본인 v1 자동 복사 확인 + `/deep-research` 강사 호출 시 **출력 경로 명시 필수**: `"전국 김밥 맛집 주제로 딥리서치 해줘. 결과는 ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습24-스킬분석개선/강사-풀스펙-결과/ 에 저장해줘"` |
| B-2 (3분) | STEP 2 본인 SKILL.md 구조 분석 → 약점 발견 |
| B-3 (4분) | STEP 3 본인 v1 ↔ 강사 풀스펙 5관점 비교 → 추가할 디테일 1~2개 |
| B-4 (4분) | STEP 4 발견한 개선안 SKILL.md에 직접 손으로 → v2 (trash-guard 자동 백업) |
| B-5 (2분) | STEP 5 v2 호출 + Before/After 비교 |
| C (1분) | 마무리 — 본인 스킬 라이프사이클 첫 진화 |
| D (0.5분) | WRAP |

## WRAP

1. 결과물 검증 — `본인-v1-결과/` + `강사-풀스펙-결과/` + `구조-분석.md` + `비교-분석.md` + `SKILL.md.bak.{날짜}` + `SKILL.md` v2 + `김밥맛집-v2-{날짜}.md`
2. README — 5관점 비교 표 + Before/After
3. progress.json — `practice_completed`에 24
4. 회고 — "가장 큰 발견 한 줄"
5. 다음 — "clip-04 skillers-suda — 스킬 만들기 체계화한 도구"
