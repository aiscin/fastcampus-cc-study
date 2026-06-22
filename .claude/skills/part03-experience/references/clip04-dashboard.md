# Clip 4: 대시보드 — 인터랙티브 HTML 대시보드

> Part 03 / Ch 02 / 실습 7 / ~25분
> 패턴: 자동 셋업 → 영상 보면서 같이 따라하기 → "완료" → WRAP
> 대응 클립: `30-practice-design/part-03-체험하기/clip-04-대시보드.md`
> 모범답안: `50-my-work/Part03-체험하기/실습07-대시보드/p3-c03-따라하기.md`

---

## 자동 셋업 (진행 안내 출력 직전 스킬이 즉시 Bash로 실행)

```bash
# 1) 워크스페이스 루트 자동 감지
WS="$(pwd)"
while [ "$WS" != "/" ] && [ ! -f "$WS/CLAUDE.md" ]; do WS="$(dirname "$WS")"; done
if [ "$WS" = "/" ]; then
  WS="$(pwd)"
  while [ "$WS" != "/" ] && [ ! -d "$WS/40-mock-data" ]; do WS="$(dirname "$WS")"; done
fi
[ "$WS" = "/" ] && { echo "⚠ 워크스페이스 루트 못 찾음"; exit 1; }
echo "워크스페이스: $WS"

# 2) 경로 (CLAUDE.md 표준)
DEST="$WS/50-my-work/Part03-체험하기/실습07-대시보드"
SRC1="$WS/50-my-work/Part03-체험하기/실습06-보고서작성"   # 우선순위 1: 직전 실습
SRC2="$WS/50-my-work/Part03-체험하기/실습05-데이터분석"   # 우선순위 2: Clip 2
MOCK="$WS/40-mock-data"

mkdir -p "$DEST"
cd "$DEST"

# 3) sample_csv 가져오기 (이전 실습 → mock 폴백)
for SRC in "$SRC1" "$SRC2"; do
  if [ -d "$SRC/sample_csv" ]; then
    cp -r "$SRC/sample_csv" ./ 2>/dev/null
    break
  fi
done
if [ ! -d ./sample_csv ] && [ -d "$MOCK" ]; then
  mkdir -p sample_csv
  cp "$MOCK"/*.csv sample_csv/ 2>/dev/null
fi

echo "=== 결과 ==="
ls -la
```

**셋업 결과 한 줄 안내**: "✓ 실습07-대시보드 폴더 준비 완료. sample_csv/ 가져왔어요. Ch 02 마지막 클립."

---

## 진행 안내 (스킬이 한 메시지로 출력)

```
Clip 4 — 대시보드를 시작합니다. (Ch 02 마지막)

■ 오늘 할 거
Clip 2~3에서 쓴 sample_csv/ 8개 →
  • 인터랙티브 HTML 대시보드 (index.html)
  • 탭 3개 + 핵심 차트 (Chart.js + papaparse)
  • 1차 뼈대 → 2차 확장 점진 개선
한 사이클로 만듭니다.

■ 진행 방식
영상에서 STEP 1~5 순서대로 실습이 진행됩니다.
영상 일시정지·재생 자유롭게 하면서 본인 워크스페이스에서 같이 따라하세요.

■ STEP 흐름

  STEP 1. 작업 폴더 진입 (스킬이 폴더+sample_csv 자동 준비 완료)
    이미 셋업된 폴더: 50-my-work/Part03-체험하기/실습07-대시보드/
    그대로 이 채팅창에서 STEP 2부터 진행하면 됨.
    (새 터미널에서 따로 열려면: cd 50-my-work/Part03-체험하기/실습07-대시보드 && claude)

  STEP 2. 1단계 질문하기 (B) — "어떻게 만들 수 있어?"
    "sample_csv 8개 CSV 가지고 인터랙티브 대시보드 만들고 싶거든.
     너가 만들려면 어떻게 해야 하냐? 할 수 있냐?"
    클로드코드가 가능성 펼침 (Chart.js·Plotly + papaparse + 탭 구조 등).

  STEP 3. 2단계 기획하기 (U) — "탭 구성 + 차트 옵션"
    "좋아. 그럼 어떤 탭 구성으로 가는 게 좋고,
     각 탭에 어떤 차트들 들어가면 임원이 한눈에 볼 수 있을지 예시 보여줘."
    클로드코드가 탭 구조 옵션 (운영 / 재무 / 라인별) + 각 탭 차트 매핑 펼침.

  STEP 4. 3단계 만들기 (I) — 1차 뼈대 → 2차 확장
    1차: "그 구조대로 index.html 만들어줘.
          한 파일 안에 CDN으로 Chart.js + papaparse.
          탭 3개 + 핵심 차트 1개씩. 1차 버전부터."
    2차 확장: "1번 탭에 차트 2개 더 추가 + 색상 톤 정돈. 다른 탭은 그대로"

  STEP 5. 4+5단계 검토 + 부분 수정 (L+D)
    open index.html → 체크: 차트 데이터 정확? 탭 전환 작동? 모바일 깨짐?
    부분 수정: "2번 탭만 색상 정돈. 다른 건 그대로"

■ 시작
1. 영상 시작 → STEP 1부터 따라가기
2. 영상 끝나면 이 채팅창에 "완료" 또는 "/wrap" 입력 → 결과물 자동 정리
```

---

## 자유 실습 (스킬 SLEEP)

**WRAP 트리거**: `완료` / `/wrap` / `끝` / `다음 클립`
**도움 요청 트리거**: `막혔어요` / `도와줘`

### 도움 안내

```
어디서 막히셨어요?

  • sample_csv 못 찾음 → cp -r ../실습05-데이터분석/sample_csv ./ 다시 실행
  • STEP 2에서 클로드코드가 바로 만들기 시작 → "결과 말고 어떻게 만들 수 있는지 흐름부터" 재요청
  • STEP 3에서 탭 구조 1-2개만 옴 → "탭 구조 옵션 3개 정도로 펼쳐줘. 각 탭에 차트 매핑까지" 재요청
  • 브라우저에서 빈 화면 → F12 콘솔 에러 메시지 그대로 클로드코드에게 전달
  • CSV 못 읽음 → "papaparse CDN으로 sample_csv/ 안 CSV 비동기로 읽기"
  • 차트가 안 그려짐 → "Chart.js v4 사용. canvas 요소 ID 확인하고 데이터 포맷 점검"
  • 부분 수정인데 전체 다시 씀 → "다른 건 그대로" 범위 명시 누락

여전히 막히면 더 구체적으로 알려주세요.
```

---

## WRAP

### 1. 파일 검증

`50-my-work/Part03-체험하기/실습07-대시보드/` 안에 점검:
- `index.html` 존재
- 브라우저에서 열리는지 권장 (open index.html)

`index.html` 없으면 "STEP 4 작성 안 됐어요. 지금 만들까요?" 확인.

### 2. README.md 자동 작성

```markdown
# 실습 7 — 대시보드 (인터랙티브 HTML)

- 완료: {ISO 8601}
- 모델: {claude --version}
- 모드: {Auto / Accept-edits / Default}

## 진행 방식
영상 보면서 실습 (STEP 1~5).

## 5단계 사이클
- 1 질문하기 (B): "대시보드 어떻게 만들 수 있어?"
- 2 기획하기 (U): 탭 구조 + 차트 옵션 받아 고르기
- 3 만들기 (I): index.html 1차 뼈대 → 2차 확장
- 4 검토하기 (L): 데이터 정확·탭 전환·모바일
- 5 개선하기 (D): "N번 탭만 ··· 다른 건 그대로"

## 결과물
- index.html (Chart.js + papaparse, 탭 3개 + 차트 다수)

## 핵심 발견
{자유 입력한 한 줄}

## 다음 클립 연결
Ch 02 종료 — 같은 CSV로 분석·보고서·대시보드 3종 결과물 완료.
다음 Clip 5 (자료 리서치) — Ch 03 시작. 재료 없는 상태에서 콘텐츠 파이프라인.
```

### 3. progress.json 업데이트

```json
{
  "practice_completed": [..., "실습 7"],
  "completed_chapters": [..., "Ch 02"],
  "current_clip": null,
  "last_activity": "{ISO 8601}"
}
```

### 4. 다음 안내

```
✓ 실습 7 (대시보드) 완료. Ch 02 종료.
  같은 CSV에서 분석·보고서·대시보드 세 결과물이 나왔습니다.

다음은 Clip 5 (자료 리서치) — Ch 03 시작. 새 폴더에서 시작.
이어서 진행하려면 /part03 → Clip 5 선택.
```

---

## EDGE CASES

| 상황 | 대응 |
|---|---|
| sample_csv 폴더 없음 | "Clip 2 폴더에서 복사하세요" + cp 명령 안내 |
| STEP 2 생략 → 바로 만들기 요청 | 자유 영역. 결과 차이 확인 |
| 브라우저에 빈 화면 | F12 콘솔 에러 메시지 → AI 재요청 |
| 차트 데이터 어긋남 | "papaparse 결과 콘솔 출력해서 디버그. 다른 건 그대로" |
| 부분 수정인데 전체 다시 씀 | "다른 건 그대로" 누락 |
| `완료` 입력 후 index.html 없음 | "어느 STEP에서 멈췄나요?" 확인 |
