# Clip 9 — 모닝 브리핑 (Part 5 GWS + /nopal + 슬래시 커맨드, 실습 30, 30분)

> 페르소나 메모 — A(마케터): 메일 많음, 한 화면 가치 / B(PO): 외부 도구 연결 부담 / C(영업): 일정 + 고객 메일 우선순위 자동

## 자동 셋업

```bash
mkdir -p ~/fastcampus-cc/50-my-work/Part06-스킬만들기/실습30-모닝브리핑스킬/
mkdir -p ~/fastcampus-cc/.claude/skills/morning-briefing/
mkdir -p ~/fastcampus-cc/.claude/commands/
# clip-06 naver-news 활성화 확인 (재호출 대상)
if [ -f ~/fastcampus-cc/.claude/skills/naver-news/SKILL.md ]; then
  echo "✓ naver-news 확인 (재호출 가능)"
else
  echo "⚠ naver-news 없음 — clip-06 먼저"
fi
# Part 5 실습20 GWS CLI 자산 확인 (사용자 명시 자산 사슬)
which gws >/dev/null 2>&1 && echo "✓ Part 5 실습20 GWS CLI 자산 확인 (nopal 재활용)" || echo "ℹ Part 5 실습20 GWS CLI 연동 필요"
# nopal 플러그인 확인 (gptaku-plugins 마켓플레이스 내)
if [ -d ~/.claude/plugins/cache/gptaku-plugins/nopal ]; then
  echo "✓ nopal 확인 (GWS 자연어 오케스트레이션)"
else
  if [ -d ~/.claude/plugins/marketplaces/gptaku-plugins ]; then
    echo "ℹ 마켓플레이스는 등록됨 — /plugin install nopal@gptaku-plugins 만 실행하면 됨"
  else
    echo "ℹ 1) /plugin marketplace add fivetaku/gptaku_plugins  2) /plugin install nopal@gptaku-plugins"
  fi
fi
echo "✓ 진도 폴더 + morning-briefing 스킬 폴더 + commands 폴더 준비 완료"
```

## 브리핑

매일 아침 30분 작업을 한 클릭으로. **두 가지가 만남**:
1. **Part 5 실습20 GWS CLI 자산 사슬** — 이미 연동한 GWS 위에 nopal로 자연어 오케스트레이션
2. **clip-06 naver-news 스킬 재호출** — 스킬이 스킬을 부르는 첫 사례

**3개 데이터 소스 통합**:

| 소스 | 도구 | 출력 |
|------|------|------|
| 📧 메일 | nopal (Gmail) — Part 5 GWS 자산 위에 자연어 오케스트레이션 | 안 읽은 5건 |
| 📅 일정 | nopal (Calendar) | 오늘 일정 |
| 📰 뉴스 | clip-06 naver-news 재호출 | 관심 키워드 5건 |

> **뉴스 소스 확장 안내 (선택)** — 기본 흐름은 clip-06 naver-news 재호출 그대로 둔다(스킬이 스킬을 부르는 첫 사례·자산 사슬 핵심). 다만 관심사가 투자가 아니라 "그날 알아야 할 일반 뉴스"라면, **별도로 `daily-news` 같은 종합 헤드라인 스킬을 추가로 만들어 뉴스 칸을 갈아끼울 수 있다**. naver-news를 고치는 게 아니라(반도체 특화 깊이 유지) 새 스킬을 하나 더 만들어 morning-briefing이 골라 부르는 구조. 네이버 오픈 API엔 헤드라인 엔드포인트가 없으므로 분야별 다중 검색 → 군집·보도량 랭킹으로 근사한다.

```
[사전 준비] nopal 플러그인 설치·인증 (Part 5 GWS 자산 위에 — 새 인증 X)

[STEP 1] 워크플로우 잡기
   "메일·일정·뉴스 모아서 매일 아침 모닝 브리핑 만들려는데, 어떻게 워크플로우를 구성해야 할까?"
   → 단계별 워크플로우 정리 (소스 정의·통합 방법·출력 형태)
[STEP 2] 보완 + 실행 가능 단계 정의
   정리된 단계 살펴보고 보완 → 메일/일정은 nopal로·뉴스는 clip-06 naver-news 재호출·HTML 대시보드 등 클로드코드가 실제로 할 수 있는 단계로 정의 (스킬이 스킬을 부르는 패턴)
[STEP 3] 스킬로 만들기
   morning-briefing 스킬 (HTML 대시보드) + `/morning-briefing` 슬래시 커맨드 결합
[STEP 4] 만든 스킬로 테스트·검증
   "오늘 모닝 브리핑" 호출 → 브라우저 자동 열기 + 3 소스 확인
[STEP 5] SessionStart hook 연결 미리보기 + 본인 일 응용
```

**스킬 + 슬래시 커맨드 결합 모범 사례 (사용자 명시)**:
- description 자동 발동: "오늘 모닝 브리핑" 자연어
- **명시 호출**: `/morning-briefing` 슬래시 커맨드 (`commands/morning-briefing.md`)

**Part 5 → Part 6 자산 사슬**: 
- 실습 19 study-progress (커맨드 패턴 재활용)
- 실습 20 **GWS CLI 연동 ★** (nopal로 자연어 오케스트레이션 — 새 인증 X)
- 실습 21 SessionStart hook (자동 실행 예고)

**SessionStart hook 연결 미리보기** — Part 5에서 박은 hook을 변형해 매일 아침 모닝 브리핑 자동 안내.

## 단계 안내

| Phase | 내용 |
|------|------|
| A (2분) | 도입 — Part 5 GWS + clip-06 naver-news + 스킬 + 슬래시 커맨드 결합 |
| 사전 준비 | nopal 플러그인 설치·인증 (Part 5 GWS 자산 위에) |
| B-1 (3분) | STEP 1 워크플로우 잡기 — "메일·일정·뉴스 모아서 모닝 브리핑 만들려는데 어떻게 구성해야 할까?" |
| B-2 (4분) | STEP 2 보완 + 클로드코드가 실제로 할 수 있는 단계로 정의 (3 소스 통합·스킬이 스킬 호출·HTML 대시보드) |
| B-3 (8분) | STEP 3 morning-briefing 스킬화 (HTML 대시보드) + `/morning-briefing` 슬래시 커맨드 결합 |
| B-4 (4분) | STEP 4 만든 스킬로 테스트·검증 — 오늘 브리핑 (브라우저 자동 열기) |
| B-5 (3분) | STEP 5 SessionStart hook 연결 미리보기 (Part 5 자산 재활용) + 본인 일 응용 |
| C (1분) | 마무리 |
| D (1분) | WRAP |

## WRAP

1. 결과물 검증 — `morning-briefing/SKILL.md` + `commands/morning-briefing.md` + `실습30/brief-{날짜}.html` 1건
2. README — 3 소스 통합 + Part 5 GWS 자산 사슬 + 스킬 + 커맨드 결합 + Part 5 hook 연결 미리보기
3. progress.json — `practice_completed`에 30, `skills_created`에 `morning-briefing`, `commands_created`에 `morning-briefing`
4. 회고 — "본인 모닝 브리핑 추가 소스 한 줄"
5. 다음 — "clip-10 콘텐츠 파이프라인 — Part 06 마지막 ★ 6 STEP 풀 파이프라인"
